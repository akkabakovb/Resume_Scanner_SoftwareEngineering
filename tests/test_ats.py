import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from main import app
from app.models.schemas import ATSResult

client = TestClient(app)

VALID_ATS_RESULT = ATSResult(
    ats_score=85,
    matched_keywords=["Python", "FastAPI"],
    missing_keywords=["Docker"],
    suggestions=["Add Docker experience"],
    verdict="Likely to pass ATS screening",
)


# content type tests
@pytest.mark.parametrize(
    "filename, content_type, expected_status_code",
    [
        pytest.param("resume.docx", "application/vnd.openxmlformats", 400, id="docx_not_allowed"),
        pytest.param("resume.txt",  "text/plain", 400, id="txt_not_allowed"),
        pytest.param("resume.png",  "image/png", 400, id="png_not_allowed"),
        pytest.param("resume.pdf",  "application/pdf", 200, id="pdf_allowed"),
    ]
)
def test_ats_content_type(filename, content_type, expected_status_code):
    if content_type == "application/pdf":
        with patch("app.routers.ats.fitz.open") as mock_fitz_open, \
             patch("app.routers.ats._run_ats_analysis") as mock_run_ats:
            mock_page = Mock()
            mock_page.get_text.return_value = "Valid resume content"
            mock_fitz_open.return_value = [mock_page]
            mock_run_ats.return_value = VALID_ATS_RESULT

            response = client.post(
                "/ats",
                files={"file": (filename, b"some bytes", content_type)},
                data={"job_description": "We need a Python developer with FastAPI experience."},
            )
    else:
        response = client.post(
            "/ats",
            files={"file": (filename, b"some bytes", content_type)},
            data={"job_description": "We need a Python developer with FastAPI experience."},
        )

    assert response.status_code == expected_status_code


# pdf content tests
@pytest.mark.parametrize(
    "pages_text, expected_status_code",
    [
        pytest.param(["   "],                  400, id="spaces_only"),
        pytest.param(["\n", "\t"],             400, id="whitespace_chars"),
        pytest.param(["", "", ""],             400, id="all_empty_pages"),
        pytest.param(["Valid resume content"], 200, id="valid_content_success"),
    ]
)
@patch("app.routers.ats.fitz.open")
def test_ats_pdf_content(mock_fitz_open, pages_text, expected_status_code):
    mock_pages = []
    for text in pages_text:
        page = Mock()
        page.get_text.return_value = text
        mock_pages.append(page)
    mock_fitz_open.return_value = mock_pages

    if expected_status_code == 200:
        with patch("app.routers.ats._run_ats_analysis") as mock_run_ats:
            mock_run_ats.return_value = VALID_ATS_RESULT
            response = client.post(
                "/ats",
                files={"file": ("resume.pdf", b"%PDF-blank", "application/pdf")},
                data={"job_description": "We need a Python developer with FastAPI experience."},
            )
    else:
        response = client.post(
            "/ats",
            files={"file": ("resume.pdf", b"%PDF-blank", "application/pdf")},
            data={"job_description": "We need a Python developer with FastAPI experience."},
        )

    assert response.status_code == expected_status_code


@patch("app.routers.ats.fitz.open")
def test_ats_empty_job_description(mock_fitz_open):
    mock_page = Mock()
    mock_page.get_text.return_value = "Valid resume content"
    mock_fitz_open.return_value = [mock_page]

    response = client.post(
        "/ats",
        files={"file": ("resume.pdf", b"%PDF-blank", "application/pdf")},
        data={"job_description": "   "},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Job description is empty or missing."


@patch("app.routers.ats.fitz.open")
@patch("app.routers.ats._run_ats_analysis")
def test_ats_openai_error(mock_run_ats, mock_fitz_open):
    mock_page = Mock()
    mock_page.get_text.return_value = "Valid resume content"
    mock_fitz_open.return_value = [mock_page]
    mock_run_ats.side_effect = HTTPException(status_code=500, detail="OpenAI API error: test error")

    response = client.post(
        "/ats",
        files={"file": ("resume.pdf", b"%PDF-blank", "application/pdf")},
        data={"job_description": "We need a Python developer with FastAPI experience."},
    )

    assert response.status_code == 500
