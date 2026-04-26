from fastapi import FastAPI

app =FastAPI()

@app.get("/")
def hello():
    return {"message":"Hello FastApi"}

@app.get("/about")
def about():
    return {"about page": "this is about route"}