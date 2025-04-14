# backend

Backend infrastructure for the project. Contains two subfolders:

1. `storage`: Contains the FastAPI storage service for routing files between frontend and the inversion service.
2. `inversion`: Contains the FastAPI inversion service that uses Ghostscript to invert the colors of the PDF files.
