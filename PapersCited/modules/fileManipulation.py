import modules.citationAnalysis as ca
import modules.messages as ms

import os
import sys
import textract
import xlsxwriter
import tkinter
from tkinter import filedialog
from docx2python import docx2python

def check_file(filename):
    # Check if the file entered actually exists
    file_exists = os.path.isfile(filename)

    if file_exists == False:
        raise Exception("No file selected")

    file_extension = os.path.splitext(filename)[1]
    if file_extension.casefold() == ".pdf":
        print("Warning!\nReading PDF files is not recommended and might result in inaccurate transcription.\n")

    if file_extension.casefold() == ".txt":
        print("Warning! Reading .txt files might lead to problems with special characters." +
              "\nTo ensure the best format is used, backup the .txt file, \
                then try saving it in UTF-8 or ANSI encoding." +
              "\n(\"Save as...\" dialog, \"Encoding:\" at the bottom.)\n")


def read_docx_footnotes(filename):
    content =  docx2python(filename)
    footnotes_container = content.footnotes_runs
    content.close()
    
    if footnotes_container == []:
        return("")
    
    # The third nested list contains different footnotes,
    # that footnote's nested list [0][1] is the footnote text
    footnotes = []
    footnotes_unnested = footnotes_container[0][0]
    for footnote in footnotes_unnested:
        footnotes.append(footnote[0])
    
    # First two lists are always empty and have no [1] object
    footnotes = footnotes[2 : (len(footnotes))]
    
    footnotes = [footnote[1] for footnote in footnotes]
    
    footnotes_text = " \n ".join(footnotes)
    
    return(footnotes_text)

def read_document(filename):

    try:
        target_document = textract.process(filename, output_encoding="utf-8-sig")
    except Exception as e:
        # get only the text of the exception
        error = str(e)
        # If the file exists, but cannot be read, an error will be raised.
        error_message = ms.filename_cant_be_read_message(filename) + \
            "\nThe error message:\n" + error
        raise Exception(error_message)

    # UTF-8 encoding so it recognises foreign characters
    target_document = target_document.decode("utf-8-sig")
    
    file_extension = os.path.splitext(filename)[1]
    if file_extension.casefold() == ".pdf":
        target_document = target_document.replace("\r\n", " ")
        target_document = target_document.replace("\r", "")
        target_document = target_document.replace("\n", " ")
    
    if file_extension.casefold() == ".docx":
        footnote_text = read_docx_footnotes(filename)
        target_document = target_document + " \n " + footnote_text
        
    return(target_document)

# "All-in-one" fn to perform all neccessary steps of analysis on a given file.
def find_citations(filename):
    try: 
        check_file(filename)
    except:
        raise Exception("No file selected")
    
    document = read_document(filename)
    
    # Get all types of citations
    solo_authors = ca.get_matches_solo_author(document, drop_excluded_phrases = True)
    two_authors = ca.get_matches_two_authors(document, drop_excluded_phrases = True)
    three_authors = ca.get_matches_three_authors(document, drop_excluded_phrases = True)
    author_et_al = ca.get_matches_author_et_al(document, drop_excluded_phrases = True)
    two_surnames = ca.get_matches_two_surnames(document, drop_excluded_phrases = True)
    two_surnames_et_al = ca.get_matches_two_surnames_et_al(document, drop_excluded_phrases = True)
        
    solo_authors.delete_clones_of_citations(two_authors)
    
    narrower_citations = ca.CitationType(solo_authors.citations + 
                                      two_authors.citations +
                                      author_et_al.citations)
    
    wider_citations = ca.CitationType(three_authors.citations + 
                                   two_surnames.citations +
                                   two_surnames_et_al.citations)
    
    narrower_citations.cleanup()
    wider_citations.cleanup()
    
    citation_list = [
        narrower_citations,
        wider_citations
    ]
    return(citation_list)

def write_excel(filename, citations, wider_citations):
    # Retrieve the filepath (and extension) of the analysed document,
    # The output file will have a similar name and be created 
    # in the same directory.
    output_file_prefix = os.path.splitext(filename)
    output_filename = output_file_prefix[0] + "_citations.xlsx"

    # Create a file
    try:
        workbook = xlsxwriter.Workbook(output_filename)
    except Exception as e:
        error = str(e)
        raise Exception(ms.cant_write_file(output_filename) + f"\n{error}")

    worksheet1 = workbook.add_worksheet()

    # We'll write in the second column.
    # The first column is useful for marking certain citations as "done" or "double-check"
    column = 1
    row = 0

    # Iterate through output list
    for item in citations.citations:
        worksheet1.write(row, column, item)
        row += 1

    # If there are potential wider matches, write them in the sixth column.
    if wider_citations:
        column = 5
        row = 0
        for item in wider_citations.citations:
            worksheet1.write(row, column, item)
            row += 1
    
    workbook.close()
    
    success_message = ms.report_found_citations(output_filename, citations, wider_citations)
    
    return(success_message)

def write_txt(filename, citations, wider_citations):
    # Retrieve the filepath (and extension) of the analysed document,
    # The output file will have a similar name and be created 
    # in the same directory.
    output_file_prefix = os.path.splitext(filename)
    output_filename = output_file_prefix[0] + "_citations.txt"

    citations_string = ca.citations_to_string_pretty(citations, wider_citations)
    
    # Create a file
    try:
        with open(output_filename, 'w') as f:
            f.write(citations_string)
    except Exception as e:
        error = str(e)
        raise Exception(ms.cant_write_file(output_filename) + f"\n{error}")
    
    success_message = ms.report_found_citations(output_filename, citations, wider_citations)
    
    return(success_message)

def shorten_filename(filename, nchar = 50):
    f_length = len(filename)
    if f_length <= nchar: return(filename)
    
    cutoff_length = nchar - 2
    first_part = filename[0:(cutoff_length - 1)]
    shortened_name = first_part + "..."
    return(shortened_name)

def any_citations_recorded(get_citations):
    # Return true if appData houses any citations
    if get_citations == []: return(False)
    
    narrow = get_citations[0].citations
    wider = get_citations[1].citations
    
    if len(narrow) > 0 or len(wider) > 0:
        return(True)
    else:
        return(False)
    