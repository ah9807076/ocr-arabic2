FROM python:3.8-slim\n\nWORKDIR /app\n\nCOPY requirements.txt requirements.txt\n\nRUN pip install -r requirements.txt\n\nCOPY . .\n\nEXPOSE 5000\n\nCMD ["python", "app.py"]
