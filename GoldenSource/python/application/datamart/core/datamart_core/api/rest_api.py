"""REST API for the DataMart Market."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datamart_core.api.app_loader import AppLoader
from datamart_core.api.router.commands import router as router_commands
from datamart_core.api.router.coverage import router as router_coverage
from datamart_core.api.router.system import router as router_system
from datamart_core.app.model.abstract.error import DataMartError
from datamart_core.app.service.auth_service import AuthService
from datamart_core.app.service.system_service import SystemService
from datamart_core.env import Env

logger = logging.getLogger("uvicorn.error")

system = SystemService().system_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Startup event."""
    auth = "ENABLED" if Env().API_AUTH else "DISABLED"
    banner = rf"""
  /$$$$$$            /$$       /$$                          
 /$$__  $$          | $$      | $$                          
| $$  \__/  /$$$$$$ | $$  /$$$$$$$  /$$$$$$  /$$$$$$$       
| $$ /$$$$ /$$__  $$| $$ /$$__  $$ /$$__  $$| $$__  $$      GoldenSource DataMart v{system.version}
| $$|_  $$| $$  \ $$| $$| $$  | $$| $$$$$$$$| $$  \ $$      Authentication: {auth}
| $$  \ $$| $$  | $$| $$| $$  | $$| $$_____/| $$  | $$      
|  $$$$$$/|  $$$$$$/| $$|  $$$$$$$|  $$$$$$$| $$  | $$      
 \______/  \______/ |__/ \_______/ \_______/|__/  |__/      
                                                                                             
  /$$$$$$                                                   
 /$$__  $$                                                  
| $$  \__/  /$$$$$$  /$$   /$$  /$$$$$$   /$$$$$$$  /$$$$$$ 
|  $$$$$$  /$$__  $$| $$  | $$ /$$__  $$ /$$_____/ /$$__  $$
 \____  $$| $$  \ $$| $$  | $$| $$  \__/| $$      | $$$$$$$$
 /$$  \ $$| $$  | $$| $$  | $$| $$      | $$      | $$_____/
|  $$$$$$/|  $$$$$$/|  $$$$$$/| $$      |  $$$$$$$|  $$$$$$$
 \______/  \______/  \______/ |__/       \_______/ \_______/

"""
    logger.info(banner)
    yield


app = FastAPI(
    title=system.api_settings.title,
    description=system.api_settings.description,
    version=system.api_settings.version,
    terms_of_service=system.api_settings.terms_of_service,
    contact={
        "name": system.api_settings.contact_name,
        "url": system.api_settings.contact_url,
        "email": system.api_settings.contact_email,
    },
    license_info={
        "name": system.api_settings.license_name,
        "url": system.api_settings.license_url,
    },
    servers=[
        {
            "url": s.url,
            "description": s.description,
        }
        for s in system.api_settings.servers
    ],
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=system.api_settings.cors.allow_origins,
    allow_methods=system.api_settings.cors.allow_methods,
    allow_headers=system.api_settings.cors.allow_headers,
)
AppLoader.from_routers(
    app=app,
    routers=(
        [AuthService().router, router_system, router_coverage, router_commands]
        if Env().DEV_MODE
        else [router_commands]
    ),
    prefix=system.api_settings.prefix,
)


@app.exception_handler(Exception)
async def api_exception_handler(_: Request, exc: Exception):
    """Exception handler for all other exceptions."""
    if Env().DEBUG_MODE:
        raise exc
    logger.error(exc)
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
            "error_kind": exc.__class__.__name__,
        },
    )


@app.exception_handler(DataMartError)
async def datamart_exception_handler(_: Request, exc: DataMartError):
    """Exception handler for DataMart errors."""
    if Env().DEBUG_MODE:
        raise exc
    logger.error(exc.original)
    datamart_error = exc.original
    status_code = 400 if "No results" in str(datamart_error) else 500
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": str(datamart_error),
            "error_kind": datamart_error.__class__.__name__,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("market.api.rest_api:app", reload=True)
