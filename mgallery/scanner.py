import os
import glob
import logging

from concurrent import futures

from mgallery.image import process_image_list
from mgallery.settings import GALLERY_PATH
from mgallery.database import Database

logger = logging.getLogger(__name__)


def get_file_chunks(num_cores: int = os.cpu_count()) -> list[list[str]]:
    files = []
    for ext in ("**/*.jpg", "**/*.jpeg", "**/*.png", "**/*.gif"):
        files.extend(glob.glob(f"{GALLERY_PATH}/{ext}", recursive=True))
    chunk_size = len(files) // num_cores + 1
    return [files[i : i + chunk_size] for i in range(len(files))[::chunk_size]]  # noqa


def run_scanner(num_cores: int = os.cpu_count()):
    logger.info(f"Start scanning {GALLERY_PATH}")

    existing_items = Database().all()
    existing_images = (
        [f"{x['path']}/{x['name']}" for x in Database().all()] if existing_items else []
    )

    file_chunks = get_file_chunks(num_cores=num_cores)
    with futures.ProcessPoolExecutor(max_workers=num_cores) as executor:
        processes = []
        for i in range(num_cores):
            processes.append(
                executor.submit(process_image_list, file_chunks[i], existing_images)
            )
    for _ in futures.as_completed(processes):
        """Wait while all processes will be completed"""
    logger.info("All threads are completed")
