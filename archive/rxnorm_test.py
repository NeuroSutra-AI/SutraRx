import requests

def get_interaction_text(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{drug_name}&limit=1"
    response = requests.get(url)
    data = response.json()
    result = data["results"][0]
    return result.get("drug_interactions", ["No interaction data found"])[0]

def check_pair(drug_a, drug_b):
    print(f"🔍 Checking: {drug_a.upper()} + {drug_b.upper()}")
    print("=" * 50)
    
    text_a = get_interaction_text(drug_a)
    text_b = get_interaction_text(drug_b)
    
    # Does drug A mention drug B?
    a_mentions_b = drug_b.lower() in text_a.lower()
    # Does drug B mention drug A?
    b_mentions_a = drug_a.lower() in text_b.lower()
    
    if a_mentions_b or b_mentions_a:
        print(f"⚠️  DANGER: These two drugs interact!")
        if a_mentions_b:
            print(f"   → {drug_a} warns about {drug_b}")
        if b_mentions_a:
            print(f"   → {drug_b} warns about {drug_a}")
    else:
        print(f"✅ No direct interaction detected")
    
    print()

# Test 3 pairs
check_pair("warfarin", "aspirin")
check_pair("warfarin", "ibuprofen")
check_pair("aspirin", "ibuprofen")