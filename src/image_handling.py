import random
from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile

from deepface import DeepFace
from fastapi import UploadFile
from PIL import Image
from pydantic import BaseModel

MAX_IMAGE_PIXELS = 1000
CAT_FACE_GROWTH_FACTOR = 1.5
CAT_IMAGE_DIR = Path("assets/cat_photos")


class FaceLocation(BaseModel):
    x: int
    y: int
    w: int
    h: int


def replace_faces_with_cat(image_in: UploadFile) -> bytes:
    # Begin by converting the user-provided image to our format and size.
    # Raises `UnidentifiedImageError` if given bad data.
    webp_image = _resize_image_and_convert_to_webp(image_in=image_in.file.read())
    with NamedTemporaryFile(mode="wb") as tempfile:
        tempfile.write(_convert_pillow_image_to_bytes(webp_image))
        face_locations = _get_face_locations(tempfile.name)
    image_with_faces_replaced = _replace_face_in_image(
        image=webp_image, face_locations=face_locations
    )
    return _convert_pillow_image_to_bytes(image_with_faces_replaced)


def _convert_pillow_image_to_bytes(image: Image.Image) -> bytes:
    image_out = BytesIO()
    image.save(image_out, format="WEBP")
    return image_out.getvalue()


def _resize_image_and_convert_to_webp(image_in: bytes) -> Image.Image:
    image = Image.open(BytesIO(image_in))
    image.thumbnail(size=(MAX_IMAGE_PIXELS, MAX_IMAGE_PIXELS))
    return image


def _get_face_locations(image_path: str) -> list[FaceLocation]:
    faces = DeepFace.extract_faces(img_path=image_path, enforce_detection=False)
    return [FaceLocation(**item["facial_area"]) for item in faces]


def _get_random_cat_photo(w: int, h: int) -> Image.Image:
    cat_photo_path = random.choice(list(CAT_IMAGE_DIR.iterdir()))
    image = Image.open(cat_photo_path)
    image.thumbnail(size=(w * CAT_FACE_GROWTH_FACTOR, h * CAT_FACE_GROWTH_FACTOR))
    return image


def _replace_face_in_image(
    image: Image.Image, face_locations: list[FaceLocation]
) -> Image.Image:
    for face in face_locations:
        cat_photo = _get_random_cat_photo(w=face.w, h=face.h)
        y_offset = max((0, (cat_photo.height - face.h) / 2))
        y_location = int(face.y - y_offset)
        x_offset = max((0, (cat_photo.width - face.w) / 2))
        x_location = int(face.x - x_offset)
        image.paste(im=cat_photo, box=(x_location, y_location), mask=cat_photo)
    return image
