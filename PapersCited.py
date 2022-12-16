# -*- coding: utf-8 -*-
# V 1.1.0

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
    letter_character = "[a-zšđčćžäöüñáéíóú'’\\-]"
    letter_uppercase = letter_character.upper()
    rest_of_word = "[a-zšđčćžäöüñáéíóú'’\\-]+"
    years = "(?:\\(?\\d\\d\\d\\d[abcd]?,?\\s?;?)+"
    phrase_and = " (?:and+|[i&]+)+ "

# Class CitationType, with lists for filtering

class PhrasesToChange:
    # For clarity and spotting duplicates, remove the following from citations:
    characters_to_exclude = [",", "(", ")", ";", "."]
    phrases_to_adjust = {
      # "Et al." and "sur." need a dot at the end
      " et al ": " et al. ",
      " sur ": " sur. ",
      # "A1 and A2" is the same as "A1 & A2", default to '&'
      " and ": " & ",
      # For the purposes of detecting duplicates, "sur." and "suradnici" are the same
      "suradnici": "sur.",
      "suradnika": "sur.",
    }
    croatian_excluded_phrases = [
      "^u ",
      "^tijekom ",
      "^nakon ",
      "^za ",
      "^je ",
      "^i ",
      "^do ",
      "^prije ",
      "^od ",
      "^poslije ",
      "^iz "
    ]
    english_excluded_phrases = [
      "^a ",
      "^an ",
      "^at ",
      "^in ",
      "^of ",
      "^when ",
      "^for ",
      "^the "
    ]

# Create CitationType for each kind of authorship.
# Filter their citations to encompass clones. (pair to trio doesn't need to be pruned!)
# Then combine .citations of solo, pair and et al. authorships

