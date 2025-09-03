# 🚗 AutoScout Pro - Car Finder – AI-Powered Car Search

Car Finder is a **Flutter + FastAPI app** that allows users to search for cars using **natural language questions** in **English or French**.  
Powered by **Google Gemini**, the app converts your query into SQL, runs it on a local database, and displays matching cars in a clean, modern UI.

---

## ✨ Features
- 🔎 **Natural Language Search** – Ask questions like:  
  - “Show me the 3 cheapest Peugeot cars”  
  - “Find the latest automatic Mercedes under 7000 euros”  
- 🌍 **Multilingual** – Works with both **English and French** queries.  
- 🤖 **AI-Powered** – Gemini converts questions into smart SQL queries.  
- 🛠 **Error Tolerant** – Understands typos or misspellings (e.g., *“fnd me”* → *“find me”*).  
- 📊 **Car Database** – Brand, model, year, price, mileage, transmission, fuel, power, and posting date.  
- 📱 **Flutter App** – Modern card-based UI, car details page, search bar with clear & search buttons.  
- ⚡ **FastAPI Backend** – Handles requests, executes SQL on SQLite (`cars.db`), and returns structured results.

---


## 🚀 Getting Started

### 1️⃣ Backend Setup (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate   # (or venv\Scripts\activate on Windows)
pip install -r requirements.txt
uvicorn main:app --reload
By default, the backend runs on http://127.0.0.1:8000
```

---

### 2️⃣ Frontend Setup (Flutter)
```bash
cd frontend
flutter pub get
flutter run
```

## Demo
https://github.com/user-attachments/assets/e2f3646a-6ec7-4d5c-bfe2-b34e7519611a



