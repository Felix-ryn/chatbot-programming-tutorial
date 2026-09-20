"""CodeMentor - Chatbot tutor pemrograman (versi console).

Perintah khusus:
  exit / quit   -> keluar
  reset / clear -> hapus riwayat percakapan (mulai ulang)
  save          -> simpan riwayat ke file JSON
  help          -> tampilkan bantuan
"""
import os
import sys
import json
from datetime import datetime

from dotenv import load_dotenv
from groq import Groq

from system_prompt import SYSTEM_PROMPT, MODEL

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key or api_key == "your_key_here":
    sys.exit(
        "GROQ_API_KEY belum diisi. Salin .env.example jadi .env lalu isi API key "
        "dari https://console.groq.com/keys"
    )

client = Groq(api_key=api_key)


def new_history():
    return [{"role": "system", "content": SYSTEM_PROMPT}]


def save_history(history):
    fname = f"history_{datetime.now():%Y%m%d_%H%M%S}.json"
    # simpan tanpa system prompt agar file berisi percakapan saja
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(history[1:], f, ensure_ascii=False, indent=2)
    print(f"[Riwayat disimpan ke {fname}]")


def stream_reply(history):
    """Kirim history ke Groq dan cetak balasan bertahap (streaming)."""
    reply = ""
    stream = client.chat.completions.create(
        model=MODEL, messages=history, stream=True
    )
    for chunk in stream:
        token = chunk.choices[0].delta.content or ""
        print(token, end="", flush=True)
        reply += token
    print()
    return reply


HELP = __doc__.split("Perintah khusus:")[1]


def main():
    print("=== CodeMentor: Tutor Pemrograman ===")
    print("Ketik pertanyaanmu. Perintah:" + HELP)
    history = new_history()

    while True:
        try:
            user = input("Kamu: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSampai jumpa!")
            break

        if not user:
            continue

        cmd = user.lower()
        if cmd in ("exit", "quit"):
            print("Sampai jumpa!")
            break
        if cmd in ("reset", "clear"):
            history = new_history()
            print("[Riwayat percakapan direset]")
            continue
        if cmd == "save":
            save_history(history)
            continue
        if cmd == "help":
            print(HELP)
            continue

        history.append({"role": "user", "content": user})
        print("CodeMentor: ", end="", flush=True)
        try:
            reply = stream_reply(history)
            history.append({"role": "assistant", "content": reply})
        except Exception as e:
            # jangan crash bila API gagal; buang pesan user terakhir agar bisa diulang
            history.pop()
            print(f"\n[Error: gagal menghubungi API - {e}]")


if __name__ == "__main__":
    main()
