from fastapi import FastAPI

app = FastAPI()

@app.get('/files/{file_path:path}')
def files(file_path: str):
    return {'file_path': file_path}