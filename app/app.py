from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}

if __name__ == "__main__":
    print("🚀 Running at http://localhost:8000")
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
