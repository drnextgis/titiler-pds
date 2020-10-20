"""titiler-pds app."""

from brotli_asgi import BrotliMiddleware
from mangum import Mangum

from titiler.errors import DEFAULT_STATUS_CODES, add_exception_handlers
from titiler.middleware import CacheControlMiddleware, TotalTimeMiddleware

from .routes import landsat, sentinel

from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="titiler-pds", version="0.1.0")

app.include_router(landsat.scenes.router, prefix="/scenes/landsat", tags=["Landsat 8"])
app.include_router(
    landsat.mosaicjson.router, prefix="/mosaicjson/landsat", tags=["Landsat 8"]
)

app.include_router(
    sentinel.scenes.router, prefix="/scenes/sentinel", tags=["Sentinel 2 COG"]
)
app.include_router(
    sentinel.mosaicjson.router, prefix="/mosaicjson/sentinel", tags=["Sentinel 2 COG"]
)

add_exception_handlers(app, DEFAULT_STATUS_CODES)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.add_middleware(BrotliMiddleware, minimum_size=0, gzip_fallback=True)
app.add_middleware(CacheControlMiddleware, cachecontrol="public, max-age=3600")
app.add_middleware(TotalTimeMiddleware)


@app.get("/healtz", description="Health Check", tags=["Health Check"])
def ping():
    """Health check."""
    return {"ping": "pong!"}


handler = Mangum(app, log_level="error")