from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from inversion.main import app
from inversion.utils import purge_temp_files, save_temp_file


@pytest.fixture(scope="session")
def client():
    """
    Create a test client for the FastAPI app.
    """
    yield TestClient(app)


@pytest.fixture(scope="session")
def original_test_pdf_content() -> bytes:
    test_path = Path(__file__).parent / "data" / "test.pdf"
    if not test_path.exists():
        raise FileNotFoundError(f"Test PDF file not found at {test_path}")
    return test_path.read_bytes()


@pytest.fixture(scope="session")
def test_uuid():
    return "test-uuid"


@pytest.fixture(scope="session")
def test_uuid_pre(test_uuid, original_test_pdf_content):
    save_temp_file(original_test_pdf_content, test_uuid, "pre.pdf")
    yield test_uuid
    purge_temp_files(test_uuid)


@pytest.fixture(scope="session")
def test_uuid_inverted(test_uuid, original_test_pdf_content):
    save_temp_file(original_test_pdf_content, test_uuid, "inverted.pdf")
    yield test_uuid
    purge_temp_files(test_uuid)
