import pytest

import PapersCited

# Test class behavour

def test_PhrasesToChange_has_all_attributes():
  phrases = PapersCited.PhrasesToChange()
  assert isinstance(phrases.characters_to_exclude, list)
  assert isinstance(phrases.croatian_excluded_phrases, list)
  assert isinstance(phrases.english_excluded_phrases, list)
  assert isinstance(phrases.phrases_to_adjust, dict)
