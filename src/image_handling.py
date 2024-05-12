import random
from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import BinaryIO

from deepface import DeepFace
from PIL import Image
from pydantic import BaseModel

MAX_IMAGE_PIXELS = 1000
FACE_EXPAND_PERCENTAGE = 50
CAT_IMAGE_DIR = Path("assets/cat_photos")


class FaceLocation(BaseModel):
    x: int
    y: int
    w: int
    h: int


def replace_faces_with_cats(image_in: BinaryIO) -> bytes:
    """
    Raises `UnidentifiedImageError` if given bad data.

    Returns WebP format image.
    """
    image = _resize_image(image_in=image_in.read())
    with NamedTemporaryFile(mode="wb") as tempfile:
        tempfile.write(_convert_image_to_webp_bytes(image))
        face_locations = _get_face_locations(tempfile.name)
    image_with_faces_replaced = _replace_faces_in_image(
        image=image, face_locations=face_locations
    )
    return _convert_image_to_webp_bytes(image_with_faces_replaced)


def _resize_image(image_in: bytes) -> Image.Image:
    image = Image.open(BytesIO(image_in))
    image.thumbnail(size=(MAX_IMAGE_PIXELS, MAX_IMAGE_PIXELS))
    return image


def _convert_image_to_webp_bytes(image: Image.Image) -> bytes:
    image_out = BytesIO()
    image.save(image_out, format="WEBP")
    return image_out.getvalue()


def _get_face_locations(image_path: str) -> list[FaceLocation]:
    faces = DeepFace.extract_faces(
        img_path=image_path,
        enforce_detection=False,
        expand_percentage=FACE_EXPAND_PERCENTAGE,
    )
    return [FaceLocation(**item["facial_area"]) for item in faces]


def _replace_faces_in_image(
    image: Image.Image, face_locations: list[FaceLocation]
) -> Image.Image:
    for face in face_locations:
        cat_photo = _get_random_cat_photo(w=face.w, h=face.h)
        image.paste(im=cat_photo, box=(face.x, face.y), mask=cat_photo)
    return image


def _get_random_cat_photo(w: int, h: int) -> Image.Image:
    cat_photo_path = random.choice(list(CAT_IMAGE_DIR.iterdir()))
    image = Image.open(cat_photo_path)
    image.thumbnail(size=(w, h))
    return image
