# Individual functions that are meant to be bound to UI elements when clicked.
import UI.fileManipulation as fm
import tkinter as tk
from tkinter import filedialog
import os

def fn_btn_release(event, btn):
    """Helper function for raising a pressed button

    Args:
        event (event): UI event
        btn (tk.Button): Button for which to apply de-pressing. Should be the same one the bind method is called on.
    """
    btn.config(relief = "raised")
    return("break")


def fn_btn_choose(event, btn_choose, master, data):
    """Clicking on Choose document button
    
    A popup for choosing a file appears. The chosen filepath is stored in application data. The filename is reflected
    in the program title bar, and the file contents are scanned for citations.

    Args:
        event (event): UI event
        btn_choose (tk.Button): The button this function should be bound to.
        master (main_window): The master window.
        data (AppData): Application data belonging to master.
    """
    btn_choose.config(relief="sunken")
    
    filepath = filedialog.askopenfilename(
        title="Select a document to search for citations:"
    )
    
    data.set_new_filename(filepath)
  
    # Display the document title in main window
    input_filename = os.path.basename(filepath)

    if input_filename == "":
        input_filename = "PapersCited"
    else:
        input_filename = input_filename + " - PapersCited"

    master.title(input_filename)
    
    # Read document text and find citations
    try:
        reading_operation = fm.read_document(filepath)

        message = reading_operation["status_message"]
        contents = reading_operation["document_text"]
        citations = fm.find_citations(contents)

    except Exception as e:
        # Failure to read file
        error = str(e)
        
        data.reset_on_error(error)
        
        master.update_text_widget(data.active_results, replace = True)
        return("break")

    data.set_new_results_citations(citations)
    
    master.update_text_widget(data.active_results, replace = True)

    if message:
        master.update_text_widget(message + "\n", position = "start")

    return("break")
