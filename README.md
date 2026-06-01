# SutraRx Shield

**Neuro-symbolic drug interaction checker powered by Pāṇinian Kāraka grammar verification.**

Built by Sarvesh Doiphode | BCA 2nd Year | MIT-ADT University, Pune

---

## What is SutraRx?

SutraRx is the first pharmaceutical AI application built on NeuroSutra — a neuro-symbolic framework that combines LLM fluency with Pāṇini's Kāraka grammar as a formal verification layer.

Most drug interaction checkers tell you WHAT is dangerous.  
SutraRx tells you WHY — using Kāraka role mapping.

---

## SutraRx Shield — Drug Interaction Checker

Shield is the first product. Built for pharmacists and medical shop owners in India.

**How it works:**
1. Pharmacist enters two drug names
2. Shield fetches live FDA data
3. Kāraka parser extracts agent-action-object roles
4. Verification gate checks for pathway conflicts
5. Output: FLAGGED or SAFE + full explanation

---

## Example Output
🛡️  SUTRARX SHIELD
Checking: WARFARIN + ASPIRIN
⚠️  STATUS   : FLAGGED
📋 DETECTED : Category Match
📄 EVIDENCE : Both are: blood thinner
🔬 WHY THIS IS DANGEROUS:
Mechanism  : Both inhibit clotting through different pathways
Kāraka Logic:
Warfarin (Kartā) blocks Vitamin K clotting factors (Karma).
Aspirin (Kartā) inhibits platelet aggregation (Karma).
Combined — dual pathway blockage.
Risk       : Severe bleeding risk — internal hemorrhage possible
Confidence : HIGH
⚕️  ACTION   : Do NOT dispense together without doctor confirmation

---

## Tech Stack

- Python 3.13
- spaCy (NLP parsing)
- OpenFDA API (drug data)
- Pāṇinian Kāraka grammar (verification logic)

---

## Run It

```bash
pip install requests spacy
python -m spacy download en_core_web_sm
python shield.py
```

---

## The Philosophy

Ancient Indian knowledge — Pāṇini's 2500 year old formal grammar system — rebuilt as a verification layer for modern pharmaceutical AI. India not as an adopter of AI but as a contributor of foundational ideas.

---

## Research

Based on the NeuroSutra research paper — 1st prize winner at the 8th International Symposium, MIT-ADT University, Pune.

---

*"We tell you why it works. We tell you why it failed. And when every second counts — we tell you what to do right now."*