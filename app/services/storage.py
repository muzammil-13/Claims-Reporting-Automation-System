import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from google.cloud import storage

# Load environment variables from .env file
load_dotenv()

GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")


def upload_file(file_path: Path, destination_name: Optional[str] = None) -> str:
    """
    Upload a file to the configured GCS bucket and return its public URL.
    """
    if not GCP_BUCKET_NAME:
        raise RuntimeError("GCP_BUCKET_NAME is not configured")

    client = storage.Client()
    bucket = client.bucket(GCP_BUCKET_NAME)
    destination = destination_name or file_path.name

    blob = bucket.blob(destination)
    blob.upload_from_filename(str(file_path))
    blob.make_public()

    return blob.public_url
