import spacy

nlp = spacy.load("en_core_web_sm")

def parse_sentence(sentence):
    doc = nlp(sentence)
    
    print(f"Sentence: {sentence}")
    print("=" * 50)
    
    for token in doc:
        print(f"  Word: {token.text:15} Role: {token.dep_:15} Head: {token.head.text}")
    
    print()

# Test with real drug interaction sentences
parse_sentence("Warfarin increases bleeding risk when combined with aspirin.")
parse_sentence("Ibuprofen inhibits the metabolism of warfarin.")
parse_sentence("Aspirin reduces platelet aggregation in the blood.")