from modules.fileManipulation import shorten_filename
from modules.fileManipulation import any_citations_recorded
from modules.citationAnalysis import CitationType

def test_shortening_names():
    short_name = "aeiou"
    long_name = "0123456789" + "0123456789" + "0123456789" + "0123456789" + "0123456789"
    
    assert shorten_filename(short_name) == short_name
    assert shorten_filename(short_name, 4) == "a..."
    assert shorten_filename(short_name, 5) == short_name
    
    assert shorten_filename(long_name, 50) == long_name
    assert shorten_filename(long_name, 5) == "01..."
    assert shorten_filename(long_name, 10) == "0123456..."
    
def test_checking_for_empty_citation_list():
    narrow_empty = CitationType([])
    narrow_full = CitationType(["First 2010", "Second 2020"])
    wide_empty = CitationType([])
    wide_full = CitationType(["First Second and Third 2010", "Even More and Authors 2020"])
    
    assert any_citations_recorded([]) == False
    
    assert any_citations_recorded([narrow_empty, wide_empty]) == False
    
    assert any_citations_recorded([narrow_full, wide_empty]) == True
    assert any_citations_recorded([narrow_empty, wide_full]) == True
    assert any_citations_recorded([narrow_full, wide_full]) == True