from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def index():
    return {'data':{
        'name':"Prabesh"
    }}

@app.get("/about")
def about():
    return "This is a about page"
