# Nature Diary – Figma Design

Main design file for the **Nature Diary · Personal Nature Encyclopedia** app.

**Figma link**  
https://www.figma.com/make/XF5F0VYicpI0H01BgWg7fI/Nature-Diary-App-Design?node-id=0-1&p=f&t=8IOaLM3cfMjlWU1F-0

---

## What this file contains

The Figma file defines a mobile-first UI for a nature diary application.  
Key screens and flows:

1. **Gallery (Home)**
   - Card grid of observations (plants, animals, landscapes)
   - Filters: all / by time / plants / animals / landscapes
   - Search bar by name, location, or species
   - Floating “+ New record” button to add a new observation

2. **Map**
   - Two modes:
     - *My footprints* – countries where the user has created observations
     - *Explore destinations* – recommended countries, national parks, and classic hiking trails
   - Country explore pages (e.g. USA, Canada, Japan, China):
     - Hero photo and subtitle
     - Sections for national parks / popular natural spots and classic trails

3. **Profile**
   - User card with avatar and short bio
   - Stats: total observations, number of species, number of countries
   - Badge row (high-altitude explorer, 50 plant species, first national park, 5+ countries)
   - Settings entries (language, data export, backup, etc.)

4. **Detail pages (concept)**
   - Observation detail:
     - Photo, time, location, altitude, coordinates
     - Space reserved for taxonomy (kingdom → species)
     - Space reserved for biological or geological encyclopedia text
   - Country / place detail:
     - Hero image, description, list of parks or trails

---

## How it relates to the code demo

- The **Streamlit demo** in this repository follows the same information architecture:
  - Gallery list + filters
  - Country / place exploration
  - Profile stats and badges
- The Figma file represents the **final product UI vision**,
  while the Python code focuses on:
  - data models (observations, taxonomy, places, badges)
  - a minimal, runnable prototype.

Design decisions (colors, spacing, typography) in Figma are **not strictly enforced** in the demo,  
but the layout and feature ideas match what is implemented or planned in code.
