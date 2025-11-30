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

For the first demo, place/country/badge logic is kept simple and can b
