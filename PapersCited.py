# -*- coding: utf-8 -*-
# V 1.2.0

import locale
locale.setlocale(locale.LC_ALL, "")

import os
import sys
import textract
import xlsxwriter

# regex in Python
import re

# GUI elements - for the file dialog. Explicitly import the filedialog submodule.
import tkinter
from tkinter import filedialog

# In the actual string, a single \ is used. But for escaping it, we need to put
# \\ inside strings. Otherwise it will append lines, causing indentation errors.

class RegexPatterns:
    # Phrases that make up regex patterns for detecting citations
    letter_character = "[a-zšđčćžäöüñáéíóúç'’\\-]"
    letter_uppercase = letter_character.upper()
    rest_of_word = letter_character[:-1] + letter_uppercase[1:] + "+"
    years = "(?:\\(?\\d\\d\\d\\d[abcd]?,?\\s?;?)+"
    phrase_and = " (?:and+|[i&]+) "
    phrase_et_al = "(?: et al[\\s,.(]+)"
    phrase_i_sur = "(?: i sur[\\s,.(]+)"

class PhrasesToChange:
    # For clarity and spotting duplicates, remove the following from citations:
    characters_to_exclude = [",", "(", ")", ";", ".", "\n", "_x000D_", "\r"]
    phrases_to_adjust = {
      # "Et al." and "sur." need a dot at the end
      " et al ": " et al. ",
      " sur ": " sur. ",
      # "A1 and A2" is the same as "A1 & A2", default to '&'
      " and ": " & ",
      # For the purposes of detecting duplicates, "sur." and "suradnici" are the same
      "suradnicima": "sur.",
      "suradnici": "sur.",
      "suradnika": "sur.",
    }
    # Before adding something to excluded phrases, Google [word] surname.
    # If anything shows up, don't include that word.
    croatian_excluded_phrases = [
      "^do[ ,]",
      "^i[ ,]",
      "^iz[ ,]",
      "^je[ ,]",
      "^još[ ,]",
      "^konačno[ ,]",
      "^nadalje[ ,]",
      "^nakon[ ,]",
      "^od[ ,]",
      "^poslije[ ,]",
      "^prije[ ,]",
      "^primjerice[ ,]",
      "^slično[ ,]",
      "^tijekom[ ,]",
      "^u[ ,]",
      "^za[ ,]"
    ]
    english_excluded_phrases = [
      "^a[ ,]",
      "^an[ ,]",
      "^at[ ,]",
      "^for[ ,]",
      "^in[ ,]",
      "ISSN", # not necessarily at the start
      "^of[ ,]",
      "^the[ ,]",
      "^when[ ,]"
    ]

# Create a CitationType object for each kind of authorship.

class CitationType:
    def __init__(self, citations):
        self.citations = citations

    
    def cleanup(self, allow_commas = False):
        # Apply all helper methods in a specific order. So extra characters won't affect
        # sorting, etc.
        self.citations = self._remove_extra_characters(allow_commas)
        self.citations = self._separate_name_year()
        self.citations = self._adjust_common_phrases()
        self.citations = self._remove_duplicates()
        self.citations = self._sort_citations()
    
    def drop_excluded_phrases(self):
        # Go through each citation
        # Check if the citation matches any of the excluded phrases (for loop)
        # If anything is a match, replace citation with __DELETE__
        # Remove all __DELETE__ strings

        filtered_citations = self.citations
        excluded_phrases = PhrasesToChange.croatian_excluded_phrases + \
            PhrasesToChange.english_excluded_phrases
        for index_no, citation in enumerate(self.citations):
            for phrase in excluded_phrases:
                match = re.search(
                    phrase,
                    citation,
                    re.IGNORECASE
                )
        # If a match is not found, the result of re.match is None
                if match:
                    filtered_citations[index_no] = "__DELETE__"
        # Retain only citations that haven't been flagged
        filtered_citations = [citation for citation in filtered_citations if citation != "__DELETE__"]
        self.citations = filtered_citations
    
    def _remove_extra_characters(self, allow_commas = False):
        characters_to_remove = PhrasesToChange.characters_to_exclude
        if allow_commas:
            characters_to_remove = characters_to_remove[1:]
        clean_citations = self.citations

        for index_no, citation in enumerate(clean_citations):
            # Remove uneccessary characters
            for character in characters_to_remove:
                clean_citations[index_no] = clean_citations[index_no].replace(character, " ")
            # Remove leading and trailing spaces
            clean_citations[index_no] = clean_citations[index_no].strip()
            # Condense multiple spaces to a single one.
            clean_citations[index_no] = re.sub(" +", " ", clean_citations[index_no])
        return(clean_citations)
    
    def _separate_name_year(self):
        citations = self.citations
        rx = RegexPatterns()
        # If letters and digits are "adjacent", put a space in between 
        separated_citations = [re.sub("(" + rx.rest_of_word + ")(\\d\\d)", "\\g<1> \\g<2>", citation)\
            for citation in citations]
        return(separated_citations)

    def _adjust_common_phrases(self):
        phrases_to_adjust = PhrasesToChange.phrases_to_adjust
        clean_citations = self.citations

        for index_no, citation in enumerate(clean_citations):
            # Change several phrases
            for key in phrases_to_adjust:
                clean_citations[index_no] = clean_citations[index_no].replace(key, phrases_to_adjust[key])
        return(clean_citations)
    
    def _remove_duplicates(self):
        citations = self.citations
        unique_citations = []

        for index_no, citation in enumerate(citations):
            # If the current citation HASN'T been mentioned yet, add it to the list of unique citations
            # - these will end up in the output file.
            # For determining if it has been mentioned, compare the casefold current citation with
            # a list comprehension returning casefold versions of mentioned citations.
            if citation.casefold() not in [stored_citation.casefold() for stored_citation in unique_citations]:
                unique_citations.append(citation)
        return(unique_citations)
    
    def _sort_citations(self):
        citations = self.citations
        # Sort the list alphabetically, ignoring case.
        sorted_citations = sorted(citations, key=str.casefold)

        # Apply locale settings for sorting alphabetically by characters like 'Š'
        sorted_citations = sorted(sorted_citations, key=locale.strxfrm)
        return(sorted_citations)
    
    def delete_clones_of_citations(self, Citation_object):
    # If a citation is part of a set of "wider" citations (one author of two)
    # flag it for deletetion.
        narrow_citations = self.citations
        wide_citations = Citation_object.citations
        
        for wider_citation in wide_citations:
            narrow_citation_no = 0
            found_match_for_wider_citation = False
            while narrow_citation_no <= len(narrow_citations) and found_match_for_wider_citation == False:
                if narrow_citations[narrow_citation_no] in wider_citation:
                    found_match_for_wider_citation = True
                    narrow_citations[narrow_citation_no] = "__DELETE__"
                narrow_citation_no += 1
        # Retain only citations that haven't been flagged
        narrow_citations = [citation for citation in narrow_citations if citation != "__DELETE__"]
        self.citations = narrow_citations

