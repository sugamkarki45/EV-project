from fastapi import APIRouter, Depends, UploadFile, File
from typing import List

router = APIRouter()

@router.post("/submit")
async def submit_kyc(
    id_type: str,
    front: UploadFile = File(...),
    back: UploadFile = File(None),
    selfie: UploadFile = File(...)
):
    # Simulation: upload to S3, call AWS Rekognition
    return {"status": "pending", "message": "KYC submitted for review"}

@router.get("/status")
async def get_kyc_status():
    return {"status": "verified"}
