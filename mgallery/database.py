import json
from collections import defaultdict

import redis

from mgallery.settings import REDIS_URL


class Database:
    def __init__(self):
        self.client = redis.from_url(REDIS_URL)

    def get(self, key: str) -> dict:
        return json.loads(self.client.get(key))

    def all(self, pattern: str = "*") -> list:
        return [self.get(key) for key in self.client.keys(pattern)]

    def duplicates(self) -> dict[str, list]:
        duplicates = defaultdict(list)
        for item in self.all():
            if item["phash"]:
                duplicates[item["phash"]].append(item)
        return {k: v for k, v in duplicates.items() if len(v) > 1}

    def create(
        self,
        path: str,
        name: str,
        phash: str = None,
        width: int = None,
        height: int = None,
        size: int = None,
    ):
        key = f"{phash}-{path}/{name}"
        value = json.dumps(
            {
                "path": path,
                "name": name,
                "phash": phash,
                "width": width,
                "height": height,
                "size": size,
            }
        )
        self.client.set(key, value)

    def delete(self, path: str, name: str):
        for key in self.client.keys(f"*{path}/{name}"):
            self.client.delete(key)
