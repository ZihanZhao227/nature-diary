import json
from pathlib import Path
from typing import List, Optional
import sys

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.models import Observation, observation_from_dict

DATA_PATH = ROOT_DIR / "backend" / "demo_data.json"




def load_observations() -> List[Observation]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    observations: List[Observation] = [observation_from_dict(item) for item in raw]
    # sort newest first by default
    observations.sort(key=lambda o: o.datetime, reverse=True)
    return observations


def filter_by_type(observations: List[Observation], filter_type: str) -> List[Observation]:
    if filter_type == "All":
        return observations
    mapping = {
        "Plants": "plant",
        "Animals": "animal",
        "Landscapes": "landscape",
    }
    target = mapping.get(filter_type)
    return [o for o in observations if o.obs_type == target]


def main():
    st.set_page_config(page_title="Nature Diary Demo", layout="wide")

    st.title("Nature Diary · Personal Nature Encyclopedia")
    st.caption(
        "Minimal Streamlit demo – browse a few sample observations "
        "and see how the data model is projected into UI."
    )

    observations = load_observations()
    if not observations:
        st.error("No observations found in demo_data.json")
        return

    # ---- filters ----
    filter_col, _ = st.columns([1, 3])
    with filter_col:
        filter_type = st.radio(
            "Filter by type",
            ["All", "Plants", "Animals", "Landscapes"],
            horizontal=True,
        )

    filtered = filter_by_type(observations, filter_type)
    if not filtered:
        st.info("No observations for this filter yet.")
        return

    # ---- layout: left list, right detail ----
    list_col, detail_col = st.columns([1, 1.4])

    with list_col:
        st.subheader("Gallery")

        # remember which observation is selected
        if "selected_id" not in st.session_state:
            st.session_state["selected_id"] = filtered[0].id

        for obs in filtered:
            label = f"{obs.title_cn} · {obs.title_en}"
            if st.button(label, key=obs.id):
                st.session_state["selected_id"] = obs.id

    # get current selection
    selected_id = st.session_state.get("selected_id", filtered[0].id)
    current: Optional[Observation] = next(
        (o for o in filtered if o.id == selected_id), filtered[0]
    )

    with detail_col:
        st.subheader(f"{current.title_cn} / {current.title_en}")

        st.image(current.image_url, use_column_width=True)

        st.markdown(
            f"**Type:** {current.obs_type.capitalize()}  \n"
            f"**Location:** {current.location}, {current.country}  \n"
            f"**Time:** {current.datetime.strftime('%Y-%m-%d %H:%M')}  \n"
            f"**Altitude:** {current.altitude_m or '—'} m  \n"
            f"**Coordinates:** {current.latitude:.4f}, {current.longitude:.4f}"
        )

        st.markdown("### Feeling at that moment")
        if current.user_feeling:
            st.write(current.user_feeling)
        else:
            st.caption("No note recorded yet.")

        st.markdown("### Taxonomy & encyclopedia (future work)")
        st.caption(
            "In the full version, this section will show kingdom → species, "
            "native range, habitat, uses, ecology or geology. "
            "For now it is only documented in the architecture doc."
        )


if __name__ == "__main__":
    main()
