import locale
locale.setlocale(locale.LC_ALL, "")

import UI.messages as ms

# regex in Python
import regex

# In the actual string, a single \ is used. But for escaping it, we need to put
# \\ inside strings. Otherwise it will append lines, causing indentation errors.

class RegexPatterns:
    # Phrases that make up regex patterns for detecting citations
    letter_lowercase = "\\p{Ll}"
    letter_uppercase = "\\p{Lu}"
    rest_of_word = "(?:\\p{L}|['’\\-])+"
    # For years - must be exactly four digits, not followed by another digit.
    years = "(?:\\(?\\d{4}(?!\\d)[abcd]?,?\\s?;?\\s?)+"
    phrase_and = " +(?:and+|[i&]+) +"
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
      # Change possesive form to a proper noun
      "'s" : ""
    }
    # Before adding something to excluded phrases, Google [word] surname.
    # If anything shows up, don't include that word.
    croatian_excluded_phrases = [
      "^do[ ,]",
      "^i[ ,]",
      "istraživanje",
      "^iz[ ,]",
      "^je[ ,]",
      "^još[ ,]",
      "^konačno[ ,]",
      "metaanaliza",
      "meta-analiza",
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
        self.citations = self._separate_multiple_years()
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
                match = regex.search(
                    phrase,
                    citation,
                    regex.IGNORECASE
                )
        # If a match is not found, the result of regex.match is None
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
            clean_citations[index_no] = regex.sub(" +", " ", clean_citations[index_no])
        return(clean_citations)
    
    def _separate_name_year(self):
        citations = self.citations
        rx = RegexPatterns()
        # If letters and digits are "adjacent", put a space in between 
        separated_citations = [regex.sub("(" + rx.rest_of_word + ")(\\d\\d)", "\\g<1> \\g<2>", citation)\
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
    
    def _separate_multiple_years(self):
        rx = RegexPatterns()
        all_citations = self.citations
        # For each citation, find how many years it contains.
        # If it contains more than one, get the years as a list.
        # Flag the original citation for deletion
        single_year_pattern = "\\d{4}[abcd]?"
        all_years_pattern = rx.years
        extracted_citations = []
        
        for index_no, citation in enumerate(all_citations):
            years = regex.findall(pattern = single_year_pattern, string = citation)
            # findall always returns a list
            if len(years) > 1:
                citation_start = regex.sub(all_years_pattern, "", citation)
                all_citations[index_no] = "__DELETE__"
                new_citations = [citation_start + year for year in years]
                extracted_citations.extend(new_citations)
        
        expanded_citations = [citation for citation in all_citations if citation != "__DELETE__"]
        expanded_citations.extend(extracted_citations)
        return(expanded_citations)        
    
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
            while narrow_citation_no <= len(narrow_citations) - 1 and found_match_for_wider_citation == False:
                if narrow_citations[narrow_citation_no] in wider_citation:
                    found_match_for_wider_citation = True
                    narrow_citations[narrow_citation_no] = "__DELETE__"
                narrow_citation_no += 1
        # Retain only citations that haven't been flagged
        narrow_citations = [citation for citation in narrow_citations if citation != "__DELETE__"]
        self.citations = narrow_citations

# FUNCTIONS ----

def get_matches_solo_author(text, drop_excluded_phrases = False):
    rx = RegexPatterns()
    matches = regex.findall(
        rx.letter_uppercase + rx.rest_of_word + "[\\s,(]+" + rx.years,
        text)
    matches = CitationType(matches)
    if drop_excluded_phrases: matches.drop_excluded_phrases()
    return(matches)

def get_matches_two_authors(text, drop_excluded_phrases = False):
    # The second word doesn't have to be uppercase, to catch "suradnici".
    rx = RegexPatterns()
    matches = regex.findall(
        rx.letter_uppercase + rx.rest_of_word + rx.phrase_and +
        rx.rest_of_word + "[\\s,(]+" + rx.years,
        text)
    matches = CitationType(matches)
    if drop_excluded_phrases: matches.drop_excluded_phrases()
    return(matches)

def get_matches_author_et_al(text, drop_excluded_phrases = False):
    rx = RegexPatterns()
    matches = regex.findall(
        rx.letter_uppercase + rx.rest_of_word + "(?:" + rx.phrase_et_al + "|" + rx.phrase_i_sur + ")" + rx.years,
        text)
    matches = CitationType(matches)
    if drop_excluded_phrases: matches.drop_excluded_phrases()
    return(matches)
  
def get_matches_three_authors(text, drop_excluded_phrases = False):
    # Will probably catch too much.
    # To remedy some, the first letter of the first two words must be capitalised.
    # The last doesn't, so it catches the term "suradnici" common for multiple authors.
    rx = RegexPatterns()
    matches = regex.findall(
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
    matches = regex.findall(
        rx.letter_uppercase + rx.rest_of_word + "[\\s]+" +
        rx.letter_uppercase + rx.rest_of_word + "[\\s,(]+" + rx.years,
        text)
    matches = CitationType(matches)
    if drop_excluded_phrases: matches.drop_excluded_phrases()
    return(matches)

def get_matches_two_surnames_et_al(text, drop_excluded_phrases = False):
    # Both names must me capitalised for it to be a valid citation.
    rx = RegexPatterns()
    matches = regex.findall(
        rx.letter_uppercase + rx.rest_of_word + "[\\s]+" +
        rx.letter_uppercase + rx.rest_of_word + "(?:" + rx.phrase_et_al + "|" + rx.phrase_i_sur + ")" + rx.years,
        text)
    matches = CitationType(matches)
    if drop_excluded_phrases: matches.drop_excluded_phrases()
    return(matches)
    
def preview_citations(citations, wider_citations):
    print("\n")
    print("Citations found:")
    [print(citation) for citation in citations.citations]
    if len(wider_citations.citations) > 0:
        print("\n")
        print("Wider citations found:")
        [print(citation) for citation in wider_citations.citations]

def citations_to_string(narrower_citations, wider_citations):
  citation_string = []
  [citation_string.append(citation + "\n") for citation in narrower_citations.citations]
  if len(wider_citations.citations) > 0:
      [citation_string.append(citation + "\n") for citation in wider_citations.citations]
  results = "".join(citation_string)
  return(results)

# For display and saving to .txt, visually separate wider citations
def citations_to_string_pretty(narrower_citations, wider_citations):
  citation_string = []
  [citation_string.append(citation + "\n") for citation in narrower_citations.citations]
  if len(wider_citations.citations) > 0:
      citation_string.append("\n" + ms.break_with_lines + \
                             "\nLonger citations detected:\n\n")
      [citation_string.append(citation + "\n") for citation in wider_citations.citations]
  results = "".join(citation_string)
  return(results)