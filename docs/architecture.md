# Nature Diary – Architecture Overview

This document describes the architecture of the **Nature Diary** project – how the
design in Figma, the Python domain model, and the Streamlit demo work together.

The goal is to show that this is not just a random Streamlit toy, but the
core of a future product that could power a real mobile app and even
smart-glasses experiences.

---

## 1. Goals and non-goals

### 1.1 Product goals

Nature Diary aims to:

1. Turn outdoor photos into a **structured nature encyclopedia entry**  
   - For organisms (plants, animals, fungi, etc.):  
     full taxonomy (kingdom → species) + encyclopedia-style description.  
   - For landscapes:  
     landform type, geology, formation process, and climate context.

2. Attach each entry to a **concrete personal moment**  
   - Time, GPS location, altitude, country / place.  
   - A short feeling or note (and later, a voice note).

3. Build a clean **information architecture** that can later be used by:
   - AI vision models (species recognition, landform classification),
   - LLMs (generating encyclopedia text / summaries),
   - smart-glasses or voice assistants.

### 1.2 Non-goals of this repository

This repository intentionally **does not** try to be:

- a full production backend or API,  
- a real mobile client,  
- an ML / CV pipeline implementation.

Instead, it focuses on:

- a clear **domain model** in Python,  
- a small but runnable **Streamlit demo**,  
- and a detailed **Figma design** that shows the final UX vision.

---

## 2. High-level components

The project has three main layers:

1. **Design layer (Figma)**  
   - Complete mobile UI / UX for:
     - Gallery,
     - Map / Explore destinations,
     - Profile and badges.  
   - Contains flows for:
     - country → national parks → place detail,
     - filters (plants / animals / landscapes),
     - search, badges, and “My Footprints” (visited countries).  
   - Linked in `design/figma-link.md`.

2. **Domain layer (Python data model)**  
   - Dataclasses that describe:
     - observations (single user entries),
     - taxonomy (biological classification),
     - encyclopedia information for organisms and landscapes,
     - (planned) places, countries, badges.  
   - Implemented in `backend/models.py`.  
   - Sample data stored in `backend/demo_data.json`.

3. **Demo application (Streamlit UI)**  
   - A minimal web UI that lets you:
     - filter observations by type,
     - click a card and see a detailed panel.  
   - Implemented in `app/app.py`.  
   - Used for local exploration and portfolio demos.

Data flow (for the current demo):

```text
backend/demo_data.json  -->  Python domain model  -->  Streamlit gallery + detail view
(Future: camera / phone photos)                 (Future: DB / API)

```
---

## 3. Data model

All core concepts in the Figma design are mapped to Python types.
The most important ones are listed below.

In code, these are implemented as @dataclass objects in backend/models.py.
Here we describe the conceptual fields, not every line of code.

### 3.1 Observation

Represents one user-recorded item: a plant, animal or landscape that the user
actually saw at a specific time and place.

#### Key fields (conceptual):

- `id: str` – unique ID (e.g. "obs-1").
- `title_cn: str, title_en: str` – localized display names
(e.g. “日本枫树 / Japanese Maple”).
- `obs_type:` Literal["plant", "animal", "landscape"].
- `image_url: str` – URL to a photo used in the demo(in a real app this would be user uploads).
- `country: str` – high-level country (Japan, New Zealand, Switzerland, …).
- `location: str` – human-readable location(Kyoto, Fiordland National Park, …).
- `latitude:` float, longitude: float, altitude_m: Optional[float].
- `datetime: datetime` – when the observation happened.
- `user_feeling: Optional[str]` – short free-text note (e.g. “First time seeing autumn colors in Kyoto with friends.”).
- `taxonomy: Optional[Taxonomy]` – only for plants / animals.
- `encyclopedia: Optional[EncyclopediaEntry]` – only for plants / animals.
- `geology: Optional[GeologyInfo]` – only for landscapes.
- `ai_summary: Optional[str]` – reserved for future LLM-generated summary.

