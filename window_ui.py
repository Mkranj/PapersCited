import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

light_yellow = "#ffe08f"

main_window = tk.Tk()
main_window.columnconfigure(0, weight = 0, minsize = 50)
main_window.columnconfigure(1, weight = 1, minsize = 100)
main_window.rowconfigure(0, weight = 0, minsize = 30)
main_window.rowconfigure(1, weight = 2, minsize = 400)
main_window.rowconfigure(2, weight = 0, minsize = 30)

main_window.minsize(750, 500)

btn_choose = tk.Button(master = main_window,
                        text = "Choose document",
                        borderwidth = 2)

btn_choose.grid(row = 0, column = 0, sticky = "NW", padx = 10, pady = 5)

lbl_current_file = tk.Label(master = main_window,
                            text = "path/to/file", bg = light_yellow)

lbl_current_file.grid(row = 0, column = 1, columnspan = 3, sticky = "NWES",
                      padx = 10, pady = 5)

fr_results = tk.Frame(master = main_window, bg = "white")
fr_results.grid(row = 1, column = 0, sticky = "NWSE", columnspan = 4,
                 padx = 10)

lbl_results = tk.Label(master = fr_results, bg = "white",
                       text = "Results will be shown here...")

lbl_results.grid(row = 0, column = 0, sticky = "NW", columnspan = 4,
                 padx = 5)

btn_save_xlsx = tk.Button(master = main_window,
                          text = "Save as .xlsx",
                        borderwidth = 2)

btn_save_xlsx.grid(row = 2, column = 2, sticky = "SE",
                        padx = 10, pady = 5)

btn_save_txt = tk.Button(master = main_window,
                          text = "Save as .txt",
                        borderwidth = 2)

btn_save_txt.grid(row = 2, column = 3, sticky = "SE",
                        padx = 10, pady = 5)

main_window.title("PapersCited")
main_window.mainloop()



