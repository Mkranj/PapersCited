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
  citations.drop_excluded_phrases()
  assert citations.citations ==  ["b 2010"]
  
  croatian_citations = PapersCited.CitationType(["dobar 2010", "tijekom 2010", "je 2010", "tijekom, 2010",])
  croatian_citations.drop_excluded_phrases()
  assert croatian_citations.citations ==\
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
    
def test_removing_duplicates():
  strings = ["a 2000", "b 2000", "a 2000", "b 2000", "b 2000"]
  citations = PapersCited.CitationType(strings)
  assert citations._remove_duplicates() == ["a 2000", "b 2000"]

def test_sorting():
  strings = ["beta 2000", "alpha 2000", "gamma 2000"]
  citations = PapersCited.CitationType(strings)
  assert citations._sort_citations() == ["alpha 2000", "beta 2000", "gamma 2000"]
  
def test_cleanup():
  # All the helper methods need to be applied.
  strings = ["survivor (2000)", "(survivor, 2000)", "survivor 2002", "Author et al 1000"]
  citations = PapersCited.CitationType(strings)
  citations.cleanup() # This doesn't return any values
  assert citations.citations == ["Author et al. 1000", "survivor 2000", "survivor 2002"]
  match_with_many_spaces = ["Manman      (1999"]
  citations_many_spaces = PapersCited.CitationType(match_with_many_spaces)
  citations_many_spaces.cleanup()
  assert citations_many_spaces.citations == ["Manman 1999"]
  
def test_dropping_phrases_and_cleanup():
  strings = ["tijekom 1999", "survivor (2000)", "a 1999", "(survivor, 2000)", "survivor 2002", "Author et al 1000"]
  citations = PapersCited.CitationType(strings)
  citations.drop_excluded_phrases() # This doesn't return any values
  citations.cleanup() # This doesn't return any values
  assert citations.citations == ["Author et al. 1000", "survivor 2000", "survivor 2002"]
