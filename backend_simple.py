import os
import json
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI(title="Simple Contract Manager")

# Directories and files
CONTRACTS_DIR = "contracts"
DB_FILE = "db.json"

# Create contracts directory if it doesn't exist
os.makedirs(CONTRACTS_DIR, exist_ok=True)

# Helper to read/write to the JSON database
def read_db():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def write_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.post("/contracts/", summary="Create a new contract")
def create_contract(client: str, project: str, file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .docx is accepted.")

    db = read_db()
    contract_id = len(db) + 1
    file_path = os.path.join(CONTRACTS_DIR, f"{contract_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_contract = {
        "id": contract_id,
        "client": client,
        "project": project,
        "filename": file.filename,
        "path": file_path
    }
    db.append(new_contract)
    write_db(db)

    return {"message": "Contract created successfully", "contract": new_contract}

@app.get("/contracts/", summary="List all contracts")
def list_contracts():
    return read_db()

@app.get("/contracts/{contract_id}", summary="Download a contract file")
def download_contract(contract_id: int):
    db = read_db()
    contract = next((c for c in db if c["id"] == contract_id), None)

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found.")

    return FileResponse(path=contract["path"], filename=contract["filename"], media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
