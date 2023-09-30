import tkinter as tk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import UI.fileManipulation as fm
import UI.messages as ms
from UI.messages import version
from UI.appData import AppData

# Variables ----

light_yellow = "#ffe08f"

startup_filename = ""
startup_results = ms.intro_message

citations_font = "Segoe UI Variable"
citations_font_size = 11

app_data = AppData(startup_filename, startup_results)

class main_window(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("PapersCited")
        self.minsize(750, 500)
        
        self.columnconfigure(0, weight = 0, minsize = 50)
        self.columnconfigure(1, weight = 0, minsize = 50)
        self.columnconfigure(2, weight = 0, minsize = 20)
        self.columnconfigure(3, weight = 1, minsize = 100)
        self.rowconfigure(0, weight = 0, minsize = 30)
        self.rowconfigure(1, weight = 2, minsize = 400)
        self.rowconfigure(2, weight = 0, minsize = 30)
        
        self.data = app_data
        self.create_widgets()
        
    def create_widgets(self):
        # Sets up individual UI elements
        self.btn_choose = btnChoose(self).get()
        self.__build_btn_from_clipboard()
        self.ui_results = uiResults(self).get()
        self.__build_save_excel()
        self.__build_save_text()
        
    def __build_btn_from_clipboard(self):
        btn_from_clipboard = tk.Button(master = self,
                        text = "From clipboard",
                        borderwidth = 3, relief=tk.RAISED,
                        padx = 8, pady = 5
                        )

        btn_from_clipboard.grid(row = 0, column = 1, sticky = "NW", padx = 5, pady = 5)
        
    def __build_save_excel(self):
        btn_save_xlsx = tk.Button(master = self,
                          text = "Save as .xlsx",
                        borderwidth = 2,
                        padx = 5, pady = 5)

        btn_save_xlsx.grid(row = 2, column = 3, sticky = "SE",
                        padx = 10, pady = 5)
        
    def __build_save_text(self):
        btn_save_txt = tk.Button(master = self,
                          text = "Save as .txt",
                        borderwidth = 2,
                        padx = 5, pady = 5)

        btn_save_txt.grid(row = 2, column = 4, sticky = "SE",
                        padx = 10, pady = 5)

# Helper to return buttons to rest state after a click
def fn_btn_release(event, btn):
  btn.config(relief="raised")
  return("break")

# Individual components and their bindings
        
class btnChoose():
    def __init__(self, master):
        self.master = master

        btn_choose = tk.Button(master = self.master,
                        text = "Choose document",
                        borderwidth = 3, relief=tk.RAISED,
                        padx = 8, pady = 5
                        )

        btn_choose.grid(row = 0, column = 0, sticky = "NW", padx = 10, pady = 5)
        
        self.UI = btn_choose
        
    def on_click(self, event):
        
        self.UI.config(relief="sunken")
        
        filename = filedialog.askopenfilename(
            title = "Select a document to search for citations:"
            )
        app_data.set_new_filename(filename,
                                    list_affected_wg=[self.master])
        try:
            reading_operation = fm.read_document(filename)
            
            message = reading_operation["status_message"]
            contents = reading_operation["document_text"]
            citations = fm.find_citations(contents)
        
        except Exception as e:
            error = str(e)
            app_data.reset_on_error(error, list_affected_wg = [self.master.ui_results])
            return("break")
        
        app_data.set_new_results_citations(citations,
                                            list_affected_wg = [self.master.ui_results])
        
        if message:
            app_data.warning_in_text_widget(message, list_affected_wg = [self.master.ui_results])
        
        return("break")
        
    def get(self):
        output_component = self.UI
        output_component.bind("<Button-1>", self.on_click)
        output_component.bind("<ButtonRelease>", lambda event,
                        btn=output_component: fn_btn_release(event, btn))
        return(output_component)    
    

class uiResults():
    def __init__(self, master):
        self.master = master

        # Frame element
        fr_results = tk.Frame(master=master, bg="white",
                              borderwidth=2, relief=tk.GROOVE)
        fr_results.grid(row=1, column=0, sticky="NWSE", columnspan=5,
                        padx=10)

        fr_results.columnconfigure(0, weight=1)
        fr_results.columnconfigure(1, weight=0)
        fr_results.rowconfigure(0, weight=1)

        # Scrollbar element
        scr_results = tk.Scrollbar(fr_results, orient="vertical")
        scr_results.grid(row=0, column=1, sticky="NS")

        # Text field element
        txt_results = tk.Text(master=fr_results, bg="white",
                              yscrollcommand=scr_results.set, wrap=tk.WORD)
        txt_results.configure(font=(citations_font, citations_font_size))
        txt_results.insert(tk.END, app_data.active_results)

        scr_results.config(command=txt_results.yview)

        txt_results.config(state="normal")
        txt_results.grid(row=0, column=0, sticky="NSWE")
        txt_results.config(state="disabled")

        self.UI = txt_results

    def get(self):
        output_component = self.UI
        return(output_component)
