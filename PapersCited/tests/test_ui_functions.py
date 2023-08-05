from UI.fileManipulation import shorten_filename

def test_shortening_names():
    short_name = "aeiou"
    long_name = "0123456789" + "0123456789" + "0123456789" + "0123456789" + "0123456789"
    
    assert shorten_filename(short_name) == short_name
    assert shorten_filename(short_name, 4) == "a..."
    assert shorten_filename(short_name, 5) == short_name
    
    assert shorten_filename(long_name, 50) == long_name
    assert shorten_filename(long_name, 5) == "01..."
    assert shorten_filename(long_name, 10) == "0123456..."
    