# Simple Contract Manager

This is a lightweight, database-free contract management system built with FastAPI.

## Dependencies
- `fastapi`
- `uvicorn`
- `python-multipart`

## How to Run
1. Install the required packages:
   ```bash
   pip install fastapi uvicorn python-multipart
   ```
2. Run the application:
   ```bash
   uvicorn backend_simple:app --reload
   ```

## API Endpoints
- `POST /contracts/`: Create a new contract.
- `GET /contracts/`: List all contracts.
- `GET /contracts/{contract_id}`: Download a contract file.
