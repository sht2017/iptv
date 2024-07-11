from typing import Any, Optional

from pydantic import BaseModel, Field


class Channel(BaseModel):
    id: str = Field(..., alias="ChannelID")
    name: str = Field(..., alias="ChannelName")
    user_id: int = Field(..., alias="UserChannelID")
    url: str = Field(..., alias="ChannelURL")
    timeshift: int = Field(..., alias="TimeShift")
    sdp: str = Field(..., alias="ChannelSDP")
    timeshift_url: Optional[str] = Field(None, alias="TimeShiftURL")
    log_url: Optional[str] = Field(None, alias="ChannelLogURL")
    logo_url: Optional[str] = Field(None, alias="ChannelLogoURL")
    position_x: int = Field(..., alias="PositionX")
    position_y: int = Field(..., alias="PositionY")
    begin_time: int = Field(..., alias="BeginTime")
    interval: int = Field(..., alias="Interval")
    lasting: int = Field(..., alias="Lasting")
    type_: int = Field(..., alias="ChannelType")
    purchased: Optional[Any] = Field(None, alias="ChannelPurchased")
    timeshift_length: Optional[int] = Field(None, alias="TimeShiftLength")
    telecomcode: Optional[str] = Field(None)
    fcc_enable: Optional[int] = Field(None, alias="FCCEnable")
    fcc_function: Optional[int] = Field(None, alias="FCCFunction")
    fcc_ip: Optional[str] = Field(None, alias="ChannelFCCIP")
    fcc_port: Optional[int] = Field(None, alias="ChannelFCCPort")
