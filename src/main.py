from PIL import UnidentifiedImageError
from fastapi import FastAPI, Response, UploadFile, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from src.image_handling import replace_faces_with_cats

app = FastAPI(
    title="Human Face Improvement System (cat.osull.com)",
    description="[See GitHub for code](https://github.com/dan-osull/python_cloud_api_demo)",
)


class RecentImageStore(BaseModel):
    """
    In-memory store for the most recent image.
    For demo only, as data is lost on deploy and won't be shared between instances.
    """

    webp_image: bytes | None = None


recent_image = RecentImageStore()


@app.post("/convert", responses={400: {"detail": "Bad image data"}})
def replace_faces_with_cats_api(image: UploadFile) -> Response:
    try:
        image_bytes = replace_faces_with_cats(image)
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Bad image data")
    recent_image.webp_image = image_bytes
    return Response(content=image_bytes, media_type="image/webp")


@app.get("/recent", responses={404: {"detail": "No recent image"}})
def get_most_recent_image_api() -> Response:
    if recent_image.webp_image is None:
        raise HTTPException(status_code=404, detail="No recent image")
    return Response(content=recent_image.webp_image, media_type="image/webp")


@app.get("/")
def home_page() -> RedirectResponse:
    return RedirectResponse("/docs")
