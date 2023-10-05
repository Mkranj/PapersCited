# -*- coding: utf-8 -*-
from UI.mainWindow import mainWindow
from UI.messages import version
from ctypes import windll

# Welcome message, before loading anything
if __name__ == "__main__":
    print("PapersCited", version, "startup. Please wait...")
    

# MAIN ----

def main():
    # Resolution awareness - prevents from being blurry on high DPI
    windll.shcore.SetProcessDpiAwareness(1)
    UI = mainWindow()
    
    UI.focus_force()
    UI.mainloop()

if __name__ == "__main__":
    main()
