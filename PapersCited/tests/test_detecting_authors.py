import citationAnalysis.citationAnalysis as ca

# The \ indicates code continues in the next line
# When testing individual detection functions, they SHOULD catch extra characters
# between match start and end (first letter of name, last digit/;) 

def test_detecting_single_authors():
    test_string = "Yado (2008) and Hailey (2010) are the Best. 2009 is the final year Worst (2000) spoke of."
    # Best 2009 should not be detected as a citation.
    assert ca.get_matches_solo_author(test_string).citations ==\
        ["Yado (2008", "Hailey (2010", "Worst (2000"]
    test_string_lowercase = "Uppercase (1999) gets detected, while lowercase (2000) doesn't."
    assert ca.get_matches_solo_author(test_string_lowercase).citations ==\
        ["Uppercase (1999"]
    test_string_semicolon = "This is the facts (Truth, 1980). Also see Hard, 1980; Facts, 1989."
    assert ca.get_matches_solo_author(test_string_semicolon).citations ==\
        ["Truth, 1980", "Hard, 1980; ", "Facts, 1989"]
    test_string_and = "Villa and Maria (1875) was the best show ever. Mirko i Birko (1999) napisali su cijelu knjigu o tome."
    # What this function detects WILL NOT be the whole citation. We still need it for controlling two-author matches.
    assert ca.get_matches_solo_author(test_string_and).citations ==\
        ["Maria (1875", "Birko (1999"]
    test_string_many_spaces = "Manman      (1999) really liked his space."
    assert ca.get_matches_solo_author(test_string_many_spaces).citations ==\
        ["Manman      (1999"]
    test_string_foreign_characters_capitalization = "ULLÉN (1888) made an earlier work."
    assert ca.get_matches_solo_author(test_string_foreign_characters_capitalization).citations ==\
        ["ULLÉN (1888"]
    
def test_detecting_two_authors():
    test_string_pairs = "One and two (1212) often collaborate. This is well documented (Aesop and Berry, 1999)"
    assert ca.get_matches_two_authors(test_string_pairs).citations ==\
        ["One and two (1212", "Aesop and Berry, 1999"]
    test2 = "(Bennett i Maneval, 1998; "
    assert ca.get_matches_two_authors(test2).citations ==\
        ["Bennett i Maneval, 1998; "]
    foreign_characters_2 = "Mendonça i suradnici (2009) utvrdili su..."
    assert ca.get_matches_two_authors(foreign_characters_2).citations ==\
        ["Mendonça i suradnici (2009"]

def test_detecting_author_et_al():
    test_string_semicolon = "This is the facts (Truth et al., 1980). Also see Hard, 1980; Facts, 1989."
    assert ca.get_matches_author_et_al(test_string_semicolon).citations ==\
        ["Truth et al., 1980"]
    test_croatian_i_sur = "Branjek i suradnici (1999) spominju rad Cvanjek i suradnika (1990) više puta (Dvanjek i sur., 2010)"
    assert ca.get_matches_author_et_al(test_croatian_i_sur).citations ==\
        ["Dvanjek i sur., 2010"]
    

def test_detecting_three_authors():
    test_three_author_citation = "Find Onesie, Twosie and Threeie (2000) enclosed."
    assert ca.get_matches_three_authors(test_three_author_citation).citations ==\
        ["Onesie, Twosie and Threeie (2000"]
    test_two_part_name_caught_by_three_authors = "It's true that Marin Karin and Bro (2000) had a major impact."
    assert ca.get_matches_three_authors(test_two_part_name_caught_by_three_authors).citations ==\
        ["Marin Karin and Bro (2000"]
    test_three_authors_not_recognized_if_not_capitalized = "It's true that marin Karin and Bro (2000) had a major impact."
    assert ca.get_matches_three_authors(test_three_authors_not_recognized_if_not_capitalized).citations == []

def test_detecting_two_surnames():
    text = "U istraživanju Anić Babić (2000) utvrđeno je više stvari."
    assert ca.get_matches_two_surnames(text).citations ==\
        ["Anić Babić (2000"]

def test_detecting_two_surnames_i_suradnika():
    text = "U istraživanju Anić Babić i suradnika (2000) utvrđeno je više stvari."
    # "suradnika" should get recognised as an author name.
    # So we will loosen the restriction on the LAST name in a citation being
    # capitalised. The first two must start with capital letters!
    assert ca.get_matches_three_authors(text).citations ==\
        ["Anić Babić i suradnika (2000"]

def test_detecting_two_surnames_et_al():
    test_string_semicolon = "This is the facts (Naked Truth et al., 1980). Also see Hard, 1980; Facts, 1989."
    assert ca.get_matches_two_surnames_et_al(test_string_semicolon).citations ==\
        ["Naked Truth et al., 1980"]
    test_croatian_i_sur = "Branjek i suradnici (1999) spominju rad Cvanjek i suradnika (1990) više puta (Dvanjek Erin i sur., 2010)"
    assert ca.get_matches_two_surnames_et_al(test_croatian_i_sur).citations ==\
        ["Dvanjek Erin i sur., 2010"]

