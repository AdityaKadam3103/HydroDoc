# 💧 HydroDoc: Waterborne Disease Risk Checker

HydroDoc is an AI-powered multilingual chatbot that helps users assess their risk of waterborne diseases based on symptoms and real-time location. It intelligently asks health-related questions and provides risk assessments, treatment suggestions, and preventive measures — all through a conversational interface.

---

## 🧠 Features

- 💬 Conversational chatbot powered by Google Gemini 1.5
- 🌐 Multilingual support: English, Hindi, Spanish, French
- 🧾 Collects symptoms through 6–7 smart follow-up questions
- 📍 Location-aware context (for future API integration with water/disease data)
- 🩺 Provides a structured health report with:
  - Risk Assessment
  - Probable Diagnosis
  - Severity Level
  - Urgent Concerns
- 💡 Offers treatment plans and preventive guidance

---

## ⚙️ Tech Stack

| Component        | Technology                 |
|------------------|----------------------------|
| Backend          | Python, Flask              |
| AI Model         | Google Gemini 1.5 Flash    |
| Frontend         | HTML/CSS (with Flask templating) |
| API Integration  | Google Generative AI API   |
| Language Support | System prompts for multilingual output |
| Deployment       | Localhost / Render / Replit-ready |

---

## 🚀 Getting Started

### 🔧 Requirements

- Python 3.8+
- Flask
- `google-generativeai` Python package

### 📦 Installation

```bash
git clone https://github.com/your-username/HydroDoc.git
cd HydroDoc
pip install -r requirements.txt
🧠 Prompt Engineering
HydroDoc uses structured system prompts to:

Ask 6–7 symptom-related questions

Track conversation history and user responses

Generate a final health report with AI

Recommend treatment and water safety practices

Prompts are tailored for each language to ensure clarity, empathy, and usability.

🌐 Future Enhancements
Integrate with live water quality APIs (e.g., EPA, OpenWaterData)

Track disease outbreaks using WHO or HealthMap APIs

Add user authentication and chatbot history dashboard

📄 License
This project is open-source and available under the MIT License.


