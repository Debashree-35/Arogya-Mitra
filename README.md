# Arogya Mitra

Multilingual (Odia, Hindi, English) health guidance for rural India.
Pilot: Odisha. Built for Code for a Billion: Bharat Agentic-AI Hackathon 2026.

## Problem
Many rural families find it hard to get quick, understandable health guidance in their own language.

## What it does
- Symptom guidance in English, Odia and Hindi
- Emergency red-flag detection (directs to 108)
- District-wise hospital information

## Status
Early prototype. Guidance is rule-based and not clinically validated.
Not a medical diagnosis tool. In an emergency call 108.

## Run locally
    pip install -r requirements.txt
    streamlit run app.py

## Roadmap
- [ ] Conversational AI agent with tool calling
- [ ] Sourced hospital data for Odisha districts
- [ ] Tested accuracy on a labelled test set
- [ ] Deployment

## License
MIT