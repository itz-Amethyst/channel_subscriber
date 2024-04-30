import os


def delete_image(cover):
    storage, path = cover.storage, cover.path
    if os.path.exists(path):
        storage.delete(path)