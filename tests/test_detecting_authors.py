import PapersCited

# The \ indicates code continues in the next line
# When testing individual detection functions, they SHOULD catch extra characters
# between match start and end (first letter of name, last digit/;) 

def test_detecting_single_authors():
    test_string = "Yado (2008) and Hailey (2010) are the Best. 2009 is the final year Worst (2000) spoke of."
    # Best 2009 should not be detected as a citation.
    assert PapersCited.get_matches_solo_author(test_string).citations ==\
        ["Yado (2008", "Hailey (2010", "Worst (2000"]
    test_string_lowercase = "Uppercase (1999) and lowercase (2000) both get detected."
    assert PapersCited.get_matches_solo_author(test_string_lowercase).citations ==\
        ["Uppercase (1999", "lowercase (2000"]
    test_string_semicolon = "This is the facts (Truth, 1980). Also see Hard, 1980; Facts, 1989."
    assert PapersCited.get_matches_solo_author(test_string_semicolon).citations ==\
        ["Truth, 1980", "Hard, 1980;", "Facts, 1989"]
    test_string_and = "Villa and Maria (1875) was the best show ever. Mirko i Birko (1999) napisali su cijelu knjigu o tome."
    # What this function detects WILL NOT be the whole citation. We still need it for controlling two-author matches.
    assert PapersCited.get_matches_solo_author(test_string_and).citations ==\
        ["Maria (1875", "Birko (1999"]
    test_string_many_spaces = "Manman      (1999) really liked his space."
    assert PapersCited.get_matches_solo_author(test_string_many_spaces).citations ==\
        ["Manman      (1999"]
    test_string_foreign_characters_capitalization = "ULLÉN (1888) made an earlier work."
    assert PapersCited.get_matches_solo_author(test_string_foreign_characters_capitalization).citations ==\
        ["ULLÉN (1888"]
    
def test_detecting_two_authors():
    test_string_pairs = "One and two (1212) often collaborate. This is well documented (Aesop and Berry, 1999)"
    assert PapersCited.get_matches_two_authors(test_string_pairs).citations ==\
        ["One and two (1212", "Aesop and Berry, 1999"]
    test2 = "(Bennett i Maneval, 1998; "
    assert PapersCited.get_matches_two_authors(test2).citations ==\
        ["Bennett i Maneval, 1998;"]

def test_detecting_author_et_al():
    test_string_semicolon = "This is the facts (Truth et al., 1980). Also see Hard, 1980; Facts, 1989."
    assert PapersCited.get_matches_author_et_al(test_string_semicolon).citations ==\
        ["Truth et al., 1980"]
    test_croatian_i_sur = "Branjek i suradnici (1999) spominju rad Cvanjek i suradnika (1990) više puta (Dvanjek i sur., 2010)"
    assert PapersCited.get_matches_author_et_al(test_croatian_i_sur).citations ==\
        ["Dvanjek i sur., 2010"]
    

def test_detecting_three_authors():
    test_three_author_citation = "Find Onesie, Twosie and Threeie (2000) enclosed."
    assert PapersCited.get_matches_three_authors(test_three_author_citation).citations ==\
        ["Onesie, Twosie and Threeie (2000"]
    test_two_part_name_caught_by_three_authors = "It's true that Marin Karin and Bro (2000) had a major impact."
    assert PapersCited.get_matches_three_authors(test_two_part_name_caught_by_three_authors).citations ==\
        ["Marin Karin and Bro (2000"]
    test_three_authors_not_recognized_if_not_capitalized = "It's true that marin Karin and Bro (2000) had a major impact."
    assert PapersCited.get_matches_three_authors(test_three_authors_not_recognized_if_not_capitalized).citations == []

def test_detecting_two_surnames():
    text = "U istraživanju Anić Babić (2000) utvrđeno je više stvari."
    assert PapersCited.get_matches_two_surnames(text).citations ==\
        ["Anić Babić (2000"]

def test_detecting_two_surnames_i_suradnika():
    text = "U istraživanju Anić Babić i suradnika (2000) utvrđeno je više stvari."
    # "suradnika" should get recognised as an author name.
    # So we will loosen the restriction on the LAST name in a citation being
    # capitalised. The first two must start with capital letters!
    assert PapersCited.get_matches_three_authors(text).citations ==\
        ["Anić Babić i suradnika (2000"]

def test_detecting_two_surnames_et_al():
        test_string_semicolon = "This is the facts (Naked Truth et al., 1980). Also see Hard, 1980; Facts, 1989."
        assert PapersCited.get_matches_two_surnames_et_al(test_string_semicolon).citations ==\
            ["Naked Truth et al., 1980"]
        test_croatian_i_sur = "Branjek i suradnici (1999) spominju rad Cvanjek i suradnika (1990) više puta (Dvanjek Erin i sur., 2010)"
        assert PapersCited.get_matches_two_surnames_et_al(test_croatian_i_sur).citations ==\
            ["Dvanjek Erin i sur., 2010"]

def test_program_works_with_no_citations_found():
    document = ""
    
    solo_authors = PapersCited.get_matches_solo_author(document, drop_excluded_phrases = True)
    two_authors = PapersCited.get_matches_two_authors(document, drop_excluded_phrases = True)
    three_authors = PapersCited.get_matches_three_authors(document, drop_excluded_phrases = True)
    author_et_al = PapersCited.get_matches_author_et_al(document, drop_excluded_phrases = True)
    two_surnames = PapersCited.get_matches_two_surnames(document, drop_excluded_phrases = True)
    two_surnames_et_al = PapersCited.get_matches_two_surnames_et_al(document, drop_excluded_phrases = True)
        
    solo_authors.delete_clones_of_citations(two_authors)
    
    narrower_citations = PapersCited.CitationType(solo_authors.citations + 
                                      two_authors.citations +
                                      author_et_al.citations)
    
    wider_citations = PapersCited.CitationType(three_authors.citations + 
                                   two_surnames.citations +
                                   two_surnames_et_al.citations)
    
    narrower_citations.cleanup()
    wider_citations.cleanup()
    assert True
    
def test_program_works_when_text_is_all_excluded_phrases():
    document = "A 2019 study founded the, 1999 brightest subjects. Tijekom 2019 bilo je 2020 uzoraka."
    
    solo_authors = PapersCited.get_matches_solo_author(document, drop_excluded_phrases = True)
    two_authors = PapersCited.get_matches_two_authors(document, drop_excluded_phrases = True)
    three_authors = PapersCited.get_matches_three_authors(document, drop_excluded_phrases = True)
    author_et_al = PapersCited.get_matches_author_et_al(document, drop_excluded_phrases = True)
    two_surnames = PapersCited.get_matches_two_surnames(document, drop_excluded_phrases = True)
    two_surnames_et_al = PapersCited.get_matches_two_surnames_et_al(document, drop_excluded_phrases = True)
        
    solo_authors.delete_clones_of_citations(two_authors)
    
    narrower_citations = PapersCited.CitationType(solo_authors.citations + 
                                      two_authors.citations +
                                      author_et_al.citations)
    
    wider_citations = PapersCited.CitationType(three_authors.citations + 
                                   two_surnames.citations +
                                   two_surnames_et_al.citations)
    
    narrower_citations.cleanup()
    wider_citations.cleanup()
    assert True
    
def test_ignore_ISSN():
    text = "Online ISSN 2222-3333"
    citations = PapersCited.get_matches_two_surnames(text, drop_excluded_phrases= True)
    assert citations.citations == []