import streamlit as st
import requests
import openai

# Clé API OpenAI (à remplacer par ta vraie clé)
openai.api_key = "TON_OPENAI_API_KEY"

# Clé API Spoonacular (à remplacer par ta vraie clé)
SPOONACULAR_API_KEY = "TON_SPOONACULAR_API_KEY"
SPOONACULAR_URL = "https://api.spoonacular.com/recipes/complexSearch"

# Interface de l'application
st.title("🍽️ Trouve ta recette idéale !")

# Message d'accueil
st.subheader("Je suis ton assistant culinaire 🤖🍽️, et je vais t’aider à trouver la recette parfaite en fonction de tes goûts et besoins !")
st.write("Prêt(e) ? Commençons ! ⏳🍲")

# Étape 1 : Questionnaire interactif
st.header("📝 Réponds à ces questions !")

type_repas = st.selectbox("Quel type de repas recherchez-vous ?", ["Déjeuner", "Plat principal", "Entrée", "Dessert", "Salade", "Collation"])

intolerances = st.multiselect("Avez-vous des allergies ou intolérances ?", ["Œufs", "Produits laitiers", "Gluten", "Grain", "Moutarde", "Arachide", "Noix", "Mollusques et crustacés", "Poissons", "Fruits de mer", "Graines de sésame", "Soja", "Sulfites", "Blé et triticale", "Fruit", "Légumes", "Aucune allergie et/ou intolérance"])

regime = st.selectbox("Suivez-vous un régime alimentaire restrictif ?", ["Végétarien", "Végétalien", "Pesco-végétarisme", "Sans gluten", "Cétogène (keto)", "Lacto-Vegetarian", "Ovo-Vegetarian", "Paleo", "Primal", "Low FODMAP", "Whole30", "Aucun régime"])

st.header("📊 Restrictions nutritionnelles")
minProtein, maxProtein = st.slider("Protéines (g)", 0, 100, (0, 100))
minSugar, maxSugar = st.slider("Sucre (g)", 0, 100, (0, 100))
minCalories, maxCalories = st.slider("Calories", 0, 2000, (0, 2000))
minCholesterol, maxCholesterol = st.slider("Cholestérol (mg)", 0, 500, (0, 500))
minFat, maxFat = st.slider("Lipides saturés (g)", 0, 100, (0, 100))
minCalcium, maxCalcium = st.slider("Calcium (mg)", 0, 2000, (0, 2000))
minSodium, maxSodium = st.slider("Sodium (mg)", 0, 2000, (0, 2000))
minPotassium, maxPotassium = st.slider("Potassium (mg)", 0, 2000, (0, 2000))

includeIngredients = st.text_input("Quels ingrédients aimeriez-vous inclure dans votre recette ? (séparés par des virgules)")
cuisine = st.selectbox("Préférez-vous un type de cuisine ?", ["Asiatique", "Africain", "Américain", "Cajun", "Caribbean", "Chinois", "Europe de l’est", "Européen", "Français", "Allemand", "Grecque", "Indien", "Irlandais", "Italien", "Japonais", "Juif", "Koréen", "Amérique Latine", "Méditérannéain", "Mexicain", "Moyen-Orient", "Nordique", "Espagnol", "Thai", "Vietnamien", "Pas d’importance"])

temps = st.slider("Temps de préparation max (minutes)", 20, 180, 60)
equipment = st.radio("Préférez-vous cuisiner avec le four ou le airfryer ?", ["Airfryer", "Four", "Les deux"])

# Étape 2 : Recherche de recette
if st.button("🔍 Trouver une recette"):
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "diet": regime,
        "intolerances": ",".join(intolerances),
        "includeIngredients": includeIngredients,
        "cuisine": cuisine,
        "maxReadyTime": temps,
        "number": 1
    }
    response = requests.get(SPOONACULAR_URL, params=params)
    data = response.json()

    if "results" in data and data["results"]:
        recette = data["results"][0]
        st.subheader(f"🍽️ {recette['title']}")
        st.image(recette["image"], width=400)
        st.write("🔗 Voir la recette :", recette["sourceUrl"])
    else:
        st.error("Aucune recette trouvée, essaye d'autres paramètres !")

# Étape 3 : Chatbot IA pour répondre aux questions
st.header("💬 Pose tes questions sur la recette !")
user_question = st.text_input("Pose une question :")
if user_question:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_question}]
    )
    st.write("🤖 Chatbot :", response["choices"][0]["message"]["content"])
