import io
import yaml
import functools
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response, status

from .core.config import settings
from .middleware.logging import logger
from .schemas.responses import ROOT_RESPONSE_MODEL
from .schemas.code_samples import ROOT_CODE_SAMPLES, add_code_samples


# Setup FastAPI instance
app = FastAPI(
    swagger_ui_parameters={
        "showExtensions": False,
    }
)

# Set up CORS (Cross-Origin Resource Sharing)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/", responses=ROOT_RESPONSE_MODEL, tags=["Miscellaneous"])
@add_code_samples(ROOT_CODE_SAMPLES)
async def root() -> JSONResponse:
    """
    ```
    Default Route (Public)
    ```
    """
    logger.info(
        "%s - %s",
        "(Public)",
        "Root endpoint is called",
    )
    return JSONResponse(
        content={"message": "Hello World!"}, status_code=status.HTTP_200_OK
    )


# Generating OpenAPI schema
summary = "Utilities API for converting .docx files into .pdf files"
description = "Apart from the response codes specified in each API, the API server may respond with certain 4xx and 5xx error codes which are related to common API Gateway behaviours."
tags_metadata = [
    {
        "name": "Miscellaneous",
        "description": "Default API endpoints",
    },
    {
        "name": "Auth",
        "description": "API endpoints for managing user authentication and authorization.",
    },
]


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.API_VERSION,
        summary=summary,
        description=description,
        tags=tags_metadata,
        routes=app.routes,
        contact={
            "name": settings.NAME,
            "email": settings.EMAIL,
        },
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    # Iterate through all routes and methods
    for route in app.routes:
        if (
            ".json" not in route.path
            and ".yaml" not in route.path
            and "/docs" not in route.path
            and "/redoc" not in route.path
        ):
            for method in route.methods:
                method_lower = method.lower()
                if method_lower in openapi_schema["paths"][route.path]:
                    endpoint = getattr(route, "endpoint", None)
                    if endpoint and hasattr(endpoint, "__code_samples__"):
                        code_samples = getattr(endpoint, "__code_samples__")
                        if method_lower in openapi_schema["paths"][route.path]:
                            openapi_schema["paths"][route.path][method_lower][
                                "x-codeSamples"
                            ] = code_samples

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi


# Endpoint to serve OpenAPI schema in YAML format
@app.get("/openapi.yaml", include_in_schema=False)
@functools.lru_cache()
def read_openapi_yaml() -> Response:
    openapi_json = app.openapi()
    yaml_s = io.StringIO()
    yaml.dump(openapi_json, yaml_s)
    return Response(yaml_s.getvalue(), media_type="text/yaml")
