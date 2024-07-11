from fastapi import Body, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from .injector import Injector


class RemoteInvokeServer:
    app: FastAPI
    injector: Injector

    def __init__(
        self, app: FastAPI | None = None, injector: Injector | None = None
    ) -> None:
        if not app:
            app = FastAPI(docs_url=None, redoc_url=None)
        if not injector:
            injector = Injector()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.app = app
        self.injector = injector
        self.register_routers()

    def register_routers(self):
        @self.app.post("/invoke/{callable_}")
        async def invoke_function(
            callable_: str,
            args: list | None = Body(None),
            kwargs: dict | None = Body(None),
        ):
            if callable_ in self.injector:
                try:
                    if not args:
                        args = []
                    if not kwargs:
                        kwargs = {}
                    return jsonable_encoder(
                        {
                            "status": "success",
                            "result": self.injector[callable_](
                                *args, **kwargs
                            ),
                        }
                    )
                except Exception as e:  # pylint: disable = W0718
                    return jsonable_encoder(
                        {
                            "status": "fail",
                            "detail": f"{type(e).__name__}: {str(e)}",
                        }
                    )
            else:
                return jsonable_encoder(
                    {
                        "status": "fail",
                        "detail": "not found",
                    }
                )
