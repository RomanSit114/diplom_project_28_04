from uvicorn import run
from uvicorn_config import config

if __name__ == "__main__":
    run(**config)