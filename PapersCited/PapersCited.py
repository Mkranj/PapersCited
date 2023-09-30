# -*- coding: utf-8 -*-
from UI.windowUI import main_window
from UI.messages import version

# Welcome message, before loading anything
if __name__ == "__main__":
    print("PapersCited", version, "startup. Please wait...")
    

# MAIN ----

def main():
    main_window.focus_force()
    main_window.mainloop()

if __name__ == "__main__":
    main()
