# Nature Diary – Figma Design

Main design file for the **Nature Diary · Personal Nature Encyclopedia** app.

Figma link:  
https://www.figma.com/make/XF5F0VYicpI0H01BgWg7fI/Nature-Diary-App-Design?node-id=0-1&p=f&t=8IOaLM3cfMjlWU1F-0


---

## What this file contains

The Figma file defines a mobile-first UI for a nature diary app.  
Key screens and flows:

1. **图鉴 · Gallery (Home)**
   - Card grid of observations (plants, animals, landscapes)
   - Filters: 全部 / 按时间 / 植物 / 动物 / 景观
   - Search bar by name / location / species
   - Floating “+ 新记录” button to add a new observation

2. **地图 · Map**
   - Two modes:  
     - `我的足迹` – countries where the user has created observations  
     - `探索目的地` – recommended countries / parks / classic trails
   - Country explore pages (e.g. 美国, 加拿大, 日本, 中国):
     - Hero photo + subtitle
     - Sections for 国家公园 / 热门自然景点 and 经典徒步路线

3. **我的 · Profile**
   - User card with avatar and short bio
   - Stats: 观察总数、物种数量、国家数量
   - Badges row (高海拔探索者, 记录 50 种植物, 第一次国家公园, 跨越 5 个国家)
   - Settings entry (language, data export, backup, etc.)

4. **Detail pages (concept)**
   - Observation detail: photo, time, location, altitude,
     and space reserved for:
     - taxonomy (界 / 门 / 纲 / 目 / 科 / 属 / 种)
     - encyclopedia info for species or geology for landscapes
   - Country / place detail: hero image, description,
     list of parks or trails.

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
