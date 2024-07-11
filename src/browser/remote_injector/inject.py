import asyncio
import inspect
import socket
from pathlib import Path

import uvicorn
from jinja2 import Environment
from playwright.async_api import (
    BrowserContext,
    Page,
)

from .injector import Injector
from .server import RemoteInvokeServer


def _get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        port = s.getsockname()[1]
        return port


def _generate_script(injector: Injector) -> str:
    result = ""
    for class_name, class_ in injector:
        if class_name != "_":
            result += (
                f"class {class_name} {{}}\n"
                f"globalThis.{class_name} = {class_name};\n"
            )
        for method_name, method in class_.items():
            if class_name == "_":
                result += (
                    f"{method_name} = "
                    f"function({','.join(inspect.signature(method).parameters)})"
                    "{return "
                    f'invokeRemoteFunction("{method_name}",'
                    "null,"
                    f'{{{",".join(
                        f'"{para}":{para}' for para
                        in inspect.signature(method).parameters
                    )}}}'
                    ").result};"
                    "\n"
                    f"globalThis.{method_name} = {method_name};\n"
                )
            else:
                result += (
                    f"{class_name}.{method_name} = "
                    f"function({','.join(inspect.signature(method).parameters)})"
                    "{return "
                    f'invokeRemoteFunction("{class_name}.{method_name}",'
                    "null,"
                    f'{{{",".join(
                        f'"{para}":{para}' for para
                        in inspect.signature(method).parameters
                    )}}}'
                    ").result};"
                    "\n"
                )
    return result


async def _inject_javascript(
    target: Page | BrowserContext, injector: Injector, port: int
) -> None:
    with open(
        Path(__file__).resolve().parent
        / "template"
        / "invokeRemoteFunction.js",
        encoding="utf-8",
    ) as file:
        await target.add_init_script(
            Environment().from_string(file.read()).render(port=port)
        )
    await target.add_init_script(_generate_script(injector))


async def _override_cors_restrictions(
    target: Page | BrowserContext, port: int
) -> None:
    async def override_cors(route, request):
        url = request.url
        if f"localhost:{port}" in url or f"127.0.0.1:{port}" in url:
            await route.continue_()
        else:
            response = await target.request.fetch(request)
            headers = response.headers
            headers["Access-Control-Allow-Origin"] = "*"
            await route.fulfill(response=response, headers=headers)

    await target.route("**/*", override_cors)


async def inject(target: Page | BrowserContext, injector: Injector) -> None:
    port = _get_free_port()
    server = uvicorn.Server(
        uvicorn.Config(
            RemoteInvokeServer(injector=injector).app,
            port=port,
            log_level="warning",
        )
    )

    async def on_close():
        await server.shutdown()

    asyncio.create_task(server.serve())
    await _override_cors_restrictions(target, port)
    await _inject_javascript(target, injector, port)

    target.once("close", on_close)