#### Conceptual JSON (simplified)
```text
{
  "id": "obs-1",
  "title_cn": "日本枫树",
  "title_en": "Japanese Maple",
  "obs_type": "plant",
  "image_url": "https://images.pexels.com/photos/235985/pexels-photo-235985.jpeg",
  "country": "Japan",
  "location": "Kyoto",
  "latitude": 35.0116,
  "longitude": 135.7681,
  "altitude_m": 180,
  "datetime": "2025-10-15T14:30:00",
  "user_feeling": "First time seeing autumn colors in Kyoto with friends."
}

```
### 3.2 Taxonomy

Describes where a species sits in the biological taxonomy:

- `kingdom`, `phylum`, `class_name`, `order`, `family`, `genus`, `species`
  
#### Fields

- `kingdom: str` – e.g. "Plantae".
- `phylum: str`.
- `class_name: str`.
- `order: str`.
- `family: str`.
- `genus: str`.
- `species: str` – Latin binomial (e.g. "Acer palmatum").
  
### 3.3 EncyclopediaEntry

Biological encyclopedia information for organisms:
In the final version, this is what the user reads when opening the “encyclopedia” section.

#### Fields
- `native_range: str` – geographic origin / distribution.  
- `habitat: str `– forests, grasslands, alpine meadows, wetlands, etc.
- `edibility : Optional[str]` - edible / toxic / ornamental only, plus notes.
- `human_uses: List[str]` - ornamental, timber, medicine, food, dye, etc. 
- `ecology: str`- ecological role, including:
  - pollinators and seed dispersers,
  - typical co-occurring species,
  - position in the food web.
    
#### Optional future fields
- `cultural_meaning: str` – symbolism, festivals, traditional stories.
- `conservation_status: str` – IUCN category or local protection level.

### 3.4 GeologyInfo

Encyclopedia information for landscapes – the “why is this place like this?” part.

#### Fields
- `landform_type: str` – glacier valley, canyon, coastal cliff, karst peak forest, dune, etc.
- `formation_process: str` – glaciation, erosion, uplift, volcanic activity, river incision…
- `range_region: str` – mountain range or region name (e.g. “Swiss Alps”).
- `geological_age: Optional[str]` – approximate age or period.
- `climate: str` – typical climate zone (alpine, maritime, temperate rainforest…).
- `hazards: Optional[str]` – optional notes (avalanches, rockfall, flash floods).

This maps to the sections in Figma where a glacier, canyon or peak has a short
paragraph explaining its origin and the required conditions (ice, tectonics, etc.).

### 3.5 Ecology / co-occurrence (future concept)

The Figma design also hints at “usually appears together with…” for some plants
and animals.

This could be modeled later as:
```text
@dataclass
class EcologyRelation:
    focal_observation_id: str
    co_occurring_species_ids: list[str]
    relation_type: str  # "often seen with", "host plant of", etc.

```
For the current demo this is descriptive only and lives inside the ecology text
### 3.6 Place and Country (for Map / Explore)

The Map tab in Figma shows:
- continents (Global / North America / Europe / Asia / Oceania),
- countries (USA, Canada, Japan, China, Switzerland, Norway, New Zealand, …),
- for each country:
   - “National Parks” or “Popular Spots”,
   - “Classic Trails”.

#### Conceptual model
```text
@dataclass
class Place:
    id: str
    name_cn: str
    name_en: str
    country_code: str      # ISO code, e.g. "JP"
    place_type: str        # "national_park", "popular_spot", "trail"
    thumbnail_url: str
    summary: str
```
```text
@dataclass
class CountrySummary:
    code: str              # "US", "CA", "JP", ...
    name_cn: str
    name_en: str
    num_parks: int
    num_trails: int
```
In the current demo, full Place / CountrySummary objects are not yet stored,
but this structure matches the Figma screens and can be filled later.

### 3.7 Badge and profile statistics
The Profile tab shows badges such as:
- high-altitude explorer,
- 50 plant species,
- first national park,
- visited 5 countries.

