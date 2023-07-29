import tkinter as tk
import UI.transformCitations as tc
import UI.messages as ms
from UI.fileManipulation import shorten_filename
from UI.fileManipulation import any_citations_recorded

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
        citations_as_string = tc.citations_to_string_pretty(
            citations[0], citations[1]
        )
        
        if not any_citations_recorded(citations):
            citations_as_string = ms.no_citations_found
        
        self.active_results = citations_as_string
        for widget in list_affected_wg:
            widget.config(state = "normal")
            widget.delete("1.0", tk.END)
            widget.insert("1.0", self.active_results)
            widget.config(state = "disabled")
    
    def update_text_widget(self, update_text, list_affected_wg):
        # Add new text to window, like success messages.
        
        for widget in list_affected_wg:
            widget.config(state = "normal")
            widget.insert(tk.END, update_text)
            widget.config(state = "disabled")
            widget.see(tk.END)
    
    def get_active_filename(self):
        return(self.active_filename)
    
    def get_citations(self):
        return(self.citations)
    
    def get_active_results(self):
        return(self.active_results)
    
    def reset_on_error(self, error, list_affected_wg):
        # Failing to read a file should clear the textbox and
        # the stored citations
        self.citations = []
        self.active_results = error
        for widget in list_affected_wg:
            widget.config(state = "normal")
            widget.delete("1.0", tk.END)
            widget.insert("1.0", self.active_results)
            widget.config(state = "disabled")
    