
from flask import Flask, render_template, request,  url_for, session
import random
import os
from proof_generator import generate_fake_proof
from datetime import datetime
from googletrans import Translator



app = Flask(__name__)
app.secret_key = "your-secret-key"
translator = Translator()


translations = {
    'en': {
        'excuse_header': "Excuse Generator",
        'excuse_intro': "Make your absence legendary 💌",
        'choose_scenario': "Choose a scenario:",
        'generate_excuse': "🎲 Generate Excuse",
        'apology_link': "Need to apologize? Generate a guilt-tripping apology 💔",
        'work': "Work",
        'school': "School",
        'social': "Social",
        'family': "Family",
        'history': "History",
        'favorites': "Favorites",
         'your_excuse': "Your Excuse:",
        'fake_proof': "Fake Proof:",
        'top_excuses': "Top Excuses:",
        'prediction': "Prediction: Based on your history, you may need your next excuse on:",
        'play_excuse': "▶️ Play Excuse"
    },
    'es': {
        'excuse_header': "Generador de Excusas",
        'excuse_intro': "Haz que tu ausencia sea legendaria 💌",
        'choose_scenario': "Elige un escenario:",
        'generate_excuse': "🎲 Generar Excusa",
        'apology_link': "¿Necesitas disculparte? Genera una disculpa emocional 💔",
        'work': "Trabajo",
        'school': "Escuela",
        'social': "Social",
        'family': "Familia",
        'history': "Historial",
        'favorites': "Favoritos",
        'your_excuse': "Tu excusa:",
        'fake_proof': "Prueba falsa:",
        'top_excuses': "Principales excusas:",
        'prediction': "Predicción: Según tu historial, podrías necesitar tu próxima excusa el:",
        'play_excuse': "▶️ Reproducir excusa"
    },
    'fr': {
        'excuse_header': "Générateur d'Excuses",
        'excuse_intro': "Rendez votre absence légendaire 💌",
        'choose_scenario': "Choisissez un scénario :",
        'generate_excuse': "🎲 Générer une excuse",
        'apology_link': "Besoin de vous excuser ? Générer une excuse pleine de culpabilité 💔",
        'work': "Travail",
        'school': "École",
        'social': "Social",
        'family': "Famille",
        'history': "Historique",
        'favorites': "Favoris",
         'your_excuse': "Votre excuse:",
        'fake_proof': "Fausse preuve:",
        'top_excuses': "Meilleures excuses:",
        'prediction': "Prévision : Basé sur votre historique, vous pourriez avoir besoin de votre prochaine excuse le:",
        'play_excuse': "▶️ Lire l'excuse"
    },
    'hi': {
        'excuse_header': "बहाना जनरेटर",
        'excuse_intro': "अपनी गैरमौजूदगी को यादगार बनाएं 💌",
        'choose_scenario': "एक स्थिति चुनें:",
        'generate_excuse': "🎲 बहाना जनरेट करें",
        'apology_link': "माफी मांगनी है? एक दिल छू लेने वाली माफी जनरेट करें 💔",
        'work': "काम",
        'school': "स्कूल",
        'social': "सामाजिक",
        'family': "परिवार",
        'history': "इतिहास",
        'favorites': "पसंदीदा",
         'your_excuse': "आपका बहाना:",
        'fake_proof': "नकली सबूत:",
        'top_excuses': "शीर्ष बहाने:",
        'prediction': "भविष्यवाणी: आपके इतिहास के आधार पर, अगला बहाना आपको इस दिन ज़रूरत पड़ सकती है:",
        'play_excuse': "▶️ बहाना सुनें"
    },
    'te': {
        'excuse_header': "నెపం జనరేటర్",
        'excuse_intro': "మీ గైర్హాజరును చరిత్రలో నిలుపుకోండి 💌",
        'choose_scenario': "ఒక పరిస్థిని ఎంచుకోండి:",
        'generate_excuse': "🎲 నెపం తయారు చేయండి",
        'apology_link': "క్షమాపణ చెప్పాలా? మర్మమైన క్షమాపణను రూపొందించండి 💔",
        'work': "పని",
        'school': "పాఠశాల",
        'social': "సామాజిక",
        'family': "కుటుంబం",
        'history': "చరిత్ర",
        'favorites': "ఇష్టమైనవి",
         'your_excuse': "మీ నెపం:",
        'fake_proof': "నకిలీ ఆధారం:",
        'top_excuses': "అగ్ర నెపాలు:",
        'prediction': "అంచనా: మీ చరిత్ర ఆధారంగా, మీకు వచ్చే నెపం అవసరం అయ్యే రోజు:",
        'play_excuse': "▶️ నెపం వినండి"
    }
}


