#!/usr/bin/env python3
from fastapi import FastAPI
import uvicorn
app = FastAPI()
@app.get("/health")
def health(): return {"status": "active"}
if __name__ == "__main__": uvicorn.run(app, host="0.0.0.0", port=8000)
