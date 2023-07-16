# -*- coding: utf-8 -*-
version = "v.1.2.3"

# Welcome message, before loading anything
if __name__ == "__main__":
    print("PapersCited", version, "startup. Please wait...")
    

# MAIN ----

def main():
    print("\nChoose the file you want to find citations in.")
    filename = get_file()
    check_file(filename)
    document = read_document(filename)
    
    # Get all types of citations
    solo_authors = get_matches_solo_author(document, drop_excluded_phrases = True)
    two_authors = get_matches_two_authors(document, drop_excluded_phrases = True)
    three_authors = get_matches_three_authors(document, drop_excluded_phrases = True)
    author_et_al = get_matches_author_et_al(document, drop_excluded_phrases = True)
    two_surnames = get_matches_two_surnames(document, drop_excluded_phrases = True)
    two_surnames_et_al = get_matches_two_surnames_et_al(document, drop_excluded_phrases = True)
        
    solo_authors.delete_clones_of_citations(two_authors)
    
    narrower_citations = CitationType(solo_authors.citations + 
                                      two_authors.citations +
                                      author_et_al.citations)
    
    wider_citations = CitationType(three_authors.citations + 
                                   two_surnames.citations +
                                   two_surnames_et_al.citations)
    
    narrower_citations.cleanup()
    wider_citations.cleanup(allow_commas = False) # False prevents lots of duplication
    write_excel(filename, narrower_citations, wider_citations)
    preview_citations(narrower_citations, wider_citations)

if __name__ == "__main__":
    continue_processing_files = True
    while continue_processing_files:
        main()
        continue_processing_files = dialog_process_another_file()
        if continue_processing_files:
            print("\n-------------------\n")
