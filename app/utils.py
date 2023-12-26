import hashlib
import uuid

from time import time


def generate_unique_promise_id() -> str:
    timestamp = int(time() * 1000)
    unique_id = f"{timestamp}_{uuid.uuid4()}"
    return unique_id


def calculate_actual_md5(file_path: str) -> str:
    with open(file_path, "rb") as file:
        md5_hash = hashlib.md5()

        chunk_size = 5000
        for chunk in iter(lambda: file.read(chunk_size), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()
