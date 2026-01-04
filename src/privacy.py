from PIL import Image

def strip_metadata(file_path: str) -> None:
    try:
        image = Image.open(file_path)
        
        # Pylance cree que esto no es iterable, pero lo es.
        # Usamos 'type: ignore' para silenciar el falso error.
        data = list(image.getdata()) # type: ignore
        
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        image_without_exif.save(file_path)
    except Exception:
        pass