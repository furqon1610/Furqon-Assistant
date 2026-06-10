import os
import random
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Memuat konfigurasi dari file .env
load_dotenv()

app = Flask(__name__)

# Inisialisasi klien OpenAI
# Pastikan API Key di file .env tersimpan aman
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    
    try:
        # Mencoba terhubung ke OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response.choices[0].message.content
        
    except Exception as e:
        # Jika gagal (karena belum isi saldo/error), gunakan jawaban simulasi
        print(f"Error detail: {e}")
        replies = [
            "Wah, menarik sekali! Ceritakan lebih lanjut?",
            "Maaf, otak saya lagi dipinjam Furqon buat nabung dulu.",
            "Hmm, menurut pendapat saya itu logis.",
            "Oke, saya catat ya!"
        ]
        bot_reply = random.choice(replies)
        
    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    app.run(debug=True)