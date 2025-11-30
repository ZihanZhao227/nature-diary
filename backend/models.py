from dataclasses import dataclass
from typing import Optional, Literal
from datetime import datetime


ObservationType = Literal["plant", "animal", "landscape"]


@dataclass
class Observation:
    """
    Core domain object used in the demo.
    Represents one recorded plant / animal / landscape.
    """
    id: str
    title_cn: str
    title_en: str
    obs_type: ObservationType

    image_url: str
    country: str
    location: str

    latitude: float
    longitude: float
    altitude_m: Optional[int]
    datetime: datetime

    user_feeling: Optional[str] = None


def observation_from_dict(data: dict) -> Observation:
    """
    Helper to convert a JSON dict into an Observation instance.
    """
    dt = datetime.fromisoformat(data["datetime"])

    return Observation(
        id=data["id"],
        title_cn=data["title_cn"],
        title_en=data["title_en"],
        obs_type=data["obs_type"],
        image_url=data["image_url"],
        country=data["country"],
        location=data["location"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        altitude_m=data.get("altitude_m"),
        datetime=dt,
        user_feeling=data.get("user_feeling"),
    )
