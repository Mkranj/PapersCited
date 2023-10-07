import citationAnalysis.citationAnalysis as ca
import UI.transformCitations as tc
import regex

def test_citations_to_string_pretty_includes_all():
    narrow_citations = ca.CitationType(["Aaron 2010", "Baron 2020"])
    wide_citations = ca.CitationType(["Carron 2030"])
    
    stringified = tc.citations_to_string_pretty(narrow_citations, wide_citations)
    
    # The result is a string
    assert isinstance(stringified, str)
    
    matches = [regex.search(citation, stringified) is not None for citation in narrow_citations.citations + wide_citations.citations]
    assert all(matches)
    
    