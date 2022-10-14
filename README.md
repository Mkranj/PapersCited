# PapersCited
Write an Excel file containing all citations found in a document, so they can be used to check or build a reference list.

## Dependencies:
This program was written using Python 3.9.12. It requires the following modules:
textract, xlsxwriter

To install them in Powershell, type "*pip install textract*", followed by "*pip install xlsxwriter*"

# About:
***PapersCited*** is a small Python program designed to help you with **writing and reviewing reference lists** in your scientific articles. It reads through a document of your choice and takes a note every time something is cited. At the end, it writes all those citations in an Excel file in alphabetical order, omitting duplicate entries. 
With that file, you can easily go through your reference list and note if you cited something but didn't include it in references or, conversely, you have a reference that isn't cited anywhere in the article. It is also handy for writing a reference list from stratch. You no longer need to manually go over the whole article and note all the times you cite another source.

Tested on Windows using .doc, .docx, .txt and .pdf files. 
This program is appropriate for texts written in **English** and **Croatian**. Some sources may be detected incorrectly in other languages. The software is written with **APA style** citations in mind, but **Chicago style** would probably work as well.

## Instructions:
- Download **PapersCited.py** and put it into a folder with the document you want to extract citations from.
- Run the .py file. If you have already used Python, you can probably double-click the file to run the program.
- When prompted, input the full name of the target document, including the extension.

The program creates an Excel file called "citations.xlsx" in the same directory. **If a file called citations.xlsx already exists, it will be overwritten!**

The github repository includes a file called "*test.docx*" if you want to see what the program output looks like. Download test.docx and PapersCited.py in the same folder, and run the .py file.

The first column is empty so you can easily mark certain citations as "OK" or "double-check" when making or reviewing a reference list. If this bothers you, change "column = 1" to "column = 0" near the end of the script.

## What if I don't have Python?
Before running the script, install the Miniconda distribution to run Python scripts on your computer: 
https://docs.conda.io/en/latest/miniconda.html  
Keep all the settings on default **except** the checkmark asking to put Miniconda on your Path variable. That is off by default, turn it on.  
After installing, open Powershell and install the two modules required by the program, as described in **Dependencies**.  
With all that done, the script should run when double-clicked. If it asks you for the program to open it with, choose to select an application and navigate to C:\Users\\*(your username)*\miniconda3 and select *python.exe*. Now you can just double-click on the script to run it.

## Solutions for potential issues:
- If you get an error reading .doc files on Windows, you need to download *Antiword* and set it in your PATH environmental variable.
Guide: https://stackoverflow.com/questions/51727237/reading-doc-file-in-python-using-antiword-in-windows-also-docx/51727238#51727238

- Similarly, if PDF files are not being read, download *poppler-22.04.0* for Windows. Put the poppler folder in your C:\Program files and find the "bin" folder inside it. Copy the path to bin folder in your PATH environmental variable.  
Note that **PDF is tehnically supported, but not recommended!** Differently encoded PDFs can result in new lines breaking citations, or certain characters being read inaccurately. 

## Known limitations:
- Citations with three or more authors in the text. Note that this is incorrect citing according to APA 7, and you should use "*First author et al.*" instead. If your document still has this old way of citing, only the last two authors will be recorded.
- Secondary citations ("*XY 2010, as cited in ZZ 2012*"). *ZZ 2012* gets detected correctly, which is important. However, *XY* also gets detected as a primary source. *XY* should not be included in the reference list.
- In Croatian, different declinations of the author's surnames get detected as different authors.
- Multiple surnames such as van der Flier will get recorded only as the last word - *Van Selm and Jankowski (2006)* will be recorded as *Selm & Jankowski 2006*. *Kappe and van der Flier (2010)* will be recorded as *Flier 2010*, ignoring the first author! These require special attention when writing or reviewing a reference list. Multiple surnames with an "-", however, will be recorded correctly.
- Similarly to the last point, when citing organizations, laws and other documents, it possible that only the end of the full name gets recorded. *World Health Organization (2000)* will be recorded as *Organization (2000)*. (*WHO 2000* would be fine, though.) I can't find a workaround that wouldn't also catch lots of unnecessary words. So if you are working with these kinds of sources, extra attention is needed.

## Lastly...
Any comments, bug reports and suggestions are welcome. Happy writing!
