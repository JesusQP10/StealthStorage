from PIL import Image
import os

def compress_image(file_path: str, quality: int = 65) -> int:
    try:
        size_before = os.path.getsize(file_path)
        img = Image.open(file_path)
        img.save(file_path, "JPEG", optimize=True, quality=quality)
        size_after = os.path.getsize(file_path)
        return size_before - size_after
    except Exception:
        return 0