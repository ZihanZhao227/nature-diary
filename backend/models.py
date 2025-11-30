from dataclasses import dataclass
from typing import List, Optional, Literal
from datetime import datetime

ObservationType = Literal["plant", "animal", "landscape"]

@dataclass
class Taxonomy:
    kingdom: str
    phylum: str
    class_name: str
    order: str
    family: str
    genus: str
    species: str

@dataclass
class EncyclopediaEntry:
    native_range: str
    habitat: str
    edibility: str
    human_uses: List[str]
    ecology: str

@dataclass
class GeologyInfo:
    landform_type: str
    formation_process: str
    range_region: str
    climate: str

@dataclass
class Observation:
    id: str
    title_cn: str
    title_en: str
    obs_type: ObservationType
    image_path: str          # 对应 docs 或本地静态图
    country: str
    location: str
    latitude: float
    longitude: float
    altitude_m: Optional[int]
    datetime: datetime

    taxonomy: Optional[Taxonomy] = None
    encyclopedia: Optional[EncyclopediaEntry] = None
    geology: Optional[GeologyInfo] = None

    user_feeling: Optional[str] = None
    ai_summary: Optional[str] = None
