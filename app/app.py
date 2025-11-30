# app/app.py
import streamlit as st
import json
from datetime import datetime
from pathlib import Path

from backend.models import Observation, Taxonomy, EncyclopediaEntry, GeologyInfo

DATA_PATH = Path(__file__).parent.parent / "backend" / "demo_data.json"

def load_observations() -> list[Observation]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
    obs_list = []
    for item in raw:
        obs = Observation(
            id=item["id"],
            title_cn=item["title_cn"],
            title_en=item["title_en"],
            obs_type=item["obs_type"],
            image_path=item["image_path"],
            country=item["country"],
            location=item["location"],
            latitude=item["latitude"],
            longitude=item["longitude"],
            altitude_m=item.get("altitude_m"),
            datetime=datetime.fromisoformat(item["datetime"]),
            # 这里先略掉 taxonomy / encyclopedia，后面再补
        )
        obs_list.append(obs)
    return obs_list

def main():
    st.set_page_config(page_title="Nature Diary Demo", layout="wide")
    st.title("Nature Diary · 自然图鉴 Demo")

    observations = load_observations()

    # --- filters ---
    col1, col2 = st.columns([1, 2])
    with col1:
        filter_type = st.radio(
            "按类型筛选",
            ["全部", "植物", "动物", "景观"],
            horizontal=True,
        )
    with col2:
        sort_by_time = st.checkbox("按时间从新到旧排序", value=True)

    filtered = observations
    if filter_type != "全部":
        mapping = {"植物": "plant", "动物": "animal", "景观": "landscape"}
        filtered = [o for o in filtered if o.obs_type == mapping[filter_type]]

    if sort_by_time:
        filtered = sorted(filtered, key=lambda o: o.datetime, reverse=True)

    # --- layout: left = list, right = detail ---
    list_col, detail_col = st.columns([1, 1.2])

    with list_col:
        st.subheader("我的图鉴")
        selected_id = None
        for o in filtered:
            if st.button(f"{o.title_cn} · {o.title_en}", key=o.id):
                selected_id = o.id
        if not selected_id and filtered:
            selected_id = filtered[0].id

    if not filtered:
        with detail_col:
            st.info("当前筛选条件下没有记录。")
        return

    current = next(o for o in filtered if o.id == selected_id)

    with detail_col:
        st.subheader(f"{current.title_cn} / {current.title_en}")
        st.image(current.image_path, use_column_width=True)

        st.markdown(
            f"**地点**：{current.location} · {current.country}  \n"
            f"**时间**：{current.datetime.strftime('%Y-%m-%d %H:%M')}  \n"
            f"**海拔**：{current.altitude_m or '—'} m"
        )

        # 这里以后再加 taxonomy / encyclopedia / geology，先占个坑
        st.markdown("### 分类信息 / Taxonomy")
        st.caption("TODO: 界、门、纲、目、科、属、种")

        st.markdown("### 生物百科 / Encyclopedia / Geology")
        st.caption("TODO: 原产地、栖息地、地质成因等描述")

        st.markdown("### 那一刻的心情 / Your feeling")
        st.caption("TODO: 用户当时的语音转文字 + AI 总结")

if __name__ == "__main__":
    main()
