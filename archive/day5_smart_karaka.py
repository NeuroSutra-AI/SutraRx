import requests
import spacy

nlp = spacy.load("en_core_web_sm")

# Known drug names we're working with
KNOWN_DRUGS = ["warfarin", "aspirin", "ibuprofen", "acetaminophen", 
               "naproxen", "clopidogrel", "heparin", "digoxin"]

def get_interaction_text(drug_name):
    # Try generic name first
    url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{drug_name}&limit=1"
    response = requests.get(url)
    data = response.json()
    
    # If no results try substance name
    if "results" not in data:
        url = f"https://api.fda.gov/drug/label.json?search=openfda.substance_name:{drug_name}&limit=1"
        response = requests.get(url)
        data = response.json()
    
    if "results" not in data:
        return "No interaction data found"
    
    result = data["results"][0]
    return result.get("drug_interactions", 
           result.get("warnings", ["No interaction data found"]))[0]

def find_drugs_in_sentence(sentence):
    sentence_lower = sentence.lower()
    found = []
    for drug in KNOWN_DRUGS:
        if drug in sentence_lower:
            found.append(drug)
    return found

def smart_karaka(sentence, source_drug):
    doc = nlp(sentence)
    
    roles = {
        "Karta  (Agent)  ": None,
        "Karma  (Object) ": None,
        "Karana (Instr.) ": None,
        "Kriya  (Action) ": None,
    }

    # Extract grammatical roles
    for token in doc:
        if token.dep_ == "ROOT":
            roles["Kriya  (Action) "] = token.text
        elif token.dep_ == "dobj":
            roles["Karma  (Object) "] = token.text

    # Smart Karta: find actual drug name in sentence
    drugs_found = find_drugs_in_sentence(sentence)
    if drugs_found:
        roles["Karta  (Agent)  "] = drugs_found[0]
        if len(drugs_found) > 1:
            roles["Karana (Instr.) "] = drugs_found[1]
    else:
        # fallback to grammatical subject
        for token in doc:
            if token.dep_ == "nsubj":
                roles["Karta  (Agent)  "] = token.text

    return roles

def full_pipeline(drug_name):
    print(f"Drug: {drug_name.upper()}")
    print("=" * 50)
    
    text = get_interaction_text(drug_name)
    sentences = text.split(".")[:4]
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 15:
            roles = smart_karaka(sentence, drug_name)
            print(f"\n  Sentence: {sentence[:80]}")
            for role, word in roles.items():
                if word:
                    print(f"    {role} → {word}")
    
    print()
    print("=" * 50)
    print()

full_pipeline("warfarin")
full_pipeline("aspirin")