import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import UI.fileManipulation as fm
import UI.messages as ms
from UI.appData import AppData

# Variables ----
light_yellow = "#ffe08f"

startup_filename = ".../path/to/file"
startup_results = "Results will be shown here..."

app_data = AppData(startup_filename, startup_results)

# Build UI parts ----

main_window = tk.Tk()
main_window.columnconfigure(0, weight = 0, minsize = 50)
main_window.columnconfigure(1, weight = 1, minsize = 100)
main_window.rowconfigure(0, weight = 0, minsize = 30)
main_window.rowconfigure(1, weight = 2, minsize = 400)
main_window.rowconfigure(2, weight = 0, minsize = 30)

main_window.minsize(750, 500)

btn_choose = tk.Button(master = main_window,
                        text = "Analyse document",
                        borderwidth = 3, relief=tk.RAISED,
                        padx = 8, pady = 5
                        )

btn_choose.grid(row = 0, column = 0, sticky = "NW", padx = 10, pady = 5)

# TODO Make filepath and contents gray when nothing is selected

fr_current_file = tk.Frame(master = main_window, bg = light_yellow)
fr_current_file.grid(row = 0, column = 1, columnspan = 3, sticky = "NWES",
                      padx = 10, pady = 5)

lbl_current_file = tk.Label(master = fr_current_file,
                            text = app_data.active_filename, bg = light_yellow,
                            pady = 3)

lbl_current_file.grid(row = 0, column = 0, sticky = "W", padx = 5, pady = 5)

fr_results = tk.Frame(master = main_window, bg = "white",
                      borderwidth = 2, relief = tk.GROOVE)
fr_results.grid(row = 1, column = 0, sticky = "NWSE", columnspan = 4,
                 padx = 10)

fr_results.columnconfigure(0, weight = 1)
fr_results.columnconfigure(1, weight = 0)
fr_results.rowconfigure(0, weight = 1)

scr_results = tk.Scrollbar(fr_results, orient = "vertical")
scr_results.grid(row = 0, column = 1, sticky = "NS")

txt_results = tk.Text(master = fr_results, bg = "white", yscrollcommand = scr_results.set)
txt_results.insert(tk.END, app_data.active_results)

scr_results.config(command=txt_results.yview)

txt_results.config(state = "normal")
txt_results.grid(row = 0, column = 0, sticky="NSWE")
txt_results.config(state = "disabled")

btn_save_xlsx = tk.Button(master = main_window,
                          text = "Save as .xlsx",
                        borderwidth = 2,
                        padx = 5, pady = 5)

btn_save_xlsx.grid(row = 2, column = 2, sticky = "SE",
                        padx = 10, pady = 5)

btn_save_txt = tk.Button(master = main_window,
                          text = "Save as .txt",
                        borderwidth = 2,
                        padx = 5, pady = 5)

btn_save_txt.grid(row = 2, column = 3, sticky = "SE",
                        padx = 10, pady = 5)

main_window.title("PapersCited")

# Bind functions ----

# Helper to return buttons to rest state after a click
def fn_btn_release(event, btn):
  btn.config(relief = "raised")
  return("break")

def fn_btn_choose(event):
  btn_choose.config(relief = "sunken")
  filename = filedialog.askopenfilename(
    title = "Select a document to search for citations:"
    )
  app_data.set_new_filename(filename,
                            list_affected_wg=[lbl_current_file],
                            frame = fr_current_file)
  try:
    citations = fm.find_citations(filename)
 
  except Exception as e:
    error = str(e)
    app_data.reset_on_error(error, list_affected_wg = [txt_results])
    return("break")
  
  app_data.set_new_results_citations(citations,
                                     list_affected_wg = [txt_results])
  
  return("break")

btn_choose.bind("<Button-1>", fn_btn_choose)
btn_choose.bind("<ButtonRelease>", lambda event, btn = btn_choose: fn_btn_release(event, btn))

def fn_btn_save_excel(event):
  btn_save_xlsx.config(relief = "sunken")
  citations = app_data.get_citations()
  
  if not app_data.any_citations_recorded():
    app_data.reset_on_error(ms.no_citations_to_save, list_affected_wg = [txt_results])
    return("break")
  
  doc_filename = app_data.get_active_filename()
  try:
    message = fm.write_excel(doc_filename,
                 citations[0], citations[1])
  except Exception as e:
    error = str(e)
    app_data.reset_on_error(error, list_affected_wg = [txt_results])
    return("break")
  
  app_data.update_text_widget(message,
                          list_affected_wg = [txt_results])
  return("break")
  
btn_save_xlsx.bind("<Button-1>", fn_btn_save_excel)  
btn_save_xlsx.bind("<ButtonRelease>", lambda event, btn = btn_save_xlsx: fn_btn_release(event, btn))
 
def fn_btn_save_txt(event):
  btn_save_txt.config(relief = "sunken")
  citations = app_data.get_citations()
  
  if not app_data.any_citations_recorded():
    app_data.reset_on_error(ms.no_citations_to_save, list_affected_wg = [txt_results])
    return("break")
  
  doc_filename = app_data.get_active_filename()
  try:
    message = fm.write_txt(doc_filename,
                 citations[0], citations[1])
  except Exception as e:
    error = str(e)
    app_data.reset_on_error(error, list_affected_wg = [txt_results])
    return("break")
  
  app_data.update_text_widget(message,
                          list_affected_wg = [txt_results])
  return("break")
      
btn_save_txt.bind("<Button-1>", fn_btn_save_txt) 
btn_save_txt.bind("<ButtonRelease>", lambda event, btn = btn_save_txt: fn_btn_release(event, btn))


# On resize, re-render the filename display
def fn_window_resize(event):
  app_data.update_filename_display(
                            list_affected_wg=[lbl_current_file],
                            frame = fr_current_file
                            )
  
main_window.bind("<Configure>", fn_window_resize)