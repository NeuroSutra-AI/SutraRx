import requests
import spacy

nlp = spacy.load("en_core_web_sm")

def get_interaction_text(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{drug_name}&limit=1"
    response = requests.get(url)
    data = response.json()
    result = data["results"][0]
    return result.get("drug_interactions", ["No interaction data found"])[0]

def karaka_analyze(sentence):
    doc = nlp(sentence)
    roles = {}
    for token in doc:
        if token.dep_ == "nsubj":
            roles["Karta  (Agent)  "] = token.text
        elif token.dep_ == "dobj":
            roles["Karma  (Object) "] = token.text
        elif token.dep_ == "pobj":
            roles["Karana (Instr.) "] = token.text
        elif token.dep_ == "ROOT":
            roles["Kriya  (Action) "] = token.text
    return roles

def full_pipeline(drug_name):
    print(f"Drug: {drug_name.upper()}")
    print("=" * 50)
    
    # Step 1: Get FDA text
    text = get_interaction_text(drug_name)
    print(f"FDA Text (first 200 chars):")
    print(f"{text[:200]}")
    print()
    
    # Step 2: Split into sentences and analyze first 3
    sentences = text.split(".")[:3]
    print("Karaka Analysis:")
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 10:
            roles = karaka_analyze(sentence)
            print(f"\n  Sentence: {sentence[:80]}")
            for role, word in roles.items():
                print(f"    {role} → {word}")

    print()
    print("=" * 50)
    print()

# Run the full pipeline
full_pipeline("warfarin")
full_pipeline("ibuprofen")