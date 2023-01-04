# PapersCited
## v1.2.1
Write an Excel file containing all citations found in a document, so they can be used to check or build a reference list.

## Dependencies:
This program was written using Python 3.9.12. It requires the following modules:
textract, xlsxwriter, regex

To install them in Powershell, type "*pip install textract*" and press Enter. After that, follow with "*pip install xlsxwriter*" and "*pip install regex*".

# About:
***PapersCited*** is a small Python program designed to help you with **writing and reviewing reference lists** in your scientific articles. It reads through a document of your choice and takes a note every time something is cited. At the end, it writes all those citations in an Excel file in alphabetical order, omitting duplicate entries. 
With that file, you can easily go through your reference list and note if you cited something but didn't include it in the reference list or, conversely, you have a reference that isn't cited anywhere in the article. It is also handy for writing a reference list from stratch. You no longer need to manually go over the whole article and note all the times you cite another source.  

**Longer citations** appear in a separate column. These encompass citations listing three authors, or authors with two surnames (e.g. *Van Selm and Jankowsky (2006)*). However, the potential for superfluous words being recognised as proper surnames is somewhat higher here, so they are displayed separately.

The first column is empty so you can easily mark certain citations as "OK" or "needs double-checking" when reviewing a reference list.

Tested on Windows 10 using .doc, .docx, .txt and .pdf files. 
This program is appropriate for texts written in **English** and **Croatian**. Some sources may be detected incorrectly in other languages. The software is written with **APA style** citations in mind, but **Chicago style** and similar would work as well.

## Instructions:
- Download **PapersCited.py** (From the *Releases* tab, or click *Code* -> *Download Zip* on this page).
- Run the .py file. If you have already used Python, you can probably double-click the file to run the program.
- When prompted, select the document you want to search for citations.

The program creates an Excel file called "citations.xlsx" in the same directory as the document. **If a file called citations.xlsx already exists, it will be overwritten!**

The github repository includes a file called "*test.docx*" if you want to see what the program output looks like. Download "test.docx" and "PapersCited.py", and run the .py file.

## What if I don't have Python?
Before running the script, install the Miniconda distribution to run Python scripts on your computer: 
https://docs.conda.io/en/latest/miniconda.html  
Keep the default values for all the settings **except** the checkbox asking to put Miniconda on your Path variable. That is off by default, **turn it on**.  

After installing Miniconda, open the start menu and search for Windows Powershell, then open it. Install the two modules required by the program, as described in **Dependencies**.

With all that done, the script should run when double-clicked. If it asks you which program to open it with, choose to *look for another app on this PC* and navigate to C:\Users\\*(your username)*\miniconda3 and select *python.exe*. Now you can just double-click on the script to run it.

## Solutions for potential issues:
- If you get an error reading .doc or .pdf files on Windows, you might need to download additional libraries for working with these files. See "**help_with_libraries.txt**" for detailed instructions on how to do so. 

## Known limitations:
- Secondary citations ("*XX 2010, as cited in YY 2012*"). *YY 2012* is detected correctly. However, *XX 2010* also gets recorded as a primary source. *XX 2010* should not be included in the reference list.
- In Croatian, different declinations of the author's surnames get detected as different authors.
- Surnames with three or more words, such as van der Flier, will get recorded only as the last word or last two words - *Kappe and van der Flier (2010)* will be recorded as *Flier 2010*, **skipping the first author**! These require special attention when writing or reviewing a reference list. Multiple surnames with an "*-*", however, will be recorded correctly.
- Similarly, when citing organizations, laws and other documents, it possible that only the end of the full name gets recorded. *World Health Organization (2000)* will be recorded as *Organization 2000*, with *Health Organization 2000* as a separate suggestion. (*WHO 2000* would be fine, though.) So if you are working with these kinds of sources, extra attention is needed.

## Lastly...
Any comments, bug reports and suggestions are welcome. Happy writing!
