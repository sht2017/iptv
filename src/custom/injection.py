from typing import Any

from browser import remote_injector
from config import CONFIG, context_data
from channel import Channel
from epg import Authenticator, AuthMethod, Credential

injector = remote_injector.Injector()


def _channel_parser(content: str):
    result = {}
    for item in content.replace('"', "").split(","):
        key, value = item.strip().split("=", 1)
        result[key] = (
            int(value)
            if key
            in [
                "UserChannelID",
                "TimeShift",
                "PositionX",
                "PositionY",
                "BeginTime",
                "Interval",
                "Lasting",
                "ChannelType",
                "TimeShiftLength",
                "FCCEnable",
                "FCCFunction",
                "ChannelFCCPort",
            ]
            else value
        )
    return result


@injector.register
class Authentication:
    @staticmethod
    def CTCGetAuthInfo(token: str) -> str:
        credential_config = CONFIG["epg"]["credential"]
        credential_kwargs = {
            "token": token,
            "user_id": credential_config["user_id"],
            "password": credential_config["password"],
            "ip": credential_config["ip"],
            "mac": credential_config["mac"],
            "product_id": credential_config["product_id"],
        }
        if "ctc" in credential_config:
            credential_kwargs["ctc"] = credential_config["ctc"]

        authenticator_kwargs = {"credential": Credential(**credential_kwargs)}
        if "authenticator" in CONFIG["epg"]:
            authenticator_config = CONFIG["epg"]["authenticator"]
            if "auth_method" in authenticator_config:
                authenticator_kwargs["auth_method"] = AuthMethod[
                    authenticator_config["auth_method"]
                ]
            if "salt" in authenticator_config:
                authenticator_kwargs["salt"] = authenticator_config["salt"]

        return Authenticator(**authenticator_kwargs).info

    @staticmethod
    def CTCGetConfig(key: str):
        return context_data.get(key, "")

    @staticmethod
    def CTCSetConfig(key: str, value: Any):
        if key == "Channel":
            if key not in context_data:
                context_data[key] = []
            channel = _channel_parser(value)
            # context_data[key].append(Channel.model_validate(channel))
            context_data[key].append(
                Channel.model_validate(channel).model_dump()
            )
        else:
            context_data[key] = value

    @staticmethod
    def CTCStartUpdate():
        # print("Update requested.")
        pass