# --- Excuse + Proof Mappings ---
excuse_proofs = {
    "Work": [
        ("I'm feeling unwell and didn’t want to risk spreading anything.", "proof6.jpg"),
        ("There was an unexpected power outage at my place.", "proof5.jpg"),
        ("My internet went down just before the meeting.", "proof4.jpg"),
        ("I had to handle a family emergency this morning.", "proof13.jpg")
    ],
    "School": [
        ("I had a doctor's appointment that ran longer than expected.", "proof6.jpg"),
        ("My younger sibling was sick and I had to take care of them.", "proof9.jpg"),
        ("There was a transportation strike in my area.", "proof2.jpg"),
        ("I lost track of time while working on another assignment.", "proof12.jpg")
    ],
    "Social": [
        ("I wasn't feeling mentally up to socializing today.", "proof1.jpg"),
        ("My pet had a small emergency and needed my attention.", "proof3.jpg"),
        ("I got caught up in work and lost track of time.", "proof4.jpg"),
        ("There was a last-minute family gathering I couldn’t skip.", "proof8.jpg")
    ],
    "Family": [
        ("I was helping a relative with a medical emergency.", "proof13.jpg"),
        ("There was an issue at home that needed my immediate attention.", "proof9.jpg"),
        ("I was caught up in an important family conversation.", "proof9.jpg"),
        ("We had an unexpected visitor I couldn’t leave unattended.", "proof10.jpg")
    ]
}

# --- Apology Templates ---
apology_templates = {
    "Work": [
        "I'm truly sorry for missing work. It wasn’t my intention to let anyone down.",
        "I know how important today was — please believe that I deeply regret not being there.",
        "Work matters to me, and I feel awful that I couldn’t show up when it mattered most."
    ],
    "School": [
        "I take full responsibility for not being present. I'm deeply sorry to my classmates and teachers.",
        "I hate that I let this happen — I’ll do everything I can to make it right.",
        "It’s not an excuse, just a sincere apology. I hope I can earn back your trust."
    ],
    "Family": [
        "I never meant to let the family down. I hope you know how bad I feel.",
        "Please forgive me — I value our time together and hate that I missed it.",
        "Family means the world to me. I’m genuinely sorry for my absence."
    ],
    "Social": [
        "I was really looking forward to it. I’m so sorry I couldn’t make it.",
        "I feel like I let everyone down — I hope you can understand.",
        "Please know I regret not showing up — it wasn’t intentional."
    ]
}
top_excuses = []
scheduled_excuses = []

def rank_excuses(excuse_list):
    ranked = []
    for excuse in excuse_list:
        score = 0
        if "emergency" in excuse.lower():
            score += 5
        if "doctor" in excuse.lower() or "medical" in excuse.lower():
            score += 4
        if "internet" in excuse.lower():
            score += 3
        if "transport" in excuse.lower() or "power outage" in excuse.lower():
            score += 2
        if "family" in excuse.lower():
            score += 1
        
        ranked.append((score, excuse))

    ranked.sort(reverse=True)
    return [exc for score, exc in ranked]

