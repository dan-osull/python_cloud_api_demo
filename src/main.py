from PIL import UnidentifiedImageError
from fastapi import FastAPI, Response, UploadFile, HTTPException
from fastapi.responses import HTMLResponse

from src.image_handling import replace_faces_with_cat

app = FastAPI()


@app.post("/images")
def replace_faces_with_cat_api(image: UploadFile) -> Response:
    try:
        image_bytes = replace_faces_with_cat(image)
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="UnidentifiedImageError")
    return Response(content=image_bytes, media_type="image/webp")


@app.get("/")
def home_page() -> HTMLResponse:
    with open("assets/index.html") as file:
        return HTMLResponse(content=file.read())
