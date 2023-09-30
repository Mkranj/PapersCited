# -*- coding: utf-8 -*-
from UI.main_window import main_window
from UI.messages import version

# Welcome message, before loading anything
if __name__ == "__main__":
    print("PapersCited", version, "startup. Please wait...")
    

# MAIN ----

def main():
    UI = main_window()
    
    UI.focus_force()
    UI.mainloop()

if __name__ == "__main__":
    main()