def predict_next_excuse_time(history):
    from collections import Counter
    from datetime import timedelta

    if not history:
        return "No data to predict."
    
    valid_entries = [entry for entry in history if isinstance(entry, dict) and "timestamp" in entry]

    if not valid_entries:
        return "No valid history entries."

    times = [datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S") for entry in history]
    days_of_week = [time.weekday() for time in times]  # 0 = Monday

    # Most common day
    common_day = Counter(days_of_week).most_common(1)[0][0]

    # Estimate next occurrence of that weekday
    today = datetime.now()
    days_until_next = (common_day - today.weekday()) % 7
    predicted_date = today + timedelta(days=days_until_next)

    # Predict similar time based on average hour
    avg_hour = sum(time.hour for time in times) / len(times)
    predicted_time = predicted_date.replace(hour=int(avg_hour), minute=0, second=0, microsecond=0)

    return predicted_time.strftime("%A, %Y-%m-%d at %I:%M %p")


@app.route('/', methods=['GET', 'POST'])
def index():
    
    selected_language = request.form.get('language')
    if not selected_language:
        selected_language = request.args.get('lang')
    if not selected_language:
        selected_language = 'en-US'
    lang_code = selected_language.split('-')[0]  # en-US -> en
    language_dict = translations.get(lang_code, translations['en'])


    if "history" not in session:
        session["history"] = []
    if "favorites" not in session:
        session["favorites"] = []

    session["history"] = []

    excuse = None
    proof = None
    top_3_excuses = []
  
    #selected_language = request.form.get('language', 'en-US') # default language


    if request.method == 'POST':
        scenario = request.form.get('scenario')
        urgency = request.form.get('urgency')
        selected_language = request.form.get('language', 'en-US')
    
        if scenario in excuse_proofs:
    # Fetch all excuses for the selected scenario
           all_excuses_proofs = excuse_proofs[scenario]

    # Extract only excuses (texts) for ranking
           all_excuses = [exc for exc, proof_file in all_excuses_proofs]

    # Rank excuses
           ranked_excuses = rank_excuses(all_excuses)

    # Pick the best excuse (top-ranked)
           best_excuse = ranked_excuses[0]
           top_3_excuses = ranked_excuses[:3] 

    # Find corresponding proof image
           for exc, proof_filename in all_excuses_proofs:
               if exc == best_excuse:
                   proof = url_for('static', filename=f'proofs/{proof_filename}')
                   break

           excuse = best_excuse

        else:
            excuse = f"Sorry, I couldn't attend due to a {scenario} emergency."
            proof = url_for('static', filename='proofs/default_proof.jpg')

        # --- Translate excuse based on selected language ---
        target_lang = selected_language.split('-')[0]  # en-US -> en
        if target_lang != 'en':  # Only translate if not English
            try:
               translation = translator.translate(excuse, dest=target_lang)
               excuse = translation.text
            except Exception as e:
               print("Translation error:", e)
        # If translation fails, keep the original English excuse
        
         # Save excuse to history with timestamp
        session["history"].append({
            "excuse": excuse,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        session.modified = True

    language_dict = translations.get(selected_language[:2], translations['en'])
    predicted_schedule = predict_next_excuse_time(session.get("history", []))

        
    return render_template('index.html', excuse=excuse, proof=proof,selected_language=selected_language, language_dict=language_dict,top_excuses=top_3_excuses, predicted_schedule=predicted_schedule)


@app.route("/history")
def history():
    lang = request.args.get('lang', 'en')
    language_dict = translations.get(lang, translations['en'])

    return render_template("history.html",
                           history=session.get("history", []),
                           favorites=session.get("favorites", []),
                           language_dict=language_dict)

@app.route("/favorite", methods=["POST"])
def favorite():
    excuse = request.form.get("excuse")
    if excuse and excuse not in session["favorites"]:
        session["favorites"].append(excuse)
        session.modified = True
    return (url_for("history"))


@app.route('/apology', methods=['GET', 'POST'])
def apology():
    apology_message = None
    proof = None
    lang = request.args.get('lang', 'en')
    language_dict = translations.get(lang, translations['en'])


    if request.method == 'POST':
        scenario = request.form.get('scenario')
        urgency = request.form.get("urgency")
        tone = request.form.get('tone')

        if scenario in apology_templates:
            apology_message = random.choice(apology_templates[scenario])
            proof = generate_fake_proof(urgency)

    return render_template('apology.html', apology=apology_message, proof=proof, language_dict=language_dict)

if __name__ == "__main__":
    app.run(debug=True)
