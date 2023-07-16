import citationAnalysis as ca

class AppData:
    def __init__(self, startup_filename, startup_results):
        self.active_filename = startup_filename
        self.citations = []
        self.active_results = startup_results
        
    def set_new_filename(self, filename, list_affected_wg):
        self.active_filename = filename
        for widget in list_affected_wg:
            widget["text"] = self.active_filename
        return("break")
            
    def set_new_results_citations(self, citations, list_affected_wg):
        self.citations = citations
        citations_as_string = ca.citations_to_string(
            citations[0], citations[1]
        )
        self.active_results = citations_as_string
        for widget in list_affected_wg:
            widget["text"] = self.active_results
        return("break")
    
    def get_active_filename(self):
        return(self.active_filename)
    
    def get_citations(self):
        return(self.citations)
    