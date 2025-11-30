from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


# data structures


@dataclass
class Taxonomy:
    """Biological classification for plants / animals."""

    kingdom: str
    phylum: str
    class_name: str
    order: str
    family: str
    genus: str
    species: str


@dataclass
class EncyclopediaEntry:
    """Encyclopedia-style info for a species."""

    summary: str
    native_range: str
    uses: str
    edible: bool
    ecology: str


@dataclass
class GeologyInfo:
    """Geological context for a landscape observation."""

    formation_type: str         # e.g. "Glacial valley and mountain lake"
    age: str                    # e.g. "Quaternary"
    process: str                # e.g. "Carved by valley glaciers"
    mountain_range: Optional[str] = None


@dataclass
class Observation:
    """One nature observation made by the user."""

    id: str
    title_cn: str
    title_en: str
    obs_type: str               # "plant" | "animal" | "landscape"
    image_url: str

    country: str
    location: str
    latitude: float
    longitude: float
    altitude_m: Optional[float]

    datetime: datetime
    user_feeling: Optional[str] = None

    # rich info (optional; may be None)
    taxonomy: Optional[Taxonomy] = None
    encyclopedia: Optional[EncyclopediaEntry] = None
    geology: Optional[GeologyInfo] = None


# helper to build from JSON 


def taxonomy_from_dict(data: Dict[str, Any] | None) -> Optional[Taxonomy]:
    if not data:
        return None
    return Taxonomy(
        kingdom=data.get("kingdom", ""),
        phylum=data.get("phylum", ""),
        class_name=data.get("class_name", ""),
        order=data.get("order", ""),
        family=data.get("family", ""),
        genus=data.get("genus", ""),
        species=data.get("species", ""),
    )


def encyclopedia_from_dict(data: Dict[str, Any] | None) -> Optional[EncyclopediaEntry]:
    if not data:
        return None
    return EncyclopediaEntry(
        summary=data.get("summary", ""),
        native_range=data.get("native_range", ""),
        uses=data.get("uses", ""),
        edible=bool(data.get("edible", False)),
        ecology=data.get("ecology", ""),
    )


def geology_from_dict(data: Dict[str, Any] | None) -> Optional[GeologyInfo]:
    if not data:
        return None
    return GeologyInfo(
        formation_type=data.get("formation_type", ""),
        age=data.get("age", ""),
        process=data.get("process", ""),
        mountain_range=data.get("mountain_range"),
    )


def observation_from_dict(data: Dict[str, Any]) -> Observation:
    """Create an Observation instance from a JSON dict."""
    tax = taxonomy_from_dict(data.get("taxonomy"))
    enc = encyclopedia_from_dict(data.get("encyclopedia"))
    geo = geology_from_dict(data.get("geology"))

    return Observation(
        id=data["id"],
        title_cn=data["title_cn"],
        title_en=data["title_en"],
        obs_type=data["obs_type"],
        image_url=data["image_url"],
        country=data["country"],
        location=data["location"],
        latitude=float(data["latitude"]),
        longitude=float(data["longitude"]),
        altitude_m=data.get("altitude_m"),
        datetime=datetime.fromisoformat(data["datetime"]),
        user_feeling=data.get("user_feeling"),
        taxonomy=tax,
        encyclopedia=enc,
        geology=geo,
    )
