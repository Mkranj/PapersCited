import citationAnalysis.citationAnalysis as ca
import UI.messages as ms
import UI.transformCitations as tc

import os
import textract
import xlsxwriter
from docx2python import docx2python

def check_file(filename):
    # Check if the file entered actually exists
    file_exists = os.path.isfile(filename)

    if file_exists == False:
        raise Exception(ms.no_file_selected)

    warning = None
    
    file_extension = os.path.splitext(filename)[1]

    if file_extension.casefold() == ".txt":
        warning = ms.reading_txt_warning
        
    return(warning)


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
        message = check_file(filename)
    except:
        raise Exception(ms.no_file_selected)
    
    file_extension = os.path.splitext(filename)[1].casefold()
    
    try:
        target_document = textract.process(filename, output_encoding="utf-8-sig")
    except Exception as e:
        # get only the text of the exception
        error = str(e)
        # If the file exists, but cannot be read, an error will be raised.
        error_message = ms.filename_cant_be_read_message(filename, file_extension) + \
            "\nThe error message:\n" + error
        raise Exception(error_message)

    # UTF-8 encoding so it recognises foreign characters
    target_document = target_document.decode("utf-8-sig")
    
    if file_extension == ".pdf":
        target_document = target_document.replace("\r\n", " ")
        target_document = target_document.replace("\r", "")
        target_document = target_document.replace("\n", " ")
    
    if file_extension == ".docx":
        footnote_text = read_docx_footnotes(filename)
        target_document = target_document + " \n " + footnote_text
    
    operation_success = {"document_text": target_document,
                         "status_message": message}
        
    return(operation_success)


# "All-in-one" fn to perform all neccessary steps of analysis on a given file.
def find_citations(document_text):

    # Get all types of citations
    solo_authors = ca.get_matches_solo_author(document_text, drop_excluded_phrases = True)
    two_authors = ca.get_matches_two_authors(document_text, drop_excluded_phrases = True)
    three_authors = ca.get_matches_three_authors(document_text, drop_excluded_phrases = True)
    author_et_al = ca.get_matches_author_et_al(document_text, drop_excluded_phrases = True)
    two_surnames = ca.get_matches_two_surnames(document_text, drop_excluded_phrases = True)
    two_surnames_et_al = ca.get_matches_two_surnames_et_al(document_text, drop_excluded_phrases = True)
        
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
    output_filename = output_file_prefix[0] + ".xlsx"
    
    # Create a file
    workbook = xlsxwriter.Workbook(output_filename)

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
    output_filename = output_file_prefix[0] + ".txt"

    citations_string = tc.citations_to_string_pretty(citations, wider_citations)
    
    # Create a file
    with open(output_filename, 'w', encoding = "utf-8") as f:
        f.write(citations_string)
    
    success_message = ms.report_found_citations(output_filename, citations, wider_citations)
    
    return(success_message)

    