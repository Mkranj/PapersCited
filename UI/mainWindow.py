import tkinter as tk
import tkinter as tk
import UI.messages as ms
from UI.appData import AppData
import UI.btnFunctions as bfn
import os.path

# Constants ----

light_yellow = "#ffe08f"

startup_filename = ""
startup_text = ms.intro_message

citations_font = "Segoe UI Variable"
citations_font_size = 11

class mainWindow(tk.Tk):
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
        
        self.data = AppData(startup_filename, startup_text)
        
        # Create an icon for the main window
        UI_dir = os.path.dirname(os.path.abspath(__file__))
        PC_icon_file = os.path.join(UI_dir, "P_icon.png")
        PC_icon = tk.PhotoImage(file = PC_icon_file)
        self.wm_iconphoto(True, PC_icon)
        
        self.create_widgets()
        self.create_event_bindings()
        
    def create_widgets(self):
        # Sets up individual UI elements
        self.__build_btn_choose()
        self.__build_btn_from_clipboard()
        self.__build_results()
        self.__build_save_xlsx()
        self.__build_save_txt()
        self.__build_right_click_menu()
        
    def __build_btn_choose(self):
        btn_choose = tk.Button(master = self,
                        text = "Choose document",
                        borderwidth = 3, relief=tk.RAISED,
                        padx = 8, pady = 5
                        )

        btn_choose.grid(row = 0, column = 0, sticky = "NW", padx = 10, pady = 5)
        self.btn_choose = btn_choose
        
    def __build_btn_from_clipboard(self):
        btn_from_clipboard = tk.Button(master = self,
                        text = "From clipboard",
                        borderwidth = 3, relief=tk.RAISED,
                        padx = 8, pady = 5
                        )

        btn_from_clipboard.grid(row = 0, column = 1, sticky = "NW", padx = 5, pady = 5)
        self.btn_from_clipboard = btn_from_clipboard
        
    def __build_results(self):
        # Frame element
        fr_results = tk.Frame(master = self, bg = "white",
                      borderwidth = 2, relief = tk.GROOVE)
        fr_results.grid(row = 1, column = 0, sticky = "NWSE", columnspan = 5,
                        padx = 10)

        fr_results.columnconfigure(0, weight = 1)
        fr_results.columnconfigure(1, weight = 0)
        fr_results.rowconfigure(0, weight = 1)

        # Scrollbar element
        scr_results = tk.Scrollbar(fr_results, orient = "vertical")
        scr_results.grid(row = 0, column = 1, sticky = "NS")

        # Text field element
        txt_results = tk.Text(master = fr_results, bg = "white", yscrollcommand = scr_results.set, wrap = tk.WORD)
        txt_results.configure(font = (citations_font, citations_font_size))
        txt_results.insert(tk.END, self.data.get_active_results())

        scr_results.config(command=txt_results.yview)

        txt_results.config(state = "normal")
        txt_results.grid(row = 0, column = 0, sticky="NSWE")
        txt_results.config(state = "disabled")
        self.txt_results = txt_results
        
    def __build_save_xlsx(self):
        btn_save_xlsx = tk.Button(master = self,
                          text = "Save as .xlsx",
                        borderwidth = 2,
                        padx = 5, pady = 5)

        btn_save_xlsx.grid(row = 2, column = 3, sticky = "SE",
                        padx = 10, pady = 5)
        self.btn_save_xlsx = btn_save_xlsx
        
    def __build_save_txt(self):
        btn_save_txt = tk.Button(master = self,
                          text = "Save as .txt",
                        borderwidth = 2,
                        padx = 5, pady = 5)

        btn_save_txt.grid(row = 2, column = 4, sticky = "SE",
                        padx = 10, pady = 5)
        self.btn_save_txt = btn_save_txt
    
    def __build_right_click_menu(self):
        rc_menu = tk.Menu(master = self, tearoff=0)
        self.rc_menu = rc_menu
        
    def create_event_bindings(self):
        # Bind functionality to UI parts. Functions itself defined in btn_functions
        self.btn_choose.bind("<Button-1>", lambda event:
            bfn.fn_btn_choose(event, self.btn_choose, master = self))
        self.btn_choose.bind(
            "<ButtonRelease>", lambda event: bfn.fn_btn_release(event, self.btn_choose))

        self.btn_from_clipboard.bind("<Button-1>", lambda event:
            bfn.fn_btn_from_clipboard(event, self.btn_from_clipboard, master=self))
        self.btn_from_clipboard.bind(
            "<ButtonRelease>", lambda event: bfn.fn_btn_release(event, self.btn_from_clipboard))
        
        self.btn_save_xlsx.bind("<Button-1>", lambda event:
            bfn.fn_btn_save_xlsx(event, self.btn_save_xlsx, master=self))
        self.btn_save_xlsx.bind(
            "<ButtonRelease>", lambda event: bfn.fn_btn_release(event, self.btn_save_xlsx))
        
        self.btn_save_txt.bind("<Button-1>", lambda event:
            bfn.fn_btn_save_txt(event, self.btn_save_txt, master=self))
        self.btn_save_txt.bind(
            "<ButtonRelease>", lambda event: bfn.fn_btn_release(event, self.btn_save_txt))
        
        # The text widget can be copied from
        self.rc_menu.add_command(label="Copy", command = lambda: bfn.copy_to_clipboard(master = self))
        self.txt_results.bind("<Button-3>", lambda event: bfn.popup_menu(event, self.rc_menu))
        
    def update_text_widget(self, new_text, replace = False, position = "end", scroll_to_update = False):
        """Change displayed text.

        Args:
            new_text (string): What should be displayed in the text widget.
            replace (bool, optional): Should this text replace existing content instead of being appended? Defaults to False.
            position (str, optional): Where should this text be appended? Possible values are "start" and "end".
                If replace is true, doesn't affect the result. Defaults to "end".
            scroll_to_update (bool, optional): Should the text widget scroll to the newly added text? Defaults to False.
        """
        text_wg = self.txt_results
        
        if position == "start":
            place_to_write = "1.0"
        elif position == "end":
            place_to_write = tk.END
        else:
            Exception("Incorrect position argument!")

        text_wg.config(state = "normal")
        if replace:
            text_wg.delete("1.0", tk.END)
        text_wg.insert(place_to_write, new_text)
        text_wg.config(state = "disabled")
        
        if scroll_to_update:
            text_wg.see(position)
    