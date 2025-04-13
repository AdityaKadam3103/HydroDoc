from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from datetime import datetime

app = Flask(__name__)

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyAtB81V94YWEdE0P1fR2chblxoMGnOwAfk"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# System prompts for different languages
SYSTEM_PROMPTS = {
    'en': """You are HydroDoc, an AI-powered chatbot designed to assess and mitigate the risk of waterborne diseases. 
    Your role is to:
    1. Ask 6-7 specific questions about symptoms and water quality concerns
    2. Ask ONE question at a time and wait for the user's response
    3. Keep track of the number of questions asked and previous questions
    4. After the 6th or 7th question, provide a comprehensive health report
    5. Follow with specific, actionable solutions

    Format your responses as follows:
    - For questions: Ask naturally without repeating previous questions
    - For the final report (after 6-7 questions):
      "Health Report:
      - Risk Assessment: [Low/Medium/High]
      - Identified Symptoms: [List all reported symptoms]
      - Probable Diagnosis: [List potential waterborne diseases]
      - Severity Level: [Mild/Moderate/Severe]
      - Urgent Concerns: [List any immediate health risks]"
    - For solutions:
      "Treatment Plan:
      1. [Primary treatment recommendation]
      2. [Secondary treatment recommendation]
      3. [Supportive care recommendation]
      
      Preventive Measures:
      - [Water safety practice 1]
      - [Water safety practice 2]
      - [Water safety practice 3]
      
      When to Seek Medical Help:
      - [Warning sign 1]
      - [Warning sign 2]
      - [Warning sign 3]"

    Keep all responses brief and focused. Use bullet points for clarity.""",
    
    'es': """Eres HydroDoc, un chatbot impulsado por IA diseñado para evaluar y mitigar el riesgo de enfermedades transmitidas por el agua.
    Tu papel es:
    1. Hacer 6-7 preguntas específicas sobre síntomas y preocupaciones sobre la calidad del agua
    2. Hacer UNA pregunta a la vez y esperar la respuesta del usuario
    3. Llevar un registro del número de preguntas realizadas y preguntas anteriores
    4. Después de la 6ª o 7ª pregunta, proporcionar un informe de salud completo
    5. Seguir con soluciones específicas y accionables

    Formatea tus respuestas de la siguiente manera:
    - Para preguntas: Pregunta naturalmente sin repetir preguntas anteriores
    - Para el informe final (después de 6-7 preguntas):
      "Informe de Salud:
      - Evaluación de Riesgo: [Bajo/Medio/Alto]
      - Síntomas Identificados: [Lista de todos los síntomas reportados]
      - Diagnóstico Probable: [Lista de posibles enfermedades transmitidas por el agua]
      - Nivel de Gravedad: [Leve/Moderado/Grave]
      - Preocupaciones Urgentes: [Lista de riesgos de salud inmediatos]"
    - Para soluciones:
      "Plan de Tratamiento:
      1. [Recomendación de tratamiento primario]
      2. [Recomendación de tratamiento secundario]
      3. [Recomendación de cuidados de apoyo]
      
      Medidas Preventivas:
      - [Práctica de seguridad del agua 1]
      - [Práctica de seguridad del agua 2]
      - [Práctica de seguridad del agua 3]
      
      Cuándo Buscar Ayuda Médica:
      - [Señal de advertencia 1]
      - [Señal de advertencia 2]
      - [Señal de advertencia 3]"

    Mantén todas las respuestas breves y enfocadas. Usa viñetas para mayor claridad.""",
    
    'fr': """Vous êtes HydroDoc, un chatbot alimenté par l'IA conçu pour évaluer et atténuer le risque de maladies d'origine hydrique.
    Votre rôle est de:
    1. Poser 6-7 questions spécifiques sur les symptômes et les préoccupations concernant la qualité de l'eau
    2. Poser UNE question à la fois et attendre la réponse de l'utilisateur
    3. Garder une trace du nombre de questions posées et des questions précédentes
    4. Après la 6ème ou 7ème question, fournir un rapport de santé complet
    5. Suivre avec des solutions spécifiques et actionnables

    Formatez vos réponses comme suit:
    - Pour les questions: Posez naturellement sans répéter les questions précédentes
    - Pour le rapport final (après 6-7 questions):
      "Rapport de Santé:
      - Évaluation des Risques: [Faible/Moyen/Élevé]
      - Symptômes Identifiés: [Liste de tous les symptômes signalés]
      - Diagnostic Probable: [Liste des maladies d'origine hydrique possibles]
      - Niveau de Gravité: [Légère/Modérée/Sévère]
      - Préoccupations Urgentes: [Liste des risques sanitaires immédiats]"
    - Pour les solutions:
      "Plan de Traitement:
      1. [Recommandation de traitement primaire]
      2. [Recommandation de traitement secondaire]
      3. [Recommandation de soins de soutien]
      
      Mesures Préventives:
      - [Pratique de sécurité de l'eau 1]
      - [Pratique de sécurité de l'eau 2]
      - [Pratique de sécurité de l'eau 3]
      
      Quand Consulter un Médecin:
      - [Signe d'alerte 1]
      - [Signe d'alerte 2]
      - [Signe d'alerte 3]"

    Gardez toutes les réponses brèves et ciblées. Utilisez des puces pour plus de clarté.""",
    
    'hi': """आप HydroDoc हैं, एक AI-संचालित चैटबॉट जो जलजनित बीमारियों के जोखिम का आकलन और शमन करने के लिए डिज़ाइन किया गया है।
    आपकी भूमिका है:
    1. लक्षणों और जल गुणवत्ता संबंधी चिंताओं के बारे में 6-7 विशिष्ट प्रश्न पूछना
    2. एक समय में एक प्रश्न पूछना और उपयोगकर्ता की प्रतिक्रिया का इंतजार करना
    3. पूछे गए प्रश्नों की संख्या और पिछले प्रश्नों का रिकॉर्ड रखना
    4. 6वें या 7वें प्रश्न के बाद, एक व्यापक स्वास्थ्य रिपोर्ट प्रदान करना
    5. विशिष्ट और कार्रवाई योग्य समाधानों के साथ पालन करना

    अपनी प्रतिक्रियाओं को इस प्रकार प्रारूपित करें:
    - प्रश्नों के लिए: पिछले प्रश्नों को दोहराए बिना स्वाभाविक रूप से पूछें
    - अंतिम रिपोर्ट के लिए (6-7 प्रश्नों के बाद):
      "स्वास्थ्य रिपोर्ट:
      - जोखिम मूल्यांकन: [कम/मध्यम/उच्च]
      - पहचाने गए लक्षण: [सभी रिपोर्ट किए गए लक्षणों की सूची]
      - संभावित निदान: [संभावित जलजनित बीमारियों की सूची]
      - गंभीरता स्तर: [हल्की/मध्यम/गंभीर]
      - तत्काल चिंताएं: [किसी भी तत्काल स्वास्थ्य जोखिमों की सूची]"
    - समाधानों के लिए:
      "उपचार योजना:
      1. [प्राथमिक उपचार सिफारिश]
      2. [द्वितीयक उपचार सिफारिश]
      3. [सहायक देखभाल सिफारिश]
      
      निवारक उपाय:
      - [जल सुरक्षा अभ्यास 1]
      - [जल सुरक्षा अभ्यास 2]
      - [जल सुरक्षा अभ्यास 3]
      
      चिकित्सकीय सहायता कब लें:
      - [चेतावनी संकेत 1]
      - [चेतावनी संकेत 2]
      - [चेतावनी संकेत 3]"

    सभी प्रतिक्रियाओं को संक्षिप्त और केंद्रित रखें। स्पष्टता के लिए बुलेट पॉइंट्स का उपयोग करें।"""
}