# FUNCTIONS ----

# Open a file dialog to select a file to process.
def get_file():
    root = tkinter.Tk()
    # Make the main window of tkinter invisible since we only need the dialog.
    root.withdraw()
    root.attributes("-topmost", True)
    filename = filedialog.askopenfilename(title = "Select a document to search for citations:")
    root.destroy()
    return(filename)


def check_file(filename):
    # Check if the file entered actually exists
    file_exists = os.path.isfile(filename)

    # If the filename is False, exit the program.
    if file_exists == False:
        input("No file selected. Press Enter to end the program.")
        sys.exit()

    # Warning for PDF files:
    file_extension = filename[-4:]
    if file_extension.casefold() == ".pdf":
        print("Warning!\nReading PDF files is not recommended and might result in inaccurate transcription.\n")

    if file_extension.casefold() == ".txt":
        print("Warning! Reading .txt files might lead to problems with special characters." +
              "\nTo ensure best the best format is used, backup the .txt file, then save it in ANSI encoding." +
              "\n(\"Save as...\" dialog, \"Encoding:\" at the bottom.)\n")


def read_document(filename):

    try:
        target_document = textract.process(filename)
    except:
        # If the file exists, but cannot be read, an error will be raised.
        print(
            f"The file {filename} couldn't be read. Make sure the file is a valid textual file.")
        print("If you can regularly open it, you may be missing certain libraries:")
        print("antiword for .doc (not .docx)")
        print("poppler for .pdf")
        print("\nPlease check 'help_with_libraries.txt' at PapersCited Github.")
        input("\nPress Enter to exit the program.")
        sys.exit()

    # UTF-8 encoding so it recognises foreign characters
    target_document = target_document.decode("utf-8")
    
    file_extension = filename[-4:]
    if file_extension.casefold() == ".pdf":
        target_document = target_document.replace("\r\n", " ")
        target_document = target_document.replace("\r", "")
        target_document = target_document.replace("\n", " ")
    return(target_document)

def get_matches_solo_author(text, drop_excluded_phrases = False):
    # Regardless of case
    rx = RegexPatterns()
    matches = re.findall(
        rx.letter_character + rx.rest_of_word + "[\\s,(]+" + rx.years,
        text,
        re.IGNORECASE)
    matches = CitationType(matches)
    if drop_excluded_phrases: matches.drop_excluded_phrases()
    return(matches)

def get_matches_two_authors(text, drop_excluded_phrases = False):
    # Regardless of case
    rx = RegexPatterns()
    matches = re.findall(
        rx.letter_character + rx.rest_of_word + rx.phrase_and +
        rx.letter_character + rx.rest_of_word + "[\\s,(]+" + rx.years,
        text,
        re.IGNORECASE)
    matches = CitationType(matches)
    if drop_excluded_phrases: matches.drop_excluded_phrases()
    return(matches)

