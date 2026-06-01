import requests
import spacy

nlp = spacy.load("en_core_web_sm")

# ─────────────────────────────────────────
# KNOWLEDGE BASE
# ─────────────────────────────────────────

KNOWN_DRUGS = [
    "warfarin", "aspirin", "ibuprofen", "acetaminophen",
    "naproxen", "clopidogrel", "heparin", "digoxin",
    "metformin", "lisinopril", "atorvastatin", "amoxicillin",
    "methotrexate", "lithium", "fluoxetine", "sertraline"
]

DRUG_CATEGORIES = {
    "warfarin":       ["anticoagulant", "blood thinner", "coumarin"],
    "aspirin":        ["nsaid", "salicylate", "antiplatelet", "blood thinner"],
    "ibuprofen":      ["nsaid", "anti-inflammatory", "antiplatelet"],
    "naproxen":       ["nsaid", "anti-inflammatory"],
    "heparin":        ["anticoagulant", "blood thinner"],
    "clopidogrel":    ["antiplatelet", "blood thinner"],
    "acetaminophen":  ["analgesic", "antipyretic"],
    "methotrexate":   ["antimetabolite", "immunosuppressant"],
    "lithium":        ["mood stabilizer"],
    "fluoxetine":     ["ssri", "antidepressant"],
    "sertraline":     ["ssri", "antidepressant"],
    "digoxin":        ["cardiac glycoside", "antiarrhythmic"],
}

KARAKA_WHY = {
    ("warfarin", "aspirin"): {
        "mechanism": "Both inhibit clotting through different pathways",
        "karaka": "Warfarin (Kartā) blocks Vitamin K clotting factors (Karma). Aspirin (Kartā) inhibits platelet aggregation (Karma). Combined — dual pathway blockage.",
        "risk": "Severe bleeding risk — internal hemorrhage possible",
        "confidence": "HIGH",
        "action": "Do NOT dispense together without doctor confirmation"
    },
    ("warfarin", "ibuprofen"): {
        "mechanism": "Ibuprofen displaces warfarin from plasma proteins",
        "karaka": "Ibuprofen (Kartā) acts on plasma proteins (Karaṇā) to displace warfarin (Karma) — increasing free warfarin in blood.",
        "risk": "Warfarin toxicity — uncontrolled anticoagulation",
        "confidence": "HIGH",
        "action": "Do NOT dispense together without doctor confirmation"
    },
    ("aspirin", "ibuprofen"): {
        "mechanism": "Both inhibit COX enzymes — same pathway, compounding effect",
        "karaka": "Aspirin (Kartā) and Ibuprofen (Kartā) both act on COX-1/COX-2 enzymes (Karma) via the same prostaglandin pathway (Karaṇā).",
        "risk": "GI bleeding, stomach ulcers, kidney damage",
        "confidence": "HIGH",
        "action": "Avoid combination — use one NSAID only"
    },
    ("warfarin", "heparin"): {
        "mechanism": "Both are anticoagulants — additive bleeding effect",
        "karaka": "Warfarin (Kartā) and Heparin (Kartā) both inhibit coagulation cascade (Karma) through different but overlapping pathways (Karaṇā).",
        "risk": "Extreme bleeding risk — life threatening",
        "confidence": "HIGH",
        "action": "Hospital use only — requires continuous monitoring"
    },
    ("fluoxetine", "sertraline"): {
        "mechanism": "Both are SSRIs — serotonin overload",
        "karaka": "Fluoxetine (Kartā) and Sertraline (Kartā) both inhibit serotonin reuptake (Karma) via the same transporter (Karaṇā).",
        "risk": "Serotonin syndrome — potentially fatal",
        "confidence": "HIGH",
        "action": "Never combine two SSRIs — contact doctor immediately"
    },
}

# ─────────────────────────────────────────
# ENGINE
# ─────────────────────────────────────────

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
    return [drug for drug in KNOWN_DRUGS if drug in sentence.lower()]

def drugs_share_category(drug_a, drug_b):
    cats_a = set(DRUG_CATEGORIES.get(drug_a.lower(), []))
    cats_b = set(DRUG_CATEGORIES.get(drug_b.lower(), []))
    return cats_a.intersection(cats_b)

def get_why(drug_a, drug_b):
    key1 = (drug_a.lower(), drug_b.lower())
    key2 = (drug_b.lower(), drug_a.lower())
    return KARAKA_WHY.get(key1) or KARAKA_WHY.get(key2)

def shield_check(drug_a, drug_b):
    print()
    print(f"🛡️  SUTRARX SHIELD")
    print(f"Checking: {drug_a.upper()} + {drug_b.upper()}")
    print("=" * 55)

    flagged = False
    detection_source = None
    detected_sentence = None

    # Layer 1: FDA text match
    for drug in [drug_a, drug_b]:
        text = get_interaction_text(drug)
        for sentence in text.split("."):
            sentence = sentence.strip()
            if len(sentence) < 15:
                continue
            drugs_found = find_drugs_in_sentence(sentence)
            if drug_a.lower() in drugs_found and drug_b.lower() in drugs_found:
                flagged = True
                detection_source = "FDA Label"
                detected_sentence = sentence[:120]
                break
        if flagged:
            break

    # Layer 2: Category match
    if not flagged:
        shared = drugs_share_category(drug_a, drug_b)
        if shared:
            flagged = True
            detection_source = "Category Match"
            detected_sentence = f"Both are: {', '.join(shared)}"

    # Output
    if flagged:
        print(f"⚠️  STATUS   : FLAGGED")
        print(f"📋 DETECTED : {detection_source}")
        print(f"📄 EVIDENCE : {detected_sentence}")
        print()
        why = get_why(drug_a, drug_b)
        if why:
            print(f"🔬 WHY THIS IS DANGEROUS:")
            print(f"   Mechanism  : {why['mechanism']}")
            print()
            print(f"   Kāraka Logic:")
            print(f"   {why['karaka']}")
            print()
            print(f"   Risk       : {why['risk']}")
            print(f"   Confidence : {why['confidence']}")
            print()
            print(f"⚕️  ACTION    : {why['action']}")
        else:
            print(f"🔬 Interaction detected.")
            print(f"   Detailed Kāraka reasoning not yet in database.")
            print(f"   Confidence : MEDIUM")
            print(f"⚕️  ACTION    : Verify with pharmacist before dispensing")
    else:
        print(f"✅ STATUS    : No interaction detected")
        print(f"   Confidence : MEDIUM — always verify with pharmacist")

    print("=" * 55)
    print()

# ─────────────────────────────────────────
# USER INPUT — THE PRODUCT
# ─────────────────────────────────────────

def main():
    print()
    print("=" * 55)
    print("   🛡️  SUTRARX SHIELD — Drug Interaction Checker")
    print("   Powered by NeuroSutra Kāraka Verification")
    print("=" * 55)
    print()

    while True:
        print("Enter two drug names to check for interactions.")
        print("Type 'quit' to exit.")
        print()

        drug_a = input("  Drug 1: ").strip().lower()
        if drug_a == "quit":
            print("Exiting SutraRx Shield. Stay safe.")
            break

        drug_b = input("  Drug 2: ").strip().lower()
        if drug_b == "quit":
            print("Exiting SutraRx Shield. Stay safe.")
            break

        shield_check(drug_a, drug_b)

        another = input("Check another pair? (yes/no): ").strip().lower()
        if another != "yes":
            print()
            print("Thank you for using SutraRx Shield.")
            print("Always consult a medical professional.")
            break
        print()

main()