class CitationType:
    def __init__(self, citations):
        self.citations = citations
 
    # TO DO - .delete_clones_citations(parent_citations) method.
    # After that, apply drop_excluded_phrases() and cleanup()
    
    def cleanup(self):
        # Apply all helper methods in a specific order. So extra characters won't affect
        # sorting, etc.
        self.citations = self._remove_extra_characters()
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
                match = re.match(
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
    
    def _remove_extra_characters(self):
        characters_to_remove = PhrasesToChange.characters_to_exclude
        clean_citations = self.citations

        for index_no, citation in enumerate(clean_citations):
            # Remove uneccessary characters
            for character in characters_to_remove:
                clean_citations[index_no] = clean_citations[index_no].replace(
                    character, "")
            # Remove leading and trailing spaces with strip() to not confuse the duplicate detection
            clean_citations[index_no] = clean_citations[index_no].strip()
            # Condense multiple spaces to a single one.
            clean_citations[index_no] = re.sub(" +", " ", clean_citations[index_no])
        return(clean_citations)

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
    if file_extension == ".pdf":
        print("Warning!\nReading PDF files is not recommended and might result in inaccurate transcription.")


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
    return(target_document)

def get_matches_solo_author(text):
    # Regardless of case
    rx = RegexPatterns()
    matches = re.findall(
        rx.letter_character + rx.rest_of_word + "[\\s,(]+" + rx.years,
        text,
        re.IGNORECASE)
    return(matches)

def get_matches_two_authors(text):
    # Regardless of case
    rx = RegexPatterns()
    matches = re.findall(
        rx.letter_character + rx.rest_of_word + rx.phrase_and +
        rx.letter_character + rx.rest_of_word + "[\\s,(]+" + rx.years,
        text,
        re.IGNORECASE)
    return(matches)

def get_matches_author_et_al(text):
    # Regardless of case
    rx = RegexPatterns()
    matches = re.findall(
        rx.letter_character + rx.rest_of_word + " et al[\\s,.(]+" + rx.years,
        text,
        re.IGNORECASE)
    return(matches)  
  
def get_matches_three_authors(text):
    # Will probably catch too much, so don't filter by this.
    # To remedy some, the first letter of every word must be capitalised.
    rx = RegexPatterns()
    matches = re.findall(
        rx.letter_uppercase + rx.rest_of_word + "[\\s,]+" +
        rx.letter_uppercase + rx.rest_of_word + rx.phrase_and + 
        rx.letter_uppercase + rx.rest_of_word + "[\\s,(]+" + rx.years,
        text)
    return(matches)


# CLONING
#     # Which authors detected in matches_single_author are actually part of "Author & author / author and author"?
#     # Detect the pattern starting with " and/&/i " in matches_multiple_authors. Note the enclosing spaces.
# 
#     second_authors = []
#     for index_no, citation in enumerate(matches_multiple_authors):
#         second_authors.append(
#             re.findall(
#                 " (?:and+|[i&]+)+ " + rx_author_name + "[\s,(]+" + rx_years,
#                 citation,
#                 re.IGNORECASE,
#             )
#         )
# 
#     # It's a list of lists, turn it into a list of strings
#     second_authors = ["".join(citation) for citation in second_authors]
# 
#     # Some strings in second_authors might be empty.
#     # That's because it came across "i sur.", but didn't copy it because of the dot.
#     # These should be dropped from the second_authors list.
#     second_authors = list(filter(None, second_authors))
# 
#     # Why don't we allow the dot?
#     # Because then we'd have to allow it in matches_single_author, which would then interpret
#     # starting a new sentence with a four digit number as a citation.
# 
#     # Strip "and/&/i" from the start of lines. For safety, the count of things to be replaced is 1.
#     # Note that the words are enclosed with spaces!
#     starts_with_and = [" and ", " & ", " i "]
# 
#     for index_no, citation in enumerate(second_authors):
#         # Citation by citation, check and change all listed symbols
#         for phrase in starts_with_and:
#             second_authors[index_no] = second_authors[index_no].replace(phrase, "", 1)
# 
#     # Now we have two lists, all authors with year detected and only those who occur after an 'i'/'&'
#     # For each occuring in the second list, delete ONE from the first - so if theres A & B 2000 and also B 2000,
#     # The second one will be its own instance and won't be deleted
#     # the remove() method does exactly what we want - removes the first element matching the value given
# 
#     for author in second_authors:
#         if author in matches_single_author:
#             matches_single_author.remove(author)
#         else:
#             # All of second_authors should be included in matches_single_author.
#             # If there's unmatching entries in second_authors, notify the user.
#             print(
#                 f"Error! {author} detected as a second author, but is not part of single author citations found.")
#             print("Please report this as a bug at github.com/Mkranj/PapersCited")
#             print("The program will still generate a usable output.")


# TO DO - Trio citations should be printed on another column.
# Two inputs - citations for second columns, citations for fourth column
# Put a warning in fourth column that these longer matches are less precise. 

def write_excel(list_of_matches, filename):

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
    for item in list_of_matches:
        worksheet1.write(row, column, item)
        row += 1

    workbook.close()

    print(f"Success! A file has been created at {output_filename}.")
    print(f"A total of {len(list_of_matches)} different citations have been recorded.")
    input("\nPress Enter to exit the program.")

# MAIN ----
# Using the defined lists of phrases/characters as arguments


# def main(characters_to_remove, phrases_to_adjust, phrases_to_exclude):
    # locale.setlocale(locale.LC_ALL, "")
    # filename = get_file()
    # check_file(filename)
    # document = read_document(filename)
    # matches = get_matches(document)
    # matches = remove_characters_adjust_phrases(
        # matches, characters_to_remove, phrases_to_adjust)
    # matches = remove_duplicates(matches)
    # matches = exclude_phrases(
        # matches, phrases_to_exclude)
    # matches = sort_citations(matches)
    # write_excel(matches, filename)


# if __name__ == "__main__":
    # main(characters_to_remove, phrases_to_adjust,
        # phrases_to_exclude = croatian_excluded_phrases + english_excluded_phrases)
