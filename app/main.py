from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routes.user import user_router
from app.routes.post import post_router




app = FastAPI(title="Blog Platform")

@app.get("/")
def health_check():
    return JSONResponse(content = {"message": "Api's Running Successfully"})

app.include_router(user_router, prefix= "/user", tags=["User"])
app.include_router(post_router, prefix= "/Blog", tags=["Blog"])