break_with_lines = "--------------------"

def filename_cant_be_read_message(filename):
    message = f"The file {filename} couldn't be read. Make sure the file is a valid textual file." + \
        "If you can regularly open it, you may be missing certain libraries:" + \
        "\nantiword for .doc (not .docx)" + \
        "\npoppler for .pdf" + \
        "\n\nPlease check 'help_with_libraries.txt' at PapersCited Github:" + \
        "https://github.com/Mkranj/PapersCited/blob/main/help_with_libraries.txt"
    return(message)
