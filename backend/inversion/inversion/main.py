from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from inversion.config import Settings
from inversion.utils import download_file, invert_file, upload_file

app = FastAPI()
# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = Settings()


@app.post("/download/{uuid}")
async def download(uuid: str):
    """
    Download the file from the given remote storage path onto the local disk of the inversion service.
    """
    assert settings.STORAGE_BACKEND == "local", "Only local is supported right now."
    try:
        # Placeholder for actual download logic
        downloaded_file = download_file(uuid)
        return JSONResponse(content={"message": f"Downloaded file to path: {str(downloaded_file)}"})
    except Exception as e:
        raise e
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/invert/{uuid}")
async def invert(uuid: str):
    """
    Invert the PDF file on local disk with the given UUID.
    """
    assert settings.STORAGE_BACKEND == "local", "Only local is supported right now."
    try:
        # Placeholder for actual inversion logic
        inverted_file = invert_file(uuid)
        inverted_msg = f"Inverted file with UUID: {uuid}"
        return JSONResponse(content={"message": inverted_msg})
    except Exception as e:
        raise e
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/upload/{uuid}")
async def upload(uuid: str):
    """
    Upload the inverted PDF file to the remote storage, deleting the local copy.
    """
    assert settings.STORAGE_BACKEND == "local", "Only local is supported right now."
    try:
        # Placeholder for actual upload logic
        uploaded_file = upload_file(uuid)
        uploaded_image = f"Uploaded PDF file with UUID: {uuid}"
        # Here you would typically call your upload function
        return JSONResponse(content={"message": uploaded_image})
    except Exception as e:
        raise e
        return JSONResponse(status_code=500, content={"error": str(e)})
