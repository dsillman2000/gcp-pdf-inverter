import subprocess
from pathlib import Path

import fsspec
import gcsfs
from inversion.config import Settings

settings = Settings()


def save_temp_file(content: bytes, uuid: str, basename: str) -> Path:
    """
    Save the content to a temporary file and return its path.
    """
    local_dir = get_temp_dir(uuid, checked=False)
    local_dir.mkdir(parents=True, exist_ok=True)
    local_path = local_dir / basename
    with open(local_path, "wb") as f:
        f.write(content)
    return local_path


def purge_temp_files(uuid: str):
    """
    Purge the temporary files for the given UUID.
    """
    local_dir = get_temp_dir(uuid, checked=False)
    if not local_dir.exists():
        return
    for file in local_dir.iterdir():
        file.unlink()
    local_dir.rmdir()


def get_temp_dir(uuid: str, checked: bool = True) -> Path:
    """
    Get the path to the temporary directory for the given UUID.
    """
    temp_dir = Path(__file__).parent.parent / "storage"
    temp_dir.mkdir(parents=True, exist_ok=True)
    local_dir = temp_dir / uuid
    if checked and (not local_dir.exists() or not local_dir.is_dir()):
        raise FileNotFoundError(f"Local directory {local_dir} does not exist or is not a directory.")
    return local_dir


def get_temp_file(uuid: str, basename: str, checked: bool = True) -> Path:
    """
    Get the path to a temporary file for the given UUID and basename.
    """
    local_dir = get_temp_dir(uuid, checked)
    local_path = local_dir / basename
    if checked and not local_path.exists():
        raise FileNotFoundError(f"Local file {local_path} does not exist.")
    return local_path


def download_file(uuid: str):

    def _download_file_local(uuid: str):
        return get_temp_file(uuid, "pre.pdf")

    def _download_file_gcs(uuid: str):
        gcs_path = f"gs://{settings.GCS_BUCKET}/{uuid}/pre.pdf"
        fs = gcsfs.GCSFileSystem(project=settings.GCS_PROJECT)
        if not fs.exists(gcs_path):
            raise FileNotFoundError(f"GCS file {gcs_path} does not exist.")
        with fs.open(gcs_path, "rb") as f:
            content = f.read()
            return save_temp_file(content, uuid, "pre.pdf")

    match settings.STORAGE_BACKEND:
        case "local":
            return _download_file_local(uuid)
        case "gcs":
            return _download_file_gcs(uuid)
        case _:
            raise ValueError(f"Unsupported storage backend: {settings.STORAGE_BACKEND}")


def invert_file(uuid: str):
    _local_file = get_temp_file(uuid, "pre.pdf")
    _inverted_path = get_temp_file(uuid, "inverted.pdf", checked=False)
    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        f"-sOutputFile={str(_inverted_path)}",
        "-dNOPAUSE",
        "-dBATCH",
        "-dSAFER",
        "-c",
        "<< /Install { { 1 exch sub } settransfer } >> setpagedevice",
        "-f",
        str(_local_file),
    ]

    """
    gs -sDEVICE=pdfwrite -sOutputFile=inverted.pdf -dNOPAUSE -dBATCH -dSAFER -c '<< /Install { { 1 exch sub } settransfer } >> setpagedevice' -f pre.pdf
    """

    process = subprocess.Popen(cmd)  # , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise RuntimeError(f"gs command failed with error: {stderr.decode()}\n{stdout.decode()}")
    return _inverted_path


def upload_file(uuid: str):
    def _upload_file_local(uuid: str):
        inverted_path = get_temp_file(uuid, "inverted.pdf")
        return inverted_path

    def _upload_file_gcs(uuid: str):
        gcs_path = f"gs://{settings.GCS_BUCKET}/{uuid}/inverted.pdf"
        fs = gcsfs.GCSFileSystem(project=settings.GCS_PROJECT)
        inverted_path = get_temp_file(uuid, "inverted.pdf")
        with fs.open(gcs_path, "wb") as f:
            with open(inverted_path, "rb") as local_file:
                f.write(local_file.read())
        return inverted_path

    match settings.STORAGE_BACKEND:
        case "local":
            return _upload_file_local(uuid)
        case "gcs":
            return _upload_file_gcs(uuid)
        case _:
            raise ValueError(f"Unsupported storage backend: {settings.STORAGE_BACKEND}")