def get_matches_author_et_al(text, drop_excluded_phrases = False):
    # Regardless of case
    rx = RegexPatterns()
    matches = re.findall(
        rx.letter_character + rx.rest_of_word + "(?:" + rx.phrase_et_al + "|" + rx.phrase_i_sur + ")" + rx.years,
        text,
        re.IGNORECASE)
    matches = CitationType(matches)
    if drop_excluded_phrases: matches.drop_excluded_phrases()
    return(matches)
  
def get_matches_three_authors(text, drop_excluded_phrases = False):
    # Will probably catch too much.
    # To remedy some, the first letter of the first two words must be capitalised.
    # The last doesn't, so it catches the term "suradnici" common for multiple authors.
    rx = RegexPatterns()
    matches = re.findall(
        rx.letter_uppercase + rx.rest_of_word + "[\\s,]+" +
        rx.letter_uppercase + rx.rest_of_word + rx.phrase_and + 
        rx.rest_of_word + "[\\s,(]+" + rx.years,
        text)
    matches = CitationType(matches)
    if drop_excluded_phrases: matches.drop_excluded_phrases()
    return(matches)

def get_matches_two_surnames(text, drop_excluded_phrases = False):
    # Both names must me capitalised for it to be a valid citation.
    rx = RegexPatterns()
    matches = re.findall(
        rx.letter_uppercase + rx.rest_of_word + "[\\s]+" +
        rx.letter_uppercase + rx.rest_of_word + "[\\s,(]+" + rx.years,
        text)
    matches = CitationType(matches)
    if drop_excluded_phrases: matches.drop_excluded_phrases()
    return(matches)

def get_matches_two_surnames_et_al(text, drop_excluded_phrases = False):
    # Both names must me capitalised for it to be a valid citation.
    rx = RegexPatterns()
    matches = re.findall(
        rx.letter_uppercase + rx.rest_of_word + "[\\s]+" +
        rx.letter_uppercase + rx.rest_of_word + "(?:" + rx.phrase_et_al + "|" + rx.phrase_i_sur + ")" + rx.years,
        text)
    matches = CitationType(matches)
    if drop_excluded_phrases: matches.drop_excluded_phrases()
    return(matches)
            
def write_excel(filename, citations, wider_citations):
    # Retrieve the directory in which the analysed document is located,
    # The output file will be created in the same directory.
    output_folder = os.path.dirname(filename)
    output_filename = output_folder + "/citations.xlsx"

    # Create a file
    try:
        workbook = xlsxwriter.Workbook(output_filename)
    except:
        print(f"Cannot create a file at {output_filename}.")
        print("Possible permissions issue, can you create files at that folder?")
        input("\nPress Enter to exit the program.")
        sys.exit()

    worksheet1 = workbook.add_worksheet()

    # We'll write in the second column.
    # The first column is useful for marking certain citations as "done" or "double-check"
    column = 1
    row = 0

    # Iterate through output list
    for item in citations.citations:
        worksheet1.write(row, column, item)
        row += 1

    # If there are potential wider matches, write them in the sixth column.
    if wider_citations:
        column = 5
        row = 0
        for item in wider_citations.citations:
            worksheet1.write(row, column, item)
            row += 1
    
    workbook.close()
    
    n_narrower_citations = len(citations.citations) 
    try:
        n_wider_citations = len(wider_citations.citations) 
        total_citations = n_narrower_citations + n_wider_citations
    except:
        total_citations = n_narrower_citations
    
    print(f"Success! A file has been created at {output_filename}.")
    
    if n_wider_citations:
        print(f"{n_narrower_citations} citations have been found, along with" +
              f" {n_wider_citations} wider citations, displayed to the right.")
    
    print(f"A total of {total_citations} different citations have been recorded.")
    input("\nPress Enter to exit the program.")

# MAIN ----

def main():
    filename = get_file()
    check_file(filename)
    document = read_document(filename)
    
    # Get all types of citations
    solo_authors = get_matches_solo_author(document, drop_excluded_phrases = True)
    two_authors = get_matches_two_authors(document, drop_excluded_phrases = True)
    three_authors = get_matches_three_authors(document, drop_excluded_phrases = True)
    author_et_al = get_matches_author_et_al(document, drop_excluded_phrases = True)
    two_surnames = get_matches_two_surnames(document, drop_excluded_phrases = True)
    two_surnames_et_al = get_matches_two_surnames_et_al(document, drop_excluded_phrases = True)
        
    solo_authors.delete_clones_of_citations(two_authors)
    
    narrower_citations = CitationType(solo_authors.citations + 
                                      two_authors.citations +
                                      author_et_al.citations)
    
    wider_citations = CitationType(three_authors.citations + 
                                   two_surnames.citations +
                                   two_surnames_et_al.citations)
    
    narrower_citations.cleanup()
    wider_citations.cleanup(allow_commas = False) # False prevents lots of duplication
    write_excel(filename, narrower_citations, wider_citations)

if __name__ == "__main__":
    main()
