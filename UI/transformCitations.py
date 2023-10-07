import UI.messages as ms

def citations_to_string(narrower_citations, wider_citations):
  citation_string = []
  [citation_string.append(citation + "\n") for citation in narrower_citations.citations]
  if len(wider_citations.citations) > 0:
      [citation_string.append(citation + "\n") for citation in wider_citations.citations]
  results = "".join(citation_string)
  return(results)

# For display and saving to .txt, visually separate wider citations
def citations_to_string_pretty(narrower_citations, wider_citations):
  citation_string = []
  [citation_string.append(citation + "\n") for citation in narrower_citations.citations]
  if len(wider_citations.citations) > 0:
      citation_string.append("\n" + ms.break_with_lines + \
                             "\nLonger citations detected:\n\n")
      [citation_string.append(citation + "\n") for citation in wider_citations.citations]
  results = "".join(citation_string)
  return(results)