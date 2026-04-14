import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from main import app  

client = TestClient(app)


# content type tests
@pytest.mark.parametrize(
    "filename, content_type, expected_status_code",
    [
        pytest.param("resume.docx", "application/vnd.openxmlformats", 400, id="docx_not_allowed"),
        pytest.param("resume.txt",  "text/plain", 400, id="txt_not_allowed"),
        pytest.param("resume.png",  "image/png", 400, id="png_not_allowed"),
        pytest.param("resume.csv",  "text/csv", 400, id="csv_not_allowed"),
        pytest.param("resume.pdf",  "application/pdf", 200, id="pdf_allowed"),
    ]
)
def test_content_type(filename, content_type, expected_status_code):
    # Only mock for valid PDF case
    if content_type == "application/pdf":
        with patch("app.routers.resume.fitz.open") as mock_fitz_open:
            mock_page = Mock()
            mock_page.get_text.return_value = "Valid resume text"
            mock_fitz_open.return_value = [mock_page]

            response = client.post(
                "/resume",
                files={"file": (filename, b"some bytes", content_type)},
            )
    else:
        response = client.post(
            "/resume",
            files={"file": (filename, b"some bytes", content_type)},
        )

    assert response.status_code == expected_status_code

# pdf content tests
@pytest.mark.parametrize(
    "pages_text, expected_status_code",
    [
        pytest.param(["   "],        400, id="spaces_only"),
        pytest.param(["\n", "\t"],   400, id="whitespace_chars"),
        pytest.param(["", "", ""],   400, id="all_empty_pages"),
        pytest.param(["Valid resume content"], 200, id="valid_content_success"),
    ]
)
@patch("app.routers.resume.fitz.open")
def test_pdf_content(mock_fitz_open, pages_text, expected_status_code):
    # create mock pages
    mock_pages = []
    for text in pages_text:
        page = Mock()
        page.get_text.return_value = text
        mock_pages.append(page)
    mock_fitz_open.return_value = mock_pages
    response = client.post("/resume",files={"file": ("resume.pdf", b"%PDF-blank", "application/pdf")},)
    assert response.status_code == expected_status_code