#### Conceptual model
```text
@dataclass
class Badge:
    id: str
    name_cn: str
    name_en: str
    description: str
    unlock_condition: str
    unlocked_at: Optional[datetime]
```
Profile statistics can be derived from observations:
- total_observations,
- num_species_plants,
- num_species_animals,
- num_countries_visited.
  
For the current demo these are not fully implemented in code,
but the architecture keeps them in mind.

---

## 4. Data storage for the demo

For now, data is stored as a simple JSON file:
- backend/demo_data.json

### Characteristics
- Small, human-readable, easy to edit while designing.
- Each entry corresponds to one Observation.
- Only a subset of fields is currently populated (name, type, image URL, location, time, feeling).
- In the future this could be replaced by:
   - a proper database, or
   - API calls to a backend service.

### Example entry (see also the real file):
```text
{
  "id": "obs-2",
  "title_cn": "森林蕨类",
  "title_en": "Forest Fern",
  "obs_type": "plant",
  "image_url": "https://images.pexels.com/photos/807598/pexels-photo-807598.jpeg",
  "country": "New Zealand",
  "location": "Fiordland National Park",
  "latitude": -45.417,
  "longitude": 167.718,
  "altitude_m": 250,
  "datetime": "2025-06-18T10:15:00",
  "user_feeling": "Cool, damp forest with deep green ferns everywhere."
}
```
`app/app.py` loads this file, converts each dict into an Observation object,
and then drives the UI.

## 5. Demo behaviour (Streamlit app)

`app/app.py` will gradually implement the following flows:

1. **Gallery View**
   - Load observations from `backend/demo_data.json`.
   - Converts entries to Observation objects (observation_from_dict).
   - Sorts them by `datetime` (newest first).
   - Shows a filter bar:
      - All / Plants / Animals / Landscapes.
   - Shows a list of buttons on the left – one per observation.

Shows a list of buttons on the left – one per observation.

2. **Selection state**
   - Uses st.session_state["selected_id"] to remember which observation is selected.
   - Clicking a button updates this ID.
   - This mimics navigating from a card on the Gallery tab to a detail page.

3. **Observation detail**
   - Show photo, time, location, altitude and coordinates.
   - Show taxonomy block (if available).
   - Show encyclopedia section:
     - biology for plants and animals,
     - geology for landscapes.
   - Show user feeling text and (later) an AI summary.

4. **Mapping to Figma**
   - The left column ≈ Gallery card list in the 图鉴 tab.
   - The right column ≈ observation detail page.
     
   Future work:
   - separate pages / tabs for Map and Profile,
   - country → place → detail navigation,
   - badge detail sheets.

---

## 6. Future AI integration (not implemented yet)

Planned future extensions:

1. **Vision → species recognition**
   - Take an image from camera or smart glasses.
   - Use a vision model to suggest candidate species.
   - Fill in taxonomy and part of the encyclopedia entry automatically.

2. **LLM-generated encyclopedia text**
   - Use an LLM (e.g., via an API) to:
     - generate short descriptions for `EncyclopediaEntry` or `GeologyInfo`,
     - summarize user feelings into one or two sentences.

3. **Safety and offline packs**
   - Pre-download “safety packs” for certain regions:
     - poisonous plants / animals,
     - terrain hazards and weather warnings.

4. **Smart-glasses integration**
   - Replace manual photo upload with a camera stream from smart glasses.
   - Voice interface for adding feelings and asking follow-up questions.

These ideas are documented here to show the direction of the project,
even though the current repository focuses on a small, clear, local demo.

---

## 7. Summary
- **Figma** defines the full mobile UX: Gallery, Map, Profile, badges and
detailed encyclopedia sections.
- **Python dataclasses** in backend/models.py capture the core domain:
observations, taxonomy, encyclopedia biology, geology, places and badges.
- **Streamlit** provides a simple but fully runnable demo that:
   - loads structured data,
   - renders a gallery and detail view,
   - and can be extended towards the Figma vision.

---
