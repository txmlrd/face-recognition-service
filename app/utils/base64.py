from extensions import base64, Image, BytesIO, os

def base64_to_image(base64_string, filename):
    if base64_string.startswith("data:image"):
        base64_string = base64_string.split(",")[1]  #delete header data
    img_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(img_data))
    image.save(filename)
    return filename