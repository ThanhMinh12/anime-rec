import redis
import os
from dotenv import load_dotenv
import json

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def cache_get(key: str):
    value = redis_client.get(key)
    return json.loads(value) if value else None

def cache_set(key: str, data, expire_seconds: int = 3600):
    redis_client.setex(key, expire_seconds, json.dumps(data))
