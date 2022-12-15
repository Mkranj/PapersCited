import pytest

import PapersCited

# Test class behavour
def test_PhrasesToChange_has_all_attributes():
  phrases = PapersCited.PhrasesToChange()
  assert isinstance(phrases.characters_to_exclude, list)
  assert isinstance(phrases.croatian_excluded_phrases, list)
  assert isinstance(phrases.english_excluded_phrases, list)
  assert isinstance(phrases.phrases_to_adjust, dict)

def test_dropping_citations_starting_with_excluded_phrases():
  strings = ["a 2010", "b 2010", "of 2010"]
  citations = PapersCited.CitationType(strings)
  assert citations.drop_excluded_phrases() ==  ["b 2010"]
  
  croatian_citations = PapersCited.CitationType(["dobar 2010", "tijekom 2010", "je 2010"])
  assert croatian_citations.drop_excluded_phrases() ==\
    ["dobar 2010"]
    
def test_removing_extra_characters_from_citations():
  strings = ["(Swirly) 2000", ",Comma, 2000", "(Everything.); 2010"]
  citations = PapersCited.CitationType(strings)
  assert citations._remove_extra_characters() ==\
    ["Swirly 2000", "Comma 2000", "Everything 2010"]
    
def test_adjusting_phrases():
  strings = ["One et al 1999", "Autor i suradnici 1999", "Autora i suradnika 1999"]
  citations = PapersCited.CitationType(strings)
  assert citations._adjust_common_phrases() ==\
    ["One et al. 1999", "Autor i sur. 1999", "Autora i sur. 1999"]