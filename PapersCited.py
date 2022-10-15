# -*- coding: utf-8 -*-

# For reading doc files
import textract

# regex in Python
import re

# writing to XLSX
import xlsxwriter
import os
import sys

# Tested with these file types:
# .doc, .docx, .txt, .pdf
# .pdf is not recommended! Some characters might be read incorrectly, and line breaks might break citations.

filename = input("Paste the name of the file to process, including the .doc or .docx extension: ")

# Check if the file entered actually exists, or is possibly mistyped
file_exists = os.path.isfile(filename)

# If the filename is False, exit the program.
if file_exists == False:
    input(f"No file named {filename} in directory. Press Enter to end the program.")
    sys.exit()

# Warning for PDF files:
file_extension = filename[-4:]
if file_extension == ".pdf":
    print("Warning!\nReading PDF files is not recommended and might result in inaccurate transcription.")

# Read the document file:
try:
    target_document = textract.process(filename)
except:
    # If the file exists, but cannot be read, an error will be raised.
    print(f"The file {filename} couldn't be read. Make sure the file is valid. If you can regularly open it,")
    print("please report a bug and consult the Internet for textract errors with this type of file.")
    print("For opening .doc (not .docx) files on Windows, downloading Antiword can solve the problem,")
    print("please consult the documentation.")
    print("For .pdf files, downloading poppler can solve the issue.")
    print("\nPress Enter to exit the program.")
    input()
    sys.exit()

# UTF-8 encoding so it recognises foreign characters
target_document = target_document.decode("utf-8")


# These are the ways a source can be cited in text:

# 1) One author
# 2) Author & author / author and author / author i author
# 3) Author et al.

# The year of the source can be separated by ( or ,
# The function will be case-insensitive.

# For ease of reading, parts of the regex will be assigned to variables

# Name - any combination of letters. Added extra characters that might occur,
# as well as ' in Cohen's and - for multi-part last names.
rx_author_name = "[a-zšđčćžäöüñáéíóú'’\-]+"

# Between names and years, add this
# "[\s,(]+"
# To capture spaces or commas. If someone types Author(1999) without space,
# the inclusion of ( will catch it as well.

# Year - four digits preceded by ( or commas (commas are caught in the previous part). Possibly multiples.
rx_years = "(?:\(?\d\d\d\d,?\s?;?)+"

# Catching individual types of citation ----

# 1) One author
regex_case1 = re.findall(
    rx_author_name + "[\s,(]+" + rx_years,
    target_document,
    re.IGNORECASE,
)


# 2) Author & author / author and author / author i author
# Note that the part before rx_years now includes a dot in the character set [\s,.]+
# This catches the Croatian part "i sur." in citations.
regex_case2 = re.findall(
    rx_author_name + ",? (?:and+|[i&]+)+ " + rx_author_name + "[\s,.(]+" + rx_years,
    target_document,
    re.IGNORECASE,
)

# Which authors detected in 1) as solo authors are actually part of "Author & author / author and author"?
# Detect the pattern starting with " and/&/i " in 2)

second_authors = []
for index_no, citation in enumerate(regex_case2):
    second_authors.append(
        (
            re.findall(
                " (?:and+|[i&]+)+ " + rx_author_name + "[\s,(]+" + rx_years,
                citation,
                re.IGNORECASE,
            )
        )
    )

# It's a list of lists, turn it into a list of strings
second_authors = ["".join(citation) for citation in second_authors]

# Some strings in second_authors might be empty.
# That's because it detected "i sur." in case 2), which has no meaning on its own.
# These should be dropped from the second_authors list.
second_authors = list(filter(None, second_authors))

# Strip "and/&/i" from the start of lines. For safety, the count of things to be replaced is 1.
# Note that the words are enclosed with spaces!
starts_with_and = [" and ", " & ", " i "]

for index_no, citation in enumerate(second_authors):
    # Citation by citation, check and change all listed symbols
    for phrase in starts_with_and:
        second_authors[index_no] = second_authors[index_no].replace(phrase, "", 1)

# Now we have two lists, all authors with year detected and only those who occur after an i/&
# For each occuring in the second list, delete ONE from the first - so if theres A & B 2000 and also B 2000,
# The second one will be its own instance and won't be deleted
# the remove() method does exactly what we want - removes the first element matching the value given

for author in second_authors:
    if author in regex_case1:
        regex_case1.remove(author)
    else:
        # All of second_authors should be included in regex_case1.
        # If there's somehow an additional entry in second_authors, notify the user.
        # That would be a bug.
        print(f"Error! {author} detected as a second author, but not caught in Case1.")
        print("Please report this as a bug.")
        print("The program will still generate an usable output.")


# 3) Author et al.
# Note that the dot doesn't need to be escaped inside of a [character set]
regex_case3 = re.findall(
    rx_author_name + " et al[\s,.(]+" + rx_years,
    target_document,
    re.IGNORECASE,
)

# Combine all found cases into a single list
complete_list = regex_case1 + regex_case2 + regex_case3

# Editing the list ----

# For clarity and spotting duplicates, remove the following from citations:
chars_to_remove = [",", "(", ")", ";", "."]

# Several phrases in the final list should be adjusted:
phrases_to_adjust = {
    # Et al. and sur. need a dot at the end
    " sur ": " sur. ",
    " et al ": " et al. ",
    # A1 and A2 is the same as A1 & A2, default to &
    " and ": " & ",
    # For the purposes of detecting duplicates, "sur." and "suradnici" are the same
    "suradnici": "sur.",
    "suradnika": "sur.",
}

for index_no, citation in enumerate(complete_list):
    # Remove uneccessary characters
    for char in chars_to_remove:
        complete_list[index_no] = complete_list[index_no].replace(char, "")
    # Change several phrases
    for key in phrases_to_adjust:
        complete_list[index_no] = complete_list[index_no].replace(key, phrases_to_adjust[key])
    # Remove leading and trailing spaces with strip() to not confuse the duplicate detection
    complete_list[index_no] = complete_list[index_no].strip()


# Remove duplicates
# To keep - elements to keep
to_keep = []
# Temporary file - we'll put casefold strings (case insensitive) in here so we can check repeating citations
tmp = []
for index_no, citation in enumerate(complete_list):
    # If the current citation HASN'T been mentioned yet, add it to the list of citations to keep
    # - these will end up in the output file.
    # Furthermore, turn that same citation casefold and add it to the object which stores all gathered citations
    # in lowercase, for comparison. We need a separate file since we cannot return from all lowercase to actual case automatically.
    if citation.casefold() not in tmp:
        to_keep.append(citation)
        tmp.append(citation.casefold())

complete_list = to_keep
# Sort the list alphabetically, ignoring case
complete_list.sort(key=str.casefold)
complete_list


# Outputting in Excel ----

output_filename = "citations.xlsx"

# Create a file
workbook = xlsxwriter.Workbook(output_filename)

# Create a sheet
worksheet1 = workbook.add_worksheet()

# We'll write in the second column
# The first column is useful for marking certain citations as "done" or "double-check"
column = 1
# Start from the first row
row = 0

# Iterate through output list
for item in complete_list:
    # Perform writing in specified cell
    worksheet1.write(row, column, item)
    # Increment the value of row by one with each iteration.
    row += 1

workbook.close()

print(f"Success! A file called {output_filename} has been created.")
print(f"A total of {len(complete_list)} different citations have been recorded.")
print("Press Enter to end the program.")
input("")
