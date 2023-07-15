import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Variables ----
light_yellow = "#ffe08f"

current_filename = None

# UI functions ----

def get_file(lbl_filename):
  filename = filedialog.askopenfilename(title = "Select a document to search for citations:")
  lbl_filename["text"] = filename
  return(filename)

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
                            text = "path/to/file", bg = light_yellow,
                            pady = 3)

lbl_current_file.grid(row = 0, column = 0, sticky = "W", padx = 5, pady = 5)

fr_results = tk.Frame(master = main_window, bg = "white",
                      borderwidth = 2, relief = tk.GROOVE)
fr_results.grid(row = 1, column = 0, sticky = "NWSE", columnspan = 4,
                 padx = 10)

lbl_results = tk.Label(master = fr_results, bg = "white",
                       text = "Results will be shown here...")

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
                lambda event, lbl_filename = lbl_current_file:
                  get_file(lbl_filename))

# Final window object ----
main_window.focus_force()
main_window.mainloop()




