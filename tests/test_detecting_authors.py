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

def test_detecting_author_et_al():
    test_string_semicolon = "This is the facts (Truth et al., 1980). Also see Hard, 1980; Facts, 1989."
    assert PapersCited.get_matches_author_et_al(test_string_semicolon).citations ==\
        ["Truth et al., 1980"]

def test_detecting_three_authors():
    test_three_author_citation = "Find Onesie, Twosie and Threeie (2000) enclosed."
    assert PapersCited.get_matches_three_authors(test_three_author_citation).citations ==\
        ["Onesie, Twosie and Threeie (2000"]
    test_two_part_name_caught_by_three_authors = "It's true that Marin Karin and Bro (2000) had a major impact."
    assert PapersCited.get_matches_three_authors(test_two_part_name_caught_by_three_authors).citations ==\
        ["Marin Karin and Bro (2000"]
    test_three_authors_not_recognized_if_not_capitalized = "It's true that marin Karin and Bro (2000) had a major impact."
    assert PapersCited.get_matches_three_authors(test_three_authors_not_recognized_if_not_capitalized).citations == []

def test_detect_all_in_text():
    pass
