import asyncio
from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from urlguardian.dependecies import URLListManager


class URLCheckRequest(BaseModel):
    url: str


class URLAddRequest(BaseModel):
    url: str


url_guardian_app = FastAPI()


# Dependency

@url_guardian_app.on_event("startup")
def startup_event():
    url_manager = URLListManager()
    url_guardian_app.state.url_manager = url_manager
    asyncio.create_task(url_manager.periodic_update_url_list())


# Mount static directory
url_guardian_app.mount("/static", StaticFiles(directory="static"), name="static")


@url_guardian_app.get("/healthz")
def health_check():
    return {"status": "ok"}


# Serve HTML file from the root route
@url_guardian_app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r") as file:
        return HTMLResponse(content=file.read())


@url_guardian_app.post("/add-url")
async def add_url(url_add_request: URLAddRequest, request: Request):
    url = url_add_request.url
    url_manager = request.app.state.url_manager

    # Logic to add the URL
    url_manager.add_url(url)  # Assuming you have a method `add_url` in URLListManager

    return {"status": "URL added to the list"}


@url_guardian_app.post("/check-url")  # Note the change to a POST request
async def check_url(url_check_request: URLCheckRequest, request: Request):
    url = url_check_request.url
    url_manager = request.app.state.url_manager
    if url_manager.check_url(url):
        return {"status": "URL is in the list"}
    else:
        return {"status": "URL not found"}
