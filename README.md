# Visionary Health Tracker

[![Author](https://img.shields.io/badge/Author-Sharvan%20Gajula-8b5cf6?style=for-the-badge)](https://www.linkedin.com/in/sharvan-gajula/)
[![GitHub](https://img.shields.io/badge/GitHub-mani--1509-4c1d95?style=for-the-badge&logo=github)](https://github.com/mani-1509)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sharvan%20Gajula-0077b5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/sharvan-gajula/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.1-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**Visionary Health Tracker** is an intelligent, AI-powered health and wellness application. By integrating multimodal Computer Vision (`Qwen/Qwen2.5-VL-72B-Instruct`) and LLM telemetry analysis (`Llama-3.3-70B-Instruct`) via Nebius AI Token Factory, the platform provides real-time meal scanning, workout feedback, vitals tracking, and interactive health analytics.

---

## Key Features & Architecture

### 1. Live Vision & Meal Telemetry
- **Webcam & File Upload**: Real-time camera viewfinder with scanning animations or file/URL drag-and-drop.
- **Multimodal AI Analysis**: Powered by `Qwen/Qwen2.5-VL-72B-Instruct` to analyze food items for nutritional breakdown, healthier meal alternatives, and exercise form feedback.

### 2. Vital Signs Telemetry & AI Health Advisor
- **Metric Inputs**: Input vital metrics including Heart Rate (BPM), Blood Pressure (Systolic/Diastolic mmHg), and Daily Caloric Intake (Kcal).
- **Personalized Recommendations**: Instant LLM-generated health advice tailored to your vital telemetry.

### 3. Interactive Analytics & Progress Dashboard
- **Chart.js Graphs**: Interactive line charts with smooth curve gradients displaying historical trends.
- **Metrics Timeline**: History list of recorded metrics with date badges and status pills.

### 4. Glassmorphic UI/UX Design System
- Built with a modern Midnight Purple & Violet glassmorphism design system (`#0f0a21`, `#8b5cf6`, `#f3e8ff`).
- Integrated Google Fonts (`Plus Jakarta Sans` & `Outfit`), micro-animations, and responsive navbar.

### 5. Authentication & Data Privacy
- User registration & login system with password hashing (`Werkzeug`).
- Data management settings to view account details or clear metrics history.

---

## Technology Stack

- **Backend**: Python 3.12, Flask 3.1, Flask-SQLAlchemy, Werkzeug, python-dotenv
- **AI Models & API**: Nebius AI Token Factory API (`https://api.tokenfactory.nebius.com/v1/`), `Qwen/Qwen2.5-VL-72B-Instruct` (Vision), `meta-llama/Llama-3.3-70B-Instruct` (Health Tips)
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism & CSS Variables), JavaScript (ES6+), Chart.js, Marked.js
- **Database**: SQLite (SQLAlchemy 2.0 ORM)
- **Testing**: pytest test suite

---

## Quick Start & Installation

### Prerequisites
- Python 3.12 (Recommended)
- Git

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mani-1509/Visionary-Health-Tracker.git
   cd Visionary-Health-Tracker
   ```

2. **Create & Activate Virtual Environment**:
   ```powershell
   py -3.12 -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables (`.env`)**:
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY="your_secret_key"
   NEBIUS_API_KEY="your_nebius_api_key"
   NEBIUS_BASE_URL="https://api.tokenfactory.nebius.com/v1/"
   NEBIUS_VISION_MODEL="Qwen/Qwen2.5-VL-72B-Instruct"
   CLOUDINARY_CLOUD_NAME="your_cloud_name"
   CLOUDINARY_API_KEY="your_api_key"
   CLOUDINARY_API_SECRET="your_api_secret"
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   Open your browser at `http://127.0.0.1:8000`.

---

## Automated Testing

Run the automated test suite with `pytest`:

```powershell
python -m pytest tests/
```

**Test Coverage**:
- Index & navigation routes
- User registration, duplicate checks & password hashing
- User login, invalid credentials & session persistence
- Health metrics CRUD endpoints
- Metric summary calculation with null/missing value safety
- Profile rendering and settings management

---

## Author & Contact

**Sharvan Gajula** (`mani-1509`)
- **GitHub**: [https://github.com/mani-1509](https://github.com/mani-1509)
- **LinkedIn**: [https://www.linkedin.com/in/sharvan-gajula/](https://www.linkedin.com/in/sharvan-gajula/)
- **Repository**: [https://github.com/mani-1509/Visionary-Health-Tracker](https://github.com/mani-1509/Visionary-Health-Tracker)

---

## License

This project is licensed under the [MIT License](LICENSE).
