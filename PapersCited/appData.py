import tkinter as tk
import citationAnalysis as ca
from fileManipulation import shorten_filename

class AppData:
    def __init__(self, startup_filename, startup_results):
        self.active_filename = startup_filename
        self.citations = []
        self.active_results = startup_results
        
    def set_new_filename(self, filename, list_affected_wg, length_display = 110):
        self.active_filename = filename
        for widget in list_affected_wg:
            widget["text"] = shorten_filename(self.active_filename, length_display)
        
            
    def set_new_results_citations(self, citations, list_affected_wg):
        self.citations = citations
        citations_as_string = ca.citations_to_string(
            citations[0], citations[1]
        )
        self.active_results = citations_as_string
        for widget in list_affected_wg:
            widget.config(state = "normal")
            widget.delete("1.0", tk.END)
            widget.insert("1.0", self.active_results)
            widget.config(state = "disabled")
    
    def update_results(self, update_text, list_affected_wg):
        # Add new text to window, like success messages.
        
        for widget in list_affected_wg:
            widget.config(state = "normal")
            widget.insert(tk.END, update_text)
            widget.config(state = "disabled")
    
    def get_active_filename(self):
        return(self.active_filename)
    
    def get_citations(self):
        return(self.citations)
    