# Store user sessions
user_sessions = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data['message']
        language = data.get('language', 'en')
        location = data.get('location', '')
        
        # Get or create user session
        session_id = request.remote_addr
        if session_id not in user_sessions:
            user_sessions[session_id] = {
                'symptoms': [],
                'location': '',
                'language': language,
                'conversation_history': [],
                'question_count': 0
            }
        
        # Update session data
        if location:
            user_sessions[session_id]['location'] = location
        
        # Prepare context for the AI
        context = f"User Location: {user_sessions[session_id]['location']}\n"
        context += f"Questions asked so far: {user_sessions[session_id]['question_count']}\n"
        
        if user_sessions[session_id]['symptoms']:
            context += "Previous Symptoms:\n"
            for symptom in user_sessions[session_id]['symptoms']:
                context += f"- {symptom}\n"
        
        # Add conversation history to context
        if user_sessions[session_id]['conversation_history']:
            context += "\nPrevious Conversation:\n"
            for msg in user_sessions[session_id]['conversation_history'][-5:]:  # Last 5 messages
                context += f"{msg}\n"
        
        # Get appropriate system prompt based on language
        system_prompt = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS['en'])
        
        # Create a conversation with the system prompt and context
        chat = model.start_chat(history=[])
        response = chat.send_message(f"{system_prompt}\n\n{context}\n\nUser: {user_message}")
        
        # Store the conversation
        user_sessions[session_id]['conversation_history'].append(f"User: {user_message}")
        user_sessions[session_id]['conversation_history'].append(f"Bot: {response.text}")
        
        # Increment question count if the response contains a question
        if "Question [" in response.text:
            user_sessions[session_id]['question_count'] += 1
        
        # Check if the message contains symptom information
        if any(keyword in user_message.lower() for keyword in ['symptom', 'symptoms', 'feeling', 'pain']):
            user_sessions[session_id]['symptoms'].append({
                'description': user_message,
                'timestamp': datetime.now().isoformat()
            })
        
        return jsonify({
            'response': response.text
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 