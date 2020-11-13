import base64
import os
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from es import add_doc, delete_doc, get_doc, update_doc
from transcribe import get_state, put_state, transcribe


def _update_state(state, query, value):
    state["transcript"] = query
    state["value"] = value
    put_state(state)


def _urlify(value):
    if value.startswith("http") or value.startswith("www."):
        return f'<a href="{value}">{value}</a>'
    return value


get_audio = components.declare_component("get_audio", path="frontend/build")

audio = get_audio()

os.makedirs("data", exist_ok=True)
file_name = os.path.join("data", "out.mp4")
Path(file_name).touch()

if audio:
    with open(file_name, "wb") as out:
        out.write(base64.b64decode(audio.split(",")[1]))

transcript = transcribe(file_=file_name)
query = st.text_input("Query:", transcript)
top_doc, id_ = get_doc(query)

res1, res2 = st.beta_columns(2)

with res1:
    st.markdown(
        f'<p style="color:gray">{top_doc.get("key")}</p>',
        unsafe_allow_html=True,
    )
with res2:
    st.markdown(
        f'<p style="font-size:150%">{_urlify(top_doc.get("value"))}</p>',
        unsafe_allow_html=True,
    )

state = get_state()
value = st.text_input("New value:", state.get("value", ""))

col1, col2, col3 = st.beta_columns(3)

with col1:
    if st.button("Add"):
        add_doc({"key": query, "value": value})
        _update_state(state, query, value)
        st.experimental_rerun()

with col2:
    if st.button("Update"):
        update_doc({"key": top_doc["key"], "value": value}, id_)
        _update_state(state, query, value)
        st.experimental_rerun()

with col3:
    if st.button("Delete"):
        delete_doc(id_)
        _update_state(state, query, value)
        st.experimental_rerun()

state["rerun"] = not state.get("rerun") if state.get("rerun") is not None else True
_update_state(state, query, value)
if state["rerun"]:
    st.experimental_rerun()
