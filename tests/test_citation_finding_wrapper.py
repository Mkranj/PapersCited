# Tests the wrapper which handles all existing fns related to finding citations in text, organising the output
# so there are no duplicates, removing extraneous characters etc. This is what happens when you click the "Analyse document" button.
# Lower level fns tested in test_individual_citation_fns.
from UI.fileManipulation import find_citations

def test_find_citations_wrapper():
    text = "One and two (1212) often collaborate. This is well documented (Aesop and Berry, 1999). Aasimov (1999) had a revelation (Bassimov, 2000). Long Surname (2020) found his match."
    
    # Specifying sought-after matches. Berry, 1999 is a side-effect not considered harmful.
    expected_narrow = ["Aasimov 1999", "Bassimov 2000", "Aesop & Berry 1999", "One & two 1212"]
    expected_wider = ["Long Surname 2020"]
    
    found_citations = find_citations(text)
    assert all([citation in found_citations[0].citations for citation in expected_narrow])
    assert all([citation in found_citations[1].citations for citation in expected_wider])