import os
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Nature Diary", layout="wide")
st.title("Nature Diary – Full-stack + Distributed Skeleton")

# Create entry
with st.sidebar:
    st.header("Create entry")
    kind = st.selectbox("kind", ["plant", "animal", "landscape"])
    title = st.text_input("title", "Morning hike observation")
    notes = st.text_area("notes", "Saw an interesting leaf pattern...")
    if st.button("Create"):
        r = requests.post(f"{API_BASE}/v1/entries", json={"kind": kind, "title": title, "notes": notes}, timeout=10)
        st.success(f"Created: {r.json()['id']}")

# List entries
st.subheader("Recent entries")
entries = requests.get(f"{API_BASE}/v1/entries", timeout=10).json()
if not entries:
    st.info("No entries yet. Create one on the left.")
else:
    cols = st.columns([2, 2, 2, 2])
    cols[0].write("id")
    cols[1].write("title")
    cols[2].write("status")
    cols[3].write("favorite")

    for e in entries:
        c = st.columns([2, 2, 2, 2])
        c[0].code(e["id"])
        c[1].write(f"{e['kind']} · {e['title']}")
        c[2].write(e["status"])
        c[3].write("⭐" if e["is_favorite"] else "")

# Detail + favorite
st.subheader("Entry detail")
entry_id = st.text_input("entry_id (paste from list)")
if st.button("Fetch detail") and entry_id:
    e = requests.get(f"{API_BASE}/v1/entries/{entry_id}", timeout=10).json()
    st.json(e)
    if st.button("Favorite ⭐"):
        e2 = requests.post(f"{API_BASE}/v1/entries/{entry_id}/favorite", timeout=10).json()
        st.json(e2)

# Search
st.subheader("Search")
q = st.text_input("q")
if st.button("Search") and q:
    res = requests.get(f"{API_BASE}/v1/search", params={"q": q}, timeout=10).json()
    st.write(f"{len(res)} results")
    st.json(res[:10])
