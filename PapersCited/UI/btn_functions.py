import UI.fileManipulation as fm
from tkinter import filedialog

# Helper function for raising a pressed button
def fn_btn_release(event, btn):
  btn.config(relief = "raised")
  return("break")


def fn_btn_choose(event, btn_choose, master, data, text_component):
  btn_choose.config(relief="sunken")
  filename = filedialog.askopenfilename(
      title="Select a document to search for citations:"
  )
  data.set_new_filename(filename,
                            list_affected_wg=[master])
  try:
    reading_operation = fm.read_document(filename)

    message = reading_operation["status_message"]
    contents = reading_operation["document_text"]
    citations = fm.find_citations(contents)

  except Exception as e:
    error = str(e)
    data.reset_on_error(error, list_affected_wg=[text_component])
    return("break")

  data.set_new_results_citations(citations,
                                     list_affected_wg=[text_component])

  if message:
    data.warning_in_text_widget(message, list_affected_wg=[text_component])

  return("break")
