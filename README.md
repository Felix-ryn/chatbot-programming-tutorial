# CodeMentor - Chatbot Tutor Pemrograman

## 1. Tema & Konsep
**CodeMentor** adalah chatbot berbasis LLM yang berperan sebagai **tutor pemrograman**.
Ia menjelaskan konsep coding dengan bahasa sederhana, membantu men-debug kode, dan
memberi contoh kode. Chatbot menggunakan **API Groq** (model `openai/gpt-oss-120b`)
dan mengingat konteks percakapan dalam satu sesi.

## 2. Cara Menjalankan

1. Dapatkan API key gratis dari https://console.groq.com/keys
2. Salin `.env.example` menjadi `.env`, lalu isi key-nya:
   ```
   GROQ_API_KEY=gsk_xxxxxxxx
   ```
3. Install dependency:
   ```
   pip install -r requirements.txt
   ```
4. Jalankan salah satu versi:
   - **Console:** `python chatbot.py`
   - **Web (Streamlit):** `streamlit run app.py`

### Alur Running System
```
                 python chatbot.py  /  streamlit run app.py
                              |
                              v
              [1] load_dotenv() baca GROQ_API_KEY dari .env
                              |
                    key kosong? --> tampilkan error & berhenti
                              |
                              v
              [2] buat Groq client + siapkan history:
                  [{system: SYSTEM_PROMPT}]
                              |
                              v
              [3] user mengetik pesan / perintah khusus
                              |
        perintah? --exit--> keluar   --reset--> kosongkan history
                              |
                              v
              [4] pesan user di-append ke history
                              |
                              v
              [5] history dikirim ke Groq (stream=True)
                              |
              gagal? --> tampilkan pesan error, history user
                         terakhir dibuang, lanjut loop (tidak crash)
                              |
                              v
              [6] token balasan dicetak bertahap (streaming)
                              |
                              v
              [7] balasan di-append ke history --> kembali ke [3]
```
Inti alurnya: **history** (list `messages`) inilah yang membuat bot "ingat"
konteks — setiap giliran, seluruh riwayat ikut dikirim ke API.

### Perintah khusus (versi console)
| Perintah        | Fungsi                              |
| --------------- | ----------------------------------- |
| `exit` / `quit` | keluar dari program                 |
| `reset` / `clear` | hapus riwayat, mulai percakapan baru |
| `save`          | simpan riwayat ke file JSON         |
| `help`          | tampilkan daftar perintah           |

## 3. Contoh Percakapan
Berikut cuplikan hasil percakapan dengan CodeMentor:

![Contoh percakapan 1](dokumentasi/Screenshot%202026-09-20%20160300.png)

![Contoh percakapan 2](dokumentasi/Screenshot%202026-09-20%20160323.png)

## 4. Struktur Kode
| File               | Keterangan                                                        |
| ------------------ | ----------------------------------------------------------------- |
| `system_prompt.py` | System prompt persona tutor + nama model (dipakai console & web)  |
| `chatbot.py`       | Versi **console**: loop input, perintah khusus, streaming, error handling |
| `app.py`           | Versi **web Streamlit**: chat UI, slider temperature, download riwayat |
| `.env.example`     | Template API key (yang asli di `.env`, tidak di-commit)           |
| `.gitignore`       | Mengecualikan `.env` dan file riwayat dari Git                    |
| `requirements.txt` | Daftar dependency (groq, python-dotenv, streamlit)                |
| `dokumentasi/`     | Folder berisi screenshot contoh percakapan                        |

### Fitur yang memenuhi ketentuan
- System prompt sesuai tema (tutor pemrograman)
- Conversation history (bot ingat konteks dalam satu sesi)
- Penanganan error API (program tidak crash saat API gagal)
- 4 perintah khusus (`exit`, `reset`, `save`, `help`)

### Fitur bonus
- Tampilan web Streamlit
- Streaming response (console & web)
- Simpan riwayat ke JSON (`save` di console, tombol download di web)
- Kontrol parameter temperature (web)

## 5. Catatan Penggunaan AI
Kode awal seluruh file di-generate dengan bantuan AI assistant, kemudian
**dipahami dan disesuaikan sendiri**. Bagian yang perlu kamu isi/kerjakan mandiri:
- Menyesuaikan isi `SYSTEM_PROMPT` sesuai gaya yang diinginkan.
- Mengambil screenshot percakapan asli untuk bagian contoh.
- Memahami alur `messages` (conversation history) dan mekanisme streaming.

> Sesuaikan paragraf ini dengan kondisi pengerjaanmu yang sebenarnya.
