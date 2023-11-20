from textual.document._document import Document
from textual.document._wrapped_document import WrappedDocument

SIMPLE_TEXT = "1234567\n12345\n123456789\n"


def test_wrapped_document_lines():
    document = Document(SIMPLE_TEXT)
    wrapped_document = WrappedDocument(document, width=4)

    assert wrapped_document.lines == [
        ["1234", "567"],
        ["1234", "5"],
        ["1234", "5678", "9"],
        [""],
    ]


def test_wrapped_document_refresh_range():
    document = Document(SIMPLE_TEXT)
    wrapped_document = WrappedDocument(document, width=4)

    # Before the document was edited, it wraps as normal.
    assert wrapped_document.lines == [
        ["1234", "567"],
        ["1234", "5"],
        ["1234", "5678", "9"],
        [""],
    ]

    start_location = (1, 0)
    old_end_location = (3, 0)

    edit_result = document.replace_range(start_location, old_end_location, "123")

    # Inform the wrapped document about the range impacted by the edit
    wrapped_document.recompute_range(
        start_location, old_end_location, edit_result.end_location
    )

    # Now confirm the resulting wrapped version is as we would expect
    assert wrapped_document.lines == [["1234", "567"], ["1234"], [""]]
