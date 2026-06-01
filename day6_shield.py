import requests
import spacy

nlp = spacy.load("en_core_web_sm")

KNOWN_DRUGS = ["warfarin", "aspirin", "ibuprofen", "acetaminophen",
               "naproxen", "clopidogrel", "heparin", "digoxin",
               "metformin", "lisinopril", "atorvastatin", "amoxicillin"]

# Drug category mapping
DRUG_CATEGORIES = {
    "warfarin": ["anticoagulant", "blood thinner", "coumarin"],
    "aspirin": ["nsaid", "salicylate", "antiplatelet", "blood thinner"],
    "ibuprofen": ["nsaid", "anti-inflammatory", "antiplatelet"],
    "heparin": ["anticoagulant", "blood thinner"],
    "clopidogrel": ["antiplatelet", "blood thinner"],
    "naproxen": ["nsaid", "anti-inflammatory"],
    "acetaminophen": ["analgesic", "antipyretic"],
}

def drugs_share_category(drug_a, drug_b):
    cats_a = set(DRUG_CATEGORIES.get(drug_a.lower(), []))
    cats_b = set(DRUG_CATEGORIES.get(drug_b.lower(), []))
    shared = cats_a.intersection(cats_b)
    return shared

def get_interaction_text(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{drug_name}&limit=1"
    response = requests.get(url)
    data = response.json()

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
    return [drug for drug in KNOWN_DRUGS if drug in sentence_lower]

def karaka_extract(sentence):
    doc = nlp(sentence)
    roles = {}
    for token in doc:
        if token.dep_ == "ROOT":
            roles["Kriya"] = token.text
        elif token.dep_ == "dobj":
            roles["Karma"] = token.text

    drugs = find_drugs_in_sentence(sentence)
    if len(drugs) >= 1:
        roles["Karta"] = drugs[0]
    if len(drugs) >= 2:
        roles["Karana"] = drugs[1]

    return roles, drugs

def shield_check(drug_a, drug_b):
    print(f"🛡️  SUTRARX SHIELD")
    print(f"Checking: {drug_a.upper()} + {drug_b.upper()}")
    print("=" * 50)

    flagged = False
    flag_reasons = []

    # Layer 1: Check drug_a FDA text for drug_b
    text = get_interaction_text(drug_a)
    sentences = text.split(".")

    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) < 15:
            continue

        roles, drugs_found = karaka_extract(sentence)

        if drug_a.lower() in [d.lower() for d in drugs_found] and \
           drug_b.lower() in [d.lower() for d in drugs_found]:
            flagged = True
            action = roles.get("Kriya", "interact")
            flag_reasons.append({
                "sentence": sentence[:100],
                "action": action,
                "roles": roles,
                "source": "FDA text match"
            })

    # Layer 2: Check drug_b FDA text for drug_a
    text_b = get_interaction_text(drug_b)
    for sentence in text_b.split("."):
        sentence = sentence.strip()
        if len(sentence) < 15:
            continue
        roles, drugs_found = karaka_extract(sentence)
        if drug_a.lower() in [d.lower() for d in drugs_found] and \
           drug_b.lower() in [d.lower() for d in drugs_found]:
            flagged = True
            action = roles.get("Kriya", "interact")
            flag_reasons.append({
                "sentence": sentence[:100],
                "action": action,
                "roles": roles,
                "source": "FDA text match"
            })

    # Layer 3: Category based check
    if not flagged:
        shared_cats = drugs_share_category(drug_a, drug_b)
        if shared_cats:
            flagged = True
            flag_reasons.append({
                "sentence": f"Both {drug_a} and {drug_b} belong to category: {', '.join(shared_cats)}",
                "action": "share pathway",
                "roles": {"Karta": drug_a, "Karana": drug_b},
                "source": "Category match"
            })

    # Output
    if flagged:
        print(f"⚠️  STATUS: FLAGGED — INTERACTION DETECTED")
        print()
        for i, reason in enumerate(flag_reasons[:2]):
            print(f"  Reason {i+1}: [{reason['source']}]")
            print(f"  Sentence : {reason['sentence']}")
            print(f"  Action   : {reason['action']}")
            print(f"  Kartā    : {reason['roles'].get('Karta', 'unknown')}")
            print(f"  Karaṇā   : {reason['roles'].get('Karana', 'unknown')}")
            print()
    else:
        print(f"✅ STATUS: No interaction detected")

    print("=" * 50)
    print()

# Test Shield
shield_check("warfarin", "aspirin")
shield_check("aspirin", "ibuprofen")
shield_check("warfarin", "ibuprofen")
shield_check("warfarin", "heparin")