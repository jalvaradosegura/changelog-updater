from changelog_updater.main import prepend_a_line_to_text


def test_prepend_a_line():
    text = "Some random text"
    result = prepend_a_line_to_text(text, "Hi,")
    assert result == f"Hi,\n{text}"
