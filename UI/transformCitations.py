import UI.messages as ms

# For display and saving to .txt, visually separate wider citations
def citations_to_string_pretty(narrower_citations, wider_citations):
  citation_string = []
  [citation_string.append(citation + "\n") for citation in narrower_citations.citations]
  if len(wider_citations.citations) > 0:
      citation_string.append("\n" + ms.break_with_lines + \
                             "\nLonger citations detected:\n\n")
      [citation_string.append(citation + "\n") for citation in wider_citations.citations]
  results = "".join(citation_string)
  
  # Remove newline at end, it counts as one character
  results = results[:-1]
  return(results)