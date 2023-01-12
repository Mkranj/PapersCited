# -*- coding: utf-8 -*-
import pytest
import PapersCited
import textract
import os
import sys

import locale
locale.setlocale(locale.LC_ALL, "")

@pytest.mark.xfail(reason = "VSCode Pytest filepath issue. In terminal, this should xpass")
def test_read_analyze_text():
    text = PapersCited.read_document("tests/sample_text.txt")
    
    # Get all types of citations
    solo_authors = PapersCited.get_matches_solo_author(text, drop_excluded_phrases = True)
    two_authors = PapersCited.get_matches_two_authors(text, drop_excluded_phrases = True)
    three_authors = PapersCited.get_matches_three_authors(text, drop_excluded_phrases = True)
    author_et_al = PapersCited.get_matches_author_et_al(text, drop_excluded_phrases = True)
    two_surnames = PapersCited.get_matches_two_surnames(text, drop_excluded_phrases = True)
    two_surnames_et_al = PapersCited.get_matches_two_surnames_et_al(text, drop_excluded_phrases = True)
        
    solo_authors.delete_clones_of_citations(two_authors)
    
    narrower_citations = PapersCited.CitationType(solo_authors.citations + 
                                      two_authors.citations +
                                      author_et_al.citations)
    
    wider_citations = PapersCited.CitationType(three_authors.citations + 
                                   two_surnames.citations +
                                   two_surnames_et_al.citations)

    narrower_citations.cleanup()
    wider_citations.cleanup(allow_commas = False) # Default False prevents lots of duplication
    
    expected_output = PapersCited.read_document("tests/sample_text_full_correct_list_citations.txt")
    expected_output = expected_output.split("\n")
    
    # When reading from .txt files, encoding/character issues arise.
    # Dealing with Croatian characters errors: Save the .txt file with ANSI encoding!
    
    assert narrower_citations.citations == expected_output