def test_program_works_with_no_citations_found():
    document = ""
    
    solo_authors = ca.get_matches_solo_author(document, drop_excluded_phrases = True)
    two_authors = ca.get_matches_two_authors(document, drop_excluded_phrases = True)
    three_authors = ca.get_matches_three_authors(document, drop_excluded_phrases = True)
    author_et_al = ca.get_matches_author_et_al(document, drop_excluded_phrases = True)
    two_surnames = ca.get_matches_two_surnames(document, drop_excluded_phrases = True)
    two_surnames_et_al = ca.get_matches_two_surnames_et_al(document, drop_excluded_phrases = True)
        
    solo_authors.delete_clones_of_citations(two_authors)
    
    narrower_citations = ca.CitationType(solo_authors.citations + 
                                      two_authors.citations +
                                      author_et_al.citations)
    
    wider_citations = ca.CitationType(three_authors.citations + 
                                   two_surnames.citations +
                                   two_surnames_et_al.citations)
    
    narrower_citations.cleanup()
    wider_citations.cleanup()
    assert True
    
def test_program_works_when_text_is_all_excluded_phrases():
    document = "A 2019 study founded the, 1999 brightest subjects. Tijekom 2019 bilo je 2020 uzoraka."
    
    solo_authors = ca.get_matches_solo_author(document, drop_excluded_phrases = True)
    two_authors = ca.get_matches_two_authors(document, drop_excluded_phrases = True)
    three_authors = ca.get_matches_three_authors(document, drop_excluded_phrases = True)
    author_et_al = ca.get_matches_author_et_al(document, drop_excluded_phrases = True)
    two_surnames = ca.get_matches_two_surnames(document, drop_excluded_phrases = True)
    two_surnames_et_al = ca.get_matches_two_surnames_et_al(document, drop_excluded_phrases = True)
        
    solo_authors.delete_clones_of_citations(two_authors)
    
    narrower_citations = ca.CitationType(solo_authors.citations + 
                                      two_authors.citations +
                                      author_et_al.citations)
    
    wider_citations = ca.CitationType(three_authors.citations + 
                                   two_surnames.citations +
                                   two_surnames_et_al.citations)
    
    narrower_citations.cleanup()
    wider_citations.cleanup()
    assert True
    
def test_ignore_ISSN():
    text = "Online ISSN 2222-3333"
    citations = ca.get_matches_two_surnames(text, drop_excluded_phrases= True)
    assert citations.citations == []
    
def test_ignore_serial_numbers():
    text_with_long_serial = "Serial Number 123456789"
    assert ca.get_matches_solo_author(text_with_long_serial).citations == []
    # If a number is exactly four digits, it SHOULD get through the filter.
    text_with_short_serial = "Serial Number 1234"
    assert ca.get_matches_solo_author(text_with_short_serial).citations == ["Number 1234"]
    text_with_very_short_serial = "Serial Number 12"
    assert ca.get_matches_solo_author(text_with_very_short_serial).citations == []
    
def test_authors_should_be_capitalised_to_match():
    single_author = "Stayed up all night running 1024 tests. If only I had listened to Testly (2000)."
    assert ca.get_matches_solo_author(single_author).citations == ["Testly (2000"]
    two_authors = "Maybe writing and running 1024 tests a day takes too much time. Maybe yelling and Screaming 2000 times is better (Bogus and Dogus, 3000)."
    assert ca.get_matches_two_authors(two_authors).citations == ["Bogus and Dogus, 3000"]
    # The second name can be lowercase to catch "suradnici".
    
def test_new_foreign_characters():
    text = "Bø (1999) and Yø (2000) and Så (2001)"
    assert ca.get_matches_solo_author(text).citations ==\
        ["Bø (1999", "Yø (2000", "Så (2001"]
    text_non_alphanumeric = "Bø's (1999) research cited Yø-yoma (2000)"
    assert ca.get_matches_solo_author(text_non_alphanumeric).citations ==\
        ["Bø's (1999", "Yø-yoma (2000"]
        
def test_possesive_recognised_and_adjusted():
    possesive_text = "Listen to Cohen's (1999) talk."
    matches = ca.get_matches_solo_author(possesive_text)
    matches.cleanup()
    assert matches.citations == ["Cohen 1999"]
    # When both possesive and regular form are cited, this should result in a single,
    # proper form citation.
    possesive_and_regular = "Listen to Cohen's (1999) talk. Or read Cohen (1999)"
    matches = ca.get_matches_solo_author(possesive_and_regular)
    matches.cleanup()
    assert matches.citations == ["Cohen 1999"]
    
def test_surnames_apostrophe_s_recognised():
    text = "O'Sullivan (2000) wrote a paper. Compare it to O'Samuel's (1999) work."
    matches = ca.get_matches_solo_author(text)
    matches.cleanup()
    assert matches.citations == ["O'Samuel 1999", "O'Sullivan 2000"]
 