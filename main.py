from fastapi import FastAPI
from database import supabase
from routers.product_router import router as product_router
from routers.auth_router import router as auth_router

app = FastAPI(
    title= "FastAPI",
    description= "FastAPI Project",
    version= "1.0.0"
)

app.include_router(product_router)
app.include_router(auth_router)

@app.get('/')
def home():
    return {
        "message" : "FastAPI is running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

