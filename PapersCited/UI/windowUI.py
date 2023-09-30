import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import UI.fileManipulation as fm
import UI.messages as ms
from UI.messages import version
from UI.appData import AppData

# Variables ----

light_yellow = "#ffe08f"

startup_filename = ".../path/to/file"
startup_results = ms.intro_message

citations_font = "Segoe UI Variable"
citations_font_size = 11

app_data = AppData(startup_filename, startup_results)

# Build UI parts ----

main_window = tk.Tk()
main_window.columnconfigure(0, weight = 0, minsize = 50)
main_window.columnconfigure(1, weight = 0, minsize = 50)
main_window.columnconfigure(2, weight = 0, minsize = 20)
main_window.columnconfigure(3, weight = 1, minsize = 100)
main_window.rowconfigure(0, weight = 0, minsize = 30)
main_window.rowconfigure(1, weight = 2, minsize = 400)
main_window.rowconfigure(2, weight = 0, minsize = 30)

main_window.minsize(750, 500)

btn_choose = tk.Button(master = main_window,
                        text = "Choose document",
                        borderwidth = 3, relief=tk.RAISED,
                        padx = 8, pady = 5
                        )

btn_choose.grid(row = 0, column = 0, sticky = "NW", padx = 10, pady = 5)

btn_from_clipboard = tk.Button(master = main_window,
                        text = "From clipboard",
                        borderwidth = 3, relief=tk.RAISED,
                        padx = 8, pady = 5
                        )

btn_from_clipboard.grid(row = 0, column = 1, sticky = "NW", padx = 5, pady = 5)


fr_current_file = tk.Frame(master = main_window, bg = light_yellow)
fr_current_file.grid(row = 0, column = 3, columnspan = 2, sticky = "NWES",
                      padx = 10, pady = 5)

lbl_current_file = tk.Label(master = fr_current_file,
                            text = app_data.input_filename, bg = light_yellow,
                            pady = 3)

lbl_current_file.grid(row = 0, column = 0, sticky = "W", padx = 5, pady = 5)

fr_results = tk.Frame(master = main_window, bg = "white",
                      borderwidth = 2, relief = tk.GROOVE)
fr_results.grid(row = 1, column = 0, sticky = "NWSE", columnspan = 5,
                 padx = 10)

fr_results.columnconfigure(0, weight = 1)
fr_results.columnconfigure(1, weight = 0)
fr_results.rowconfigure(0, weight = 1)

scr_results = tk.Scrollbar(fr_results, orient = "vertical")
scr_results.grid(row = 0, column = 1, sticky = "NS")

txt_results = tk.Text(master = fr_results, bg = "white", yscrollcommand = scr_results.set, wrap = tk.WORD)
txt_results.configure(font = (citations_font, citations_font_size))
txt_results.insert(tk.END, app_data.active_results)

scr_results.config(command=txt_results.yview)

txt_results.config(state = "normal")
txt_results.grid(row = 0, column = 0, sticky="NSWE")
txt_results.config(state = "disabled")

btn_save_xlsx = tk.Button(master = main_window,
                          text = "Save as .xlsx",
                        borderwidth = 2,
                        padx = 5, pady = 5)

btn_save_xlsx.grid(row = 2, column = 3, sticky = "SE",
                        padx = 10, pady = 5)

btn_save_txt = tk.Button(master = main_window,
                          text = "Save as .txt",
                        borderwidth = 2,
                        padx = 5, pady = 5)

btn_save_txt.grid(row = 2, column = 4, sticky = "SE",
                        padx = 10, pady = 5)

main_window.title("PapersCited " + version)

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
    reading_operation = fm.read_document(filename)
    
    message = reading_operation["status_message"]
    contents = reading_operation["document_text"]
    citations = fm.find_citations(contents)
 
  except Exception as e:
    error = str(e)
    app_data.reset_on_error(error, list_affected_wg = [txt_results])
    return("break")
  
  app_data.set_new_results_citations(citations,
                                     list_affected_wg = [txt_results])
  
  if message:
    app_data.warning_in_text_widget(message, list_affected_wg = [txt_results])
  
  return("break")

btn_choose.bind("<Button-1>", fn_btn_choose)
btn_choose.bind("<ButtonRelease>", lambda event, btn = btn_choose: fn_btn_release(event, btn))

# Reading from clipboard
def fn_from_clipboard(event):
  btn_from_clipboard.config(relief = "sunken")

  # clipboard_get() errors when clipboard is empty
  try:
    clipboard_text = main_window.clipboard_get()
  
  except Exception as e:
    clipboard_text = ""
  
  app_data.set_new_filename(filename = "",
                            list_affected_wg=[lbl_current_file],
                            frame = fr_current_file)
  try:
    message = None
    citations = fm.find_citations(clipboard_text)
 
  except Exception as e:
    error = str(e)
    app_data.reset_on_error(error, list_affected_wg = [txt_results])
    return("break")
  
  app_data.set_new_results_citations(citations,
                                     list_affected_wg = [txt_results])
  
  if message:
    app_data.warning_in_text_widget(message, list_affected_wg = [txt_results])
  
  return("break")

btn_from_clipboard.bind("<Button-1>", fn_from_clipboard)
btn_from_clipboard.bind("<ButtonRelease>", lambda event, btn = btn_from_clipboard: fn_btn_release(event, btn))

def fn_btn_save_excel(event):
  btn_save_xlsx.config(relief = "sunken")
  citations = app_data.get_citations()
  
  if not app_data.any_citations_recorded():
    app_data.reset_on_error(ms.no_citations_to_save, list_affected_wg = [txt_results])
    return("break")
  
  # Ask user where to save, notify if cancelled
  try:
    doc_filename = app_data.popup_ask_save_file(".xlsx")
  except Exception as e:
    app_data.update_text_widget(ms.saving_cancelled,
                          list_affected_wg = [txt_results])
    return("break")
  
  try:
    message = fm.write_excel(doc_filename,
                 citations[0], citations[1])
  except Exception as e:
    error = str(e)
    app_data.reset_on_error(ms.cant_write_file(doc_filename) + f"\n\n{error}",
                            list_affected_wg = [txt_results])
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
  
  # Ask user where to save, notify if cancelled
  try:
    doc_filename = app_data.popup_ask_save_file(".txt")
  except Exception as e:
    app_data.update_text_widget(ms.saving_cancelled,
                          list_affected_wg = [txt_results])
    return("break")
  
  try:
    message = fm.write_txt(doc_filename,
                 citations[0], citations[1])
  except Exception as e:
    error = str(e)
    app_data.reset_on_error(ms.cant_write_file(doc_filename) + f"\n\n{error}",
                            list_affected_wg = [txt_results])
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

# Right-click menu for copying citations
rc_menu = tk.Menu(main_window, tearoff = 0)

def popup_menu(event):
  try: 
    rc_menu.tk_popup(event.x_root, event.y_root)
  finally:
    rc_menu.grab_release()

# Note - a menu command must NOT have event argument
def copy_to_clipboard():
  main_window.clipboard_clear()
  
  try: 
    selected_text = txt_results.get(tk.SEL_FIRST, tk.SEL_LAST)
  except:
    # In case the main window/selection is empty, there's no SEL_FIRST
    selected_text = ""
    
  main_window.clipboard_append(selected_text)

rc_menu.add_command(label = "Copy", command = copy_to_clipboard)
  
# Bind only to results pane, copying not important for other parts    
txt_results.bind("<Button-3>", popup_menu)

# Create an icon for the main window
PC_icon = tk.PhotoImage(file = "UI/miniicon.png")
main_window.iconphoto(True, PC_icon)