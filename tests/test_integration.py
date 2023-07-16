# -*- coding: utf-8 -*-
import pytest
import PapersCited.citationAnalysis as ca
from PapersCited.fileManipulation import read_document
import os

import locale
locale.setlocale(locale.LC_ALL, "")

@pytest.mark.xfail(reason = "VSCode Pytest issue with ANSI encoding. In terminal, this should xpass")
def test_read_analyze_text(rootdir):
    text = read_document(os.path.join(rootdir, "sample_text.txt"))
    
    # Get all types of citations
    solo_authors = ca.get_matches_solo_author(text, drop_excluded_phrases = True)
    two_authors = ca.get_matches_two_authors(text, drop_excluded_phrases = True)
    three_authors = ca.get_matches_three_authors(text, drop_excluded_phrases = True)
    author_et_al = ca.get_matches_author_et_al(text, drop_excluded_phrases = True)
    two_surnames = ca.get_matches_two_surnames(text, drop_excluded_phrases = True)
    two_surnames_et_al = ca.get_matches_two_surnames_et_al(text, drop_excluded_phrases = True)
        
    solo_authors.delete_clones_of_citations(two_authors)
    
    narrower_citations = ca.CitationType(solo_authors.citations + 
                                      two_authors.citations +
                                      author_et_al.citations)
    
    wider_citations = ca.CitationType(three_authors.citations + 
                                   two_surnames.citations +
                                   two_surnames_et_al.citations)

    narrower_citations.cleanup()
    wider_citations.cleanup(allow_commas = False) # Default False prevents lots of duplication
    
    expected_output = read_document(os.path.join(rootdir, "sample_text_full_correct_list_citations.txt"))
    expected_output = expected_output.split("\n")
    
    # When reading from .txt files, encoding/character issues arise.
    # Dealing with Croatian characters errors: Save the .txt file with ANSI encoding!
    
    assert narrower_citations.citations == expected_output
    
def test_main_text_and_docx_footnotes_analyzed(rootdir):
    text = read_document(os.path.join(rootdir, "document_footnotes.docx"))
    
    # Get all types of citations
    solo_authors = ca.get_matches_solo_author(text, drop_excluded_phrases = True)
    two_authors = ca.get_matches_two_authors(text, drop_excluded_phrases = True)
    three_authors = ca.get_matches_three_authors(text, drop_excluded_phrases = True)
    author_et_al = ca.get_matches_author_et_al(text, drop_excluded_phrases = True)
    two_surnames = ca.get_matches_two_surnames(text, drop_excluded_phrases = True)
    two_surnames_et_al = ca.get_matches_two_surnames_et_al(text, drop_excluded_phrases = True)
        
    solo_authors.delete_clones_of_citations(two_authors)
    
    narrower_citations = ca.CitationType(solo_authors.citations + 
                                      two_authors.citations +
                                      author_et_al.citations)
    
    wider_citations = ca.CitationType(three_authors.citations + 
                                   two_surnames.citations +
                                   two_surnames_et_al.citations)

    narrower_citations.cleanup()
    wider_citations.cleanup(allow_commas = False) 
    
    expected_output = ["FootnoteAuthor 1111", "FootnoteAuthorTwo 2222",  "RegularAuthor 2010"]
      
    assert narrower_citations.citations == expected_output

def test_docx_without_footnotes_analyzed(rootdir):
    text = read_document(os.path.join(rootdir, "document_no_footnotes.docx"))
    
    # Get all types of citations
    solo_authors = ca.get_matches_solo_author(text, drop_excluded_phrases = True)
    two_authors = ca.get_matches_two_authors(text, drop_excluded_phrases = True)
    three_authors = ca.get_matches_three_authors(text, drop_excluded_phrases = True)
    author_et_al = ca.get_matches_author_et_al(text, drop_excluded_phrases = True)
    two_surnames = ca.get_matches_two_surnames(text, drop_excluded_phrases = True)
    two_surnames_et_al = ca.get_matches_two_surnames_et_al(text, drop_excluded_phrases = True)
        
    solo_authors.delete_clones_of_citations(two_authors)
    
    narrower_citations = ca.CitationType(solo_authors.citations + 
                                      two_authors.citations +
                                      author_et_al.citations)
    
    wider_citations = ca.CitationType(three_authors.citations + 
                                   two_surnames.citations +
                                   two_surnames_et_al.citations)

    narrower_citations.cleanup()
    wider_citations.cleanup(allow_commas = False) 
    
    expected_output = ["RegularAuthor 2010"]
      
    assert narrower_citations.citations == expected_output