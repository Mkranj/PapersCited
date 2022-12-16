import PapersCited

# The \ indicates code continues in the next line
# When testing single detection functions, they SHOULD catch extra characters
# between match start and end (first letter of name, last digit/;) 

def test_detecting_single_authors():
    test_string = "Yado (2008) and Hailey (2010) are the Best. 2009 is the final year Worst (2000) spoke of."
    # Best 2009 should not be detected as a citation.
    assert PapersCited.get_matches_solo_author(test_string) ==\
        ["Yado (2008", "Hailey (2010", "Worst (2000"]
    test_string_lowercase = "Uppercase (1999) and lowercase (2000) both get detected."
    assert PapersCited.get_matches_solo_author(test_string_lowercase) ==\
        ["Uppercase (1999", "lowercase (2000"]
    test_string_semicolon = "This is the facts (Truth, 1980). Also see Hard, 1980; Facts, 1989."
    assert PapersCited.get_matches_solo_author(test_string_semicolon) ==\
        ["Truth, 1980", "Hard, 1980;", "Facts, 1989"]
    test_string_and = "Villa and Maria (1875) was the best show ever. Mirko i Birko (1999) napisali su cijelu knjigu o tome."
    # What this function detects WILL NOT be the whole citation. We still need it for controlling two-author matches.
    assert PapersCited.get_matches_solo_author(test_string_and) ==\
        ["Maria (1875", "Birko (1999"]
    
def test_detecting_two_authors():
    pass

def test_detecting_author_et_al():
    test_string_semicolon = "This is the facts (Truth et al., 1980). Also see Hard, 1980; Facts, 1989."
    assert PapersCited.get_matches_author_et_al(test_string_semicolon) ==\
        ["Truth et al., 1980"]


def test_second_in_two_authors():
    pass

def test_detecting_three_authors():
    pass

def test_detect_all_in_text():
    pass

def test_filtering_filler_phrases():
    # If something gets detected as first of two authors, but is a filler word,
    # Ensure that the second author, the actual one, is NOT deleted from the list!
    # I believe this currently DOES NOT happen!
    pass

def test_sorting_lists():
    pass
