# Visionary Health Tracker (`mani-1509`)

[![Author](https://img.shields.io/badge/Author-Sharvan%20Gajula-8b5cf6?style=for-the-badge)](https://www.linkedin.com/in/sharvan-gajula/)
[![GitHub](https://img.shields.io/badge/GitHub-mani--1509-4c1d95?style=for-the-badge&logo=github)](https://github.com/mani-1509)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sharvan%20Gajula-0077b5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/sharvan-gajula/)

## Overview
Visionary Health Tracker is a next-generation web application designed to assist users in monitoring and optimizing their health and wellness. Powered by multimodal vision AI models (Qwen2-VL 72B) and LLM wellness advisors (Llama 3.3 70B), the app provides real-time computer vision analysis on meals and workout setups, as well as personalized health telemetry advice and interactive trends tracking.

---

## Features
1. **Live Image & Meal Recognition**:
   - Scan meals or exercise setups using live camera stream or file upload.
   - Provides AI-driven nutritional breakdown, health feedback, and healthier meal alternatives.

2. **Vital Signs Telemetry Tracking**:
   - Log vital metrics such as heart rate (BPM), blood pressure (mmHg), and daily caloric intake (Kcal).
   - Generates personalized AI wellness advice tailored to your current metrics.

3. **Analytics & Historical Dashboard**:
   - Interactive Chart.js graphs displaying heart rate, blood pressure, and calorie trends over time.
   - History logs timeline for past entries.

4. **User Authentication & Profile**:
   - Secure login & registration system with hashed passwords and session management.
   - Personalized user profile and data management settings.

---

## Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mani-1509/Visionary-Health-Tracker.git
   cd Visionary-Health-Tracker
   ```

2. **Create & Activate Virtual Environment**:
   ```bash
   py -3.12 -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables** *(Optional for AI Features)*:
   ```bash
   $env:NEBIUS_API_KEY="your_nebius_api_key"
   $env:CLOUDINARY_CLOUD_NAME="your_cloud_name"
   $env:CLOUDINARY_API_KEY="your_api_key"
   $env:CLOUDINARY_API_SECRET="your_api_secret"
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   Open your browser at `http://127.0.0.1:8000`.

---

## Running Automated Tests

Run the test suite using `pytest`:

```bash
python -m pytest tests/
```

---

## Developer Contact & Links

- **Creator**: Sharvan Gajula
- **GitHub**: [https://github.com/mani-1509](https://github.com/mani-1509)
- **LinkedIn**: [https://www.linkedin.com/in/sharvan-gajula/](https://www.linkedin.com/in/sharvan-gajula/)
- **Repository**: [https://github.com/mani-1509/Visionary-Health-Tracker](https://github.com/mani-1509/Visionary-Health-Tracker)

---

## License

Licensed under the [MIT License](LICENSE).
