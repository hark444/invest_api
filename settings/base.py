import os
from environs import Env


_ENV = os.environ.get("ENV")

env = Env()

if _ENV in ("local", "docker"):
    env.read_env(f".env.{_ENV}", override=True)
else:
    env.read_env()
