import os


def path_static_image(messenger, phone, api_id):
    path = f"static/{messenger}/img/{phone}_{api_id}"
    filename = "img.png"
    full_path = os.path.join(path, filename)
    if not os.path.exists(path):
        os.mkdir(path)
    return full_path

