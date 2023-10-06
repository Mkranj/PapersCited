# Test fns in citationAnalysis that don't find matches itself, but perform
# cleanup, characters removal, duplicates removal etc.
import citationAnalysis.citationAnalysis as ca

def test_PhrasesToChange_has_all_attributes():
  phrases = ca.PhrasesToChange()
  assert isinstance(phrases.characters_to_exclude, list)
  assert isinstance(phrases.croatian_excluded_phrases, list)
  assert isinstance(phrases.english_excluded_phrases, list)
  assert isinstance(phrases.phrases_to_adjust, dict)

def test_dropping_citations_starting_with_excluded_phrases():
  strings = ["a 2010", "b 2010", "of 2010"]
  citations = ca.CitationType(strings)
  citations.drop_excluded_phrases()
  assert citations.citations ==  ["b 2010"]
  
  croatian_citations = ca.CitationType(["dobar 2010", "tijekom 2010", "je 2010", "tijekom, 2010"])
  croatian_citations.drop_excluded_phrases()
  assert croatian_citations.citations ==\
    ["dobar 2010"]
  croatian_uppercase = ca.CitationType(["Dobar 2010", "Tijekom 2010", "Je 2010", "Tijekom, 2010"])
  croatian_uppercase.drop_excluded_phrases()
  assert croatian_uppercase.citations == ["Dobar 2010"]
  croatian_research = ca.CitationType(["Istraživanje Cooper i sur. 2019",
                                                "Istraživanje Kleinlooga i sur. 2019",
                                                "Meta-analiza Black i sur. 2015"])
  croatian_research.drop_excluded_phrases()
  assert croatian_research.citations == []
    
def test_removing_extra_characters_from_citations():
  strings = ["(Swirly) 2000", ",Comma, 2000", "(Everything.); 2010"]
  citations = ca.CitationType(strings)
  assert citations._remove_extra_characters() ==\
    ["Swirly 2000", "Comma 2000", "Everything 2010"]
    
def test_adjusting_phrases():
  strings = ["One et al 1999", "Autor i suradnici 1999", "Autora i suradnika 1999"]
  citations = ca.CitationType(strings)
  assert citations._adjust_common_phrases() ==\
    ["One et al. 1999", "Autor i sur. 1999", "Autora i sur. 1999"]
    
def test_removing_duplicates():
  strings = ["a 2000", "b 2000", "a 2000", "b 2000", "b 2000"]
  citations = ca.CitationType(strings)
  assert citations._remove_duplicates() == ["a 2000", "b 2000"]

def test_sorting():
  strings = ["beta 2000", "alpha 2000", "gamma 2000"]
  citations = ca.CitationType(strings)
  assert citations._sort_citations() == ["alpha 2000", "beta 2000", "gamma 2000"]
  
def test_cleanup():
  # All the helper methods need to be applied.
  strings = ["survivor (2000)", "(survivor, 2000)", "survivor 2002", "Author et al 1000"]
  citations = ca.CitationType(strings)
  citations.cleanup() # This doesn't return any values
  assert citations.citations == ["Author et al. 1000", "survivor 2000", "survivor 2002"]
  match_with_many_spaces = ["Manman      (1999"]
  citations_many_spaces = ca.CitationType(match_with_many_spaces)
  citations_many_spaces.cleanup()
  assert citations_many_spaces.citations == ["Manman 1999"]

def test_cleanup_multiple_years():
  # All the helper methods need to be applied.
  strings = ["survivor (2000a)", "(survivor, 2000b)", "survivor 2002", "Author et al 1000"]
  citations = ca.CitationType(strings)
  citations.cleanup() # This doesn't return any values
  assert citations.citations == ["Author et al. 1000", "survivor 2000a", "survivor 2000b", "survivor 2002"]

def test_dropping_phrases_and_cleanup():
  strings = ["tijekom 1999", "survivor (2000)", "a 1999", "(survivor, 2000)", "survivor 2002", "Author et al 1000"]
  citations = ca.CitationType(strings)
  citations.drop_excluded_phrases() # This doesn't return any values
  citations.cleanup() # This doesn't return any values
  assert citations.citations == ["Author et al. 1000", "survivor 2000", "survivor 2002"]

def test_deleting_clones():
  narrow_citations = ca.CitationType(["Second, 1999", "Third, 2000", "Third, 2000", "Fourth, 2000"])
  wide_citations = ca.CitationType(["First and Second, 1999", "First and Third, 2000"])
  
  narrow_citations.delete_clones_of_citations(wide_citations)
  assert narrow_citations.citations == ["Third, 2000", "Fourth, 2000"]
  
def test_separating_year_from_name():
  test1 = "boney1999"
  test2 = "Rad and Amazing2010"
  test3 = "rač2000"
  examples = ca.CitationType([test1, test2, test3])
  assert examples._separate_name_year() == \
    ["boney 1999", "Rad and Amazing 2010", "rač 2000"]
    
def test_no_newlines_in_citations():
  test1 = "Aaa\n 2007"
  test2 = "Bbb\n\n\n2010"
  examples = ca.CitationType([test1, test2])
  examples.cleanup()
  assert examples.citations == ["Aaa 2007", "Bbb 2010"]
  
def test_separating_multiple_years():
  text = "AuthorA (2000; 2002; 2003) thoroughly explored..."
  matches = ca.get_matches_solo_author(text)
  matches = ca.CitationType(matches._remove_extra_characters())
  assert matches._separate_multiple_years() == ["AuthorA 2000", "AuthorA 2002", "AuthorA 2003"]
  
  text_abc = "AuthorA (2000a; 2000b; 2000c) thoroughly explored..."
  matches = ca.get_matches_solo_author(text_abc)
  matches = ca.CitationType(matches._remove_extra_characters())
  assert matches._separate_multiple_years() == ["AuthorA 2000a", "AuthorA 2000b", "AuthorA 2000c"]