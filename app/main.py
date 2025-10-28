from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.products import router as products_router


app = FastAPI()

'''
@app.on_event("startup")
async def startup_event():
    await RabbitMQConnectionManager.get_connection()


@app.on_event("shutdown")
async def shutdown_event():
    await RabbitMQConnectionManager.close_connection()
'''

@app.get("/")
async def root():
    return {"message": "Hello, world!"}


app.include_router(auth_router)
app.include_router(products_router)
