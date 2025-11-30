# Nature Diary – Architecture Overview

This document describes the high-level architecture of the **Nature Diary** project:
how the design, data model and demo application fit together.

---

## 1. Goals

Nature Diary aims to:

1. Turn outdoor photos into a **structured nature encyclopedia entry**:
   - for organisms: full taxonomy (kingdom → species) + encyclopedia-style description;
   - for landscapes: geology and formation.
2. Attach each entry to a **moment in the user’s life**:
   - time, GPS location, altitude, country, and a short feeling or voice note.
3. Provide a clear **information architecture** that can later be used by:
   - AI vision models,
   - smart glasses / voice interfaces,
   - more advanced mobile apps.

This repository focuses on a **small but coherent demo**, not a production system.

---

## 2. High-level components

The project has three main layers:

1. **Design layer (Figma)**
   - Defines the final mobile UX: navigation, visual style, and interactions.
   - See `design/figma-link.md` for the design link.

2. **Domain layer (Python data model)**
   - Data classes that describe observations, taxonomy, encyclopedia data, places and badges.
   - Implemented in `backend/models.py`.
   - Sample records stored in `backend/demo_data.json`.

3. **Demo application (Streamlit UI)**
   - Minimal web UI that visualizes the data model.
   - Implemented in `app/app.py`.
   - Used only for showing the concept and browsing sample data.

---

## 3. Data model

The core domain objects are:

### 3.1 Observation

Represents one user-recorded item (plant, animal or landscape).

Key fields (conceptual):

- `id`: unique identifier  
- `title_cn`, `title_en`: localized names  
- `obs_type`: `"plant" | "animal" | "landscape"`  
- `image_path`: path to sample image used in the demo  
- `country`, `location`: human-readable location  
- `latitude`, `longitude`, `altitude_m`  
- `datetime`: when the observation was created  
- `taxonomy`: optional `Taxonomy` object (for plants/animals)  
- `encyclopedia`: optional `EncyclopediaEntry` (biology)  
- `geology`: optional `GeologyInfo` (landscapes)  
- `user_feeling`: short free-text note  
- `ai_summary`: space for an AI-generated summary (future work)

### 3.2 Taxonomy

Describes where a species sits in the biological taxonomy:

- `kingdom`, `phylum`, `class_name`, `order`, `family`, `genus`, `species`

### 3.3 EncyclopediaEntry

Biological encyclopedia information for organisms:

- `native_range`: original distribution  
- `habitat`: typical habitat (forest, meadow, wetland, alpine, etc.)  
- `edibility`: whether it is edible / toxic  
- `human_uses`: list of uses (ornamental, timber, medicine, dye, etc.)  
- `ecology`: text describing ecological relationships and role

### 3.4 GeologyInfo

Encyclopedia information for landscapes:

- `landform_type`: glacier valley, canyon, mountain ridge, coastal cliff, etc.  
- `formation_process`: glaciation, erosion, uplift, volcanic activity, …  
- `range_region`: mountain range or region name  
- `climate`: typical climate description

### 3.5 Place, Country, Badge (planned)

For the first demo, place/country/badge logic is kept simple and can be represented as
either:

- separate dataclasses, or
- structured dictionaries inside `demo_data.json`.

Conceptually:

- **Place**: a specific park or trail; used in the Map → country detail screens.  
- **Country**: aggregates places and statistics (number of parks, classic trails, etc.).  
- **Badge**: achievements unlocked by altitude, number of species, number of countries, etc.

---

## 4. Demo behaviour (Streamlit app)

`app/app.py` will gradually implement the following flows:

1. **Gallery**
   - Load observations from `backend/demo_data.json`.
   - Provide filters by type (all / plants / animals / landscapes).
   - Optional sorting by time (newest first).
   - Display a list of cards; clicking a card opens the detail panel.

2. **Observation detail**
   - Show photo, time, location, altitude and coordinates.
   - Show taxonomy block (if available).
   - Show encyclopedia section:
     - biology for plants and animals,
     - geology for landscapes.
   - Show user feeling text and (later) an AI summary.

3. **Map and profile (conceptual)**
   - For the first Streamlit demo, only a very light version may be implemented:
     - browse observations by country,
     - display summary counts on a simple profile section.
   - The detailed country pages and badges are fully defined in Figma and can be
     added later.

---

## 5. Future AI integration (not implemented yet)

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

## 6. Summary

- Figma captures the **UX vision** and detailed mobile UI.  
- Python data classes capture the **domain model**: observations, taxonomy, encyclopedia, places and badges.  
- Streamlit provides a **simple, runnable demo** that proves the concept and can be extended later.

Together, they form a student project that is:
- small enough to run locally,
- but rich enough to discuss design, data modelling and future AI integration in a portfolio or interview.
