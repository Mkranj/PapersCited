# -*- coding: utf-8 -*-
from UI.mainWindow import mainWindow
from UI.messages import version

# Welcome message, before loading anything
if __name__ == "__main__":
    print("PapersCited", version, "startup. Please wait...")
    

# MAIN ----

def main():
    UI = mainWindow()
    
    UI.focus_force()
    UI.mainloop()

if __name__ == "__main__":
    main()
