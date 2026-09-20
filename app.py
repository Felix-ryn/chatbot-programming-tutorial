"""CodeMentor - versi web (Streamlit). Jalankan: streamlit run app.py"""
import os
import json

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from system_prompt import SYSTEM_PROMPT, MODEL

load_dotenv()

st.set_page_config(page_title="CodeMentor", page_icon="")
st.title("CodeMentor - Tutor Pemrograman")

api_key = os.getenv("GROQ_API_KEY")
if not api_key or api_key == "your_key_here":
    st.error("GROQ_API_KEY belum diisi. Buat file .env dari .env.example.")
    st.stop()

client = Groq(api_key=api_key)

# conversation history disimpan di session_state agar bot ingat konteks
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Pengaturan")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    if st.button("Reset percakapan"):
        st.session_state.messages = []
        st.rerun()
    st.download_button(
        "Download riwayat (JSON)",
        json.dumps(st.session_state.messages, ensure_ascii=False, indent=2),
        file_name="history.json",
        mime="application/json",
        disabled=not st.session_state.messages,
    )

# tampilkan riwayat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Tanya soal pemrograman..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # gabungkan system prompt + history untuk dikirim ke API
    payload = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
    try:
        stream = client.chat.completions.create(
            model=MODEL, messages=payload, temperature=temperature, stream=True
        )
        with st.chat_message("assistant"):
            reply = st.write_stream(
                (c.choices[0].delta.content or "" for c in stream)
            )
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.session_state.messages.pop()
        st.error(f"Gagal menghubungi API: {e}")
