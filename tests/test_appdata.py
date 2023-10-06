from UI.appData import AppData
from citationAnalysis.citationAnalysis import CitationType
import os

def test_checking_for_empty_citation_list():
    narrow_empty = CitationType([])
    narrow_full = CitationType(["First 2010", "Second 2020"])
    wide_empty = CitationType([])
    wide_full = CitationType(["First Second and Third 2010", "Even More and Authors 2020"])
    
    appdata = AppData("", "")
    
    appdata.set_new_results_citations([narrow_empty, wide_empty])
    assert appdata.any_citations_recorded() == False
    
    appdata.set_new_results_citations([narrow_full, wide_empty])
    assert appdata.any_citations_recorded() == True
    
    appdata.set_new_results_citations([narrow_empty, wide_full])
    assert appdata.any_citations_recorded() == True
    
    appdata.set_new_results_citations([narrow_full, wide_full])
    assert appdata.any_citations_recorded() == True
    
def test_input_filepath_stored():
    appdata = AppData("", "")
    
    filename = os.path.abspath("C:/User/Documents/my_text.txt")
    
    appdata.set_new_filename(filename)
    assert appdata.get_input_filepath() == filename
    
def test_input_filepath_with_relevant_output_filename():
    appdata = AppData("", "")
    
    filename = os.path.abspath("C:/User/Documents/my_text.txt")
    
    # The output shouldn't have an extension - that is decided when users
    # chooses what kind of file to save as
    desired_default_output_filepath = os.path.abspath("C:/User/Documents/my_text_citations")
    
    appdata.set_new_filename(filename)
    assert appdata.get_output_filepath() == desired_default_output_filepath
    
def test_input_no_filepath_is_blank():
    appdata = AppData("", "")
      
    appdata.set_new_filename("")
    assert appdata.get_input_filepath() == ""
    
def test_input_no_filepath_output_file_called_citations_found():
    appdata = AppData("", "")
      
    appdata.set_new_filename("")
    assert appdata.get_output_filepath() == "Citations_found"
    
def test_startup_text_reflected_in_results():
    startup_text = "Howdy"
    appdata = AppData("", startup_text)
      
    assert appdata.get_active_results() == startup_text
    
def test_result_on_error_no_citations_records_error():
    startup_text = "Howdy"
    appdata = AppData("", startup_text)
      
    error_text = "My error"  
    appdata.reset_on_error(error_text)  
      
    assert appdata.get_active_results() == error_text
    assert appdata.get_citations() == []
    
    # Store some citations, then cleanup on error should empty them
    narrow_citations = CitationType(["First 2010", "Second 2020"])
    wide_citations_none = CitationType([])
    appdata.set_new_results_citations([narrow_citations, wide_citations_none])
    
    assert appdata.get_citations != []
    assert appdata.get_active_results != error_text
    
    appdata.reset_on_error(error_text)
    
    assert appdata.get_active_results() == error_text
    assert appdata.get_citations() == []