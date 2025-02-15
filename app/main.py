import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from app.adapters.ingoing.rest.routes import router

app = FastAPI(
    title="Property Service API",
    description="API für Immobilienoperationen",
    version="1.0.0",
    docs_url='/docs',
    redoc_url='/docs',
    openapi_url='/openapi.json',
    root_path='/api/property',
)

origins = [
    "http://localhost:3000", "http://localhost:80", "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, tags=["properties"])

@app.get("/")
async def root():
    """
    Test-Endpunkt, um sicherzustellen, dass die API läuft.
    """
    return {"message": "Property Service is running"}


@app.get("/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK
)
async def health():
    return {"status": "healthy"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8001)
