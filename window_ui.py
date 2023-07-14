import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

main_window = tk.Tk()

btn_choose = tk.Button(master = main_window,
                        text = "Choose document")

btn_choose.grid(row = 0, column = 0)

main_window.columnconfigure(0, weight = 0, minsize = 50)
main_window.columnconfigure(1, weight = 1, minsize = 100)

lbl_current_file = tk.Label(master = main_window,
                            text = "path/to/file", bg = "blue")

lbl_current_file.grid(row = 0, column = 2)

lbl_results = tk.Label(master = main_window,
                       text = "Results will be shown here...")

lbl_results.grid(row = 1, column = 1)
main_window.rowconfigure(1, minsize = 400)

btn_save_xlsx = tk.Button(master = main_window,
                          text = "Save as .xlsx")

btn_save_xlsx.grid(row = 2, column = 2)

btn_save_txt = tk.Button(master = main_window,
                          text = "Save as .txt")

btn_save_txt.grid(row = 2, column = 3)

main_window.mainloop()



