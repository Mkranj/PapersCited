from UI.appData import AppData
from citationAnalysis.citationAnalysis import CitationType

def test_checking_for_empty_citation_list():
    narrow_empty = CitationType([])
    narrow_full = CitationType(["First 2010", "Second 2020"])
    wide_empty = CitationType([])
    wide_full = CitationType(["First Second and Third 2010", "Even More and Authors 2020"])
    
    appdata = AppData("", "")
    
    appdata.set_new_results_citations([narrow_empty, wide_empty], list_affected_wg=[])
    assert appdata.any_citations_recorded() == False
    
    appdata.set_new_results_citations([narrow_full, wide_empty], list_affected_wg=[])
    assert appdata.any_citations_recorded() == True
    
    appdata.set_new_results_citations([narrow_empty, wide_full], list_affected_wg=[])
    assert appdata.any_citations_recorded() == True
    
    appdata.set_new_results_citations([narrow_full, wide_full], list_affected_wg=[])
    assert appdata.any_citations_recorded() == True
    