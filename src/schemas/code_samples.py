from ..core.config import settings


def add_code_samples(code_samples):
    def decorator(func):
        func.__code_samples__ = code_samples
        return func

    return decorator


BASE_URL = settings.BASE_URL
nl = "\n"
tab = "    "


ROOT_CODE_SAMPLES = [
    {
        "lang": "Shell",
        "source": f"curl --location --request GET '{BASE_URL}/'{nl}",
        "label": "curl",
    },
    {
        "lang": "Python",
        "source": f"import requests{nl}{nl}"
        f'url = "{BASE_URL}/"{nl}'
        f'response = requests.request("GET", url){nl}'
        f"print(response.text)",
        "label": "Python3",
    },
    {
        "lang": "Node.js",
        "source": f"const axios = require('axios');{nl}{nl}"
        f'const url = "{BASE_URL}/"{nl}{nl}'
        f"axios{nl}"
        f"{tab}.get(url){nl}"
        f"{tab}.then(response => {{{nl}"
        f"{tab}{tab}console.log(response.data);{nl}"
        f"{tab}}}).catch(error => {{{nl}"
        f"{tab}{tab}console.error(error);{nl}"
        f"{tab}}});",
        "label": "Node.js (axios)",
    },
]
