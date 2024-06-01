import uvicorn
from fastapi import FastAPI,APIRouter

from config.config import Settings
from routers import home_page

app = FastAPI(title=Settings.PROJECT_NAME,
              description=Settings.PROJECT_DESC,
              version=Settings.PROJECT_VERSION,

              )


router = APIRouter(prefix="/api/v1")

@router.get("/")
def initial_route():
    return {"msg": "yo bro!!!"}


@router.get("/healthCheck", status_code=200, tags=["Service Health Check API"])
def health_check():
    return {"message": "Service is Up"}

app.include_router(router)
app.include_router(home_page.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app,host='0.0.0.0',port=8080)
