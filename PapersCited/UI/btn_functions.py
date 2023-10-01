import UI.fileManipulation as fm
import tkinter as tk
from tkinter import filedialog
import os

# Helper function for raising a pressed button
def fn_btn_release(event, btn):
    btn.config(relief = "raised")
    return("break")


def fn_btn_choose(event, btn_choose, master, data, text_component):
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
        
        text_component.config(state = "normal")
        text_component.delete("1.0", tk.END)
        text_component.insert("1.0", data.active_results)
        text_component.config(state = "disabled")
        return("break")

    data.set_new_results_citations(citations)
    
    master.update_text_widget(data.active_results, replace = True)

    if message:
        master.update_text_widget(message + "\n", position = "start")

    return("break")
