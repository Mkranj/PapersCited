version = "1.3"

break_with_lines = "--------------------"

intro_message = "Welcome to PapersCited " + version + "!" + \
  "\n\nFind citations in the text of a file by selecting 'Choose document'. Alternatively, analyse the text in your clipboard by selecting 'From clipboard'."

cant_read_doc_msg = "NOTE: An additional library is required to read .doc files." + \
    "\nThe simplest solution is to convert the file to a .docx file, then try analysing it again." + \
    "\n\nAnother solution is to setup Antiword." + \
    "\nFor more information, please check 'help_with_libraries.txt' at PapersCited Github: " + \
    "https://github.com/Mkranj/PapersCited/blob/main/help_with_libraries.txt"
    
cant_read_pdf_msg = "NOTE: An additional library, poppler, is required to read .pdf files." + \
    "\nFor more information, please check 'help_with_libraries.txt' at PapersCited Github: " + \
    "https://github.com/Mkranj/PapersCited/blob/main/help_with_libraries.txt" + \
    "\nAlternatively, you can manually copy the text from the .pdf and paste it into a" + \
    "supported file format, such as .docx or .txt."

reading_txt_warning = "Warning! " + \
    "If you encounter problems reading this .txt file, backup the original file, then try saving it in UTF-8 or ANSI encoding.\
    \n(\"Save as...\" dialog, \"Encoding:\" at the bottom.)\n"
    
saving_cancelled = "\n" + break_with_lines + \
    "\nSaving cancelled."

no_citations_found = "No citations were found."

no_citations_to_save = "Cannot save file: no citations found."

no_file_selected = "No file selected."

def filename_cant_be_read_message(filename, extension):
    message = f"The file {filename} couldn't be read. Make sure the file is a valid textual file."
    
    if extension == ".doc":
        message = message + "\n" + cant_read_doc_msg + "\n"
        
    if extension == ".pdf":
        message = message + "\n" + cant_read_pdf_msg + "\n"

    return(message)

def report_found_citations(filename, citations, wider_citations):
    
    n_narrower_citations = len(citations.citations) 
    try:
        n_wider_citations = len(wider_citations.citations) 
        total_citations = n_narrower_citations + n_wider_citations
    except:
        total_citations = n_narrower_citations
    
    success_message = "\n\n" + break_with_lines + \
        f"\nSuccess!\nCreated file with citations: {filename}"
    
    if n_wider_citations:
        success_message = success_message + \
        f"\n{n_narrower_citations} citations have been found, along with" + \
        f" {n_wider_citations} longer citations."
    
    success_message = success_message + \
        f"\nA total of {total_citations} different citations have been recorded."
    
    return(success_message)

def cant_write_file(filename):
    message = f"Cannot create citation file for {filename}." + \
        "\nPossible permissions issue, can you create files at that folder?"
    return(message)
