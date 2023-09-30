import tkinter as tk
from tkinter.filedialog import asksaveasfilename
import UI.transformCitations as tc
import UI.messages as ms
import os

class AppData:
    def __init__(self, startup_filename, startup_results):
        self.input_filepath = startup_filename
        self.output_filepath = ""
        self.citations = []
        self.active_results = startup_results
        
        # Options for dynamic trimming of displayed filename
        self.__right_edge_buffer_px = 0
        self.__char_width_px = 6
        
        # What to display when no file chosen:
        self.__no_file_selected_txt = ""
    
    def __calculate_chars_from_width(self, width):
        right_edge_buffer_px = self.__right_edge_buffer_px
        frame_width = width - right_edge_buffer_px
        char_width_px = self.__char_width_px
        label_width_chars = round(frame_width / char_width_px)
        return(label_width_chars)
        
    def set_new_filename(self, filename, list_affected_wg):
        user_filepath = filename
        if user_filepath == "":
            user_filepath = self.__no_file_selected_txt
        
        self.input_filepath = user_filepath
        self.__set_output_filepath()
        
        # Display the document title in main window
        input_filename = os.path.basename(user_filepath)
        
        if input_filename == self.__no_file_selected_txt:
            input_filename = "PapersCited"
        else:
            input_filename = input_filename + " - PapersCited"
        
        for widget in list_affected_wg:
            widget.title(input_filename)
            
    def set_new_results_citations(self, citations, list_affected_wg):
        self.citations = citations
        citations_as_string = tc.citations_to_string_pretty(
            citations[0], citations[1]
        )
        
        if not self.any_citations_recorded():
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
            
    def warning_in_text_widget(self, warning_text, list_affected_wg):
        # Add new text to window, like success messages.
        
        for widget in list_affected_wg:
            widget.config(state = "normal")
            widget.insert('1.0', warning_text + "\n")
            widget.config(state = "disabled")
            widget.see('1.0')
    
    def get_input_filepath(self):
        return(self.input_filepath)
    
    def __set_output_filepath(self):
        # append _citations, no extension
        input = self.get_input_filepath()
        
        # Special case: blank filename when pasting from clipboard
        if input == self.__no_file_selected_txt:
            self.output_filepath = "Citations_found"
            return(None)
        
        output_file_prefix = os.path.splitext(input)
        output_filepath = output_file_prefix[0] + "_citations"
        
        self.output_filepath = output_filepath
        
    def get_output_filepath(self):
        return(self.output_filepath)
    
    def popup_ask_save_file(self, extension):
        output_filepath = self.get_output_filepath()
        given_extension = extension
        
        directory, name = os.path.split(output_filepath)
        
        default_filename = name + given_extension
        
        # Create a tuple matching extension
        filetype = ()
        if given_extension == ".xlsx":
            filetype = ("Excel file", "*.xlsx")
        elif given_extension == ".txt":
            filetype = ("Text file", "*.txt")
            
        user_filename = asksaveasfilename(
            initialfile = default_filename,
            initialdir = directory,
            filetypes = (filetype, ) # Tuple of tuples required, single item requires comma
            )
        
        # Check if user cancelled the action:
        if user_filename == "":
            raise(Exception("Saving cancelled."))
        
        return(user_filename)
    
    def get_citations(self):
        return(self.citations)
    
    def any_citations_recorded(self):
        citations_list = self.get_citations()
        # Return true if appData houses any citations
        if citations_list == []: return(False)
        
        narrow = citations_list[0].citations
        wider = citations_list[1].citations
        
        if len(narrow) > 0 or len(wider) > 0:
            return(True)
        else:
            return(False)
        
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
    