import uvicorn

from src import API


app = API().create()
    

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)
