import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import PapersCited as pc
from appData import AppData

# Variables ----
light_yellow = "#ffe08f"

startup_filename = ".../path/to/file"
startup_results = "Results will be shown here..."

app_data = AppData(startup_filename, startup_results)

# UI functions ----

def analyse_file(filename):
  pc.check_file(filename)
  document = pc.read_document(filename)
  
  # Get all types of citations
  solo_authors = pc.get_matches_solo_author(document, drop_excluded_phrases = True)
  two_authors = pc.get_matches_two_authors(document, drop_excluded_phrases = True)
  three_authors = pc.get_matches_three_authors(document, drop_excluded_phrases = True)
  author_et_al = pc.get_matches_author_et_al(document, drop_excluded_phrases = True)
  two_surnames = pc.get_matches_two_surnames(document, drop_excluded_phrases = True)
  two_surnames_et_al = pc.get_matches_two_surnames_et_al(document, drop_excluded_phrases = True)
      
  solo_authors.delete_clones_of_citations(two_authors)
  
  narrower_citations = pc.CitationType(solo_authors.citations + 
                                    two_authors.citations +
                                    author_et_al.citations)
  
  wider_citations = pc.CitationType(three_authors.citations + 
                                  two_surnames.citations +
                                  two_surnames_et_al.citations)
  
  narrower_citations.cleanup()
  wider_citations.cleanup()
  
  return([narrower_citations, wider_citations])

def list_citations(narrower_citations, wider_citations, lbl_results):
  citation_string = []
  [citation_string.append(citation + "\n") for citation in narrower_citations.citations]
  if len(wider_citations.citations) > 0:
      [citation_string.append(citation + "\n") for citation in wider_citations.citations]
  results = "".join(citation_string)
  app_data.set_new_results(results, [lbl_results])
  return("break")

def get_file(lbl_filename, lbl_contents):
  filename = filedialog.askopenfilename(title = "Select a document to search for citations:")
  lbl_filename["text"] = filename
  citations = analyse_file(filename)
  list_citations(citations[0], citations[1], lbl_contents)
  
  return("break")



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

lbl_results = tk.Label(master = fr_results, bg = "white",
                       text = app_data.active_results,
                       anchor = "w", justify = "left")

lbl_results.grid(row = 0, column = 0, sticky = "NW", columnspan = 4,
                 padx = 5)

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

btn_choose.bind("<Button-1>",
                lambda event, lbl_filename = lbl_current_file,
                lbl_contents = lbl_results:
                  get_file(lbl_filename, lbl_contents))

# Final window object ----
main_window.focus_force()
main_window.mainloop()




