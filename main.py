from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def homePage():
    return {'status':'homepage'}