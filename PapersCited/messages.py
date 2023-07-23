break_with_lines = "--------------------"

def filename_cant_be_read_message(filename):
    message = f"The file {filename} couldn't be read. Make sure the file is a valid textual file." + \
        "If you can regularly open it, you may be missing certain libraries:" + \
        "\nantiword for .doc (not .docx)" + \
        "\npoppler for .pdf" + \
        "\n\nPlease check 'help_with_libraries.txt' at PapersCited Github:" + \
        "https://github.com/Mkranj/PapersCited/blob/main/help_with_libraries.txt"
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

no_citations_found = "No citations were found."
no_citations_to_save = "Cannot save file: no citations found."