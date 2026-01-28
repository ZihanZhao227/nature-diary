import os
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.title("Nature Diary – Full-stack Demo (Spine)")

r = requests.get(f"{API_BASE}/health", timeout=5)
st.write("API health:", r.json())
st.info("Next: wire entries CRUD + Redis queue + worker.")
