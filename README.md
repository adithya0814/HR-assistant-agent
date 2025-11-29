# 🤖 HR Assistant Agent

## 1. Overview

The **HR Assistant Agent** is an AI-powered chat application that helps employees get instant answers to common HR-related questions such as:

- Leave policy  
- Working hours  
- Holidays  
- Probation and confirmation  
- Notice period  
- Basic benefits  

Instead of emailing HR and waiting for a response, employees can ask their questions in a simple chat interface and get an answer based on the company’s HR policy document.

---

## 2. Features

- 💬 **Interactive chat UI** built using Streamlit  
- 📄 Uses a fixed HR policy file: `hr_policies.txt`  
- 🤖 Uses an OpenAI GPT model to generate professional answers  
- 🚫 If a question is outside the policy, the bot politely asks the employee to contact HR  
- 🧾 Logs all Q&A interactions to `chat_logs.csv` for future analysis  

---

## 3. Architecture

High-level architecture:

1. **User (Employee)**  
   - Opens the Streamlit web app in a browser  
   - Types a question related to HR policies  

2. **Streamlit App (`app.py`)**  
   - Receives the question  
   - Loads `hr_policies.txt`  
   - Constructs a system prompt and conversation history  

3. **OpenAI GPT Model**  
   - Takes the system prompt + chat history + latest question  
   - Generates a professional answer based only on the given policies  

4. **Streamlit App**  
   - Displays the answer back to the user  
   - Saves the question and answer into `chat_logs.csv` with timestamp  

5. **Storage**  
   - `hr_policies.txt` → HR policy knowledge base  
   - `chat_logs.csv` → Simple analytics / log store  

You can draw this as a block diagram for `architecture.png` with arrows:
**User → Streamlit UI → OpenAI GPT → Streamlit UI → User**, and a side box for **CSV Logs**.

---

## 4. Tech Stack

- **Language:** Python  
- **Frontend / UI:** Streamlit  
- **LLM Provider:** OpenAI GPT model (e.g., `gpt-4.1-mini`)  
- **Config / Secrets:** `.env` using `python-dotenv`  
- **Logging / Storage:** CSV file using `pandas`  

---

## 5. Project Structure

```text
hr-assistant-agent/
├─ app.py               # Main Streamlit application
├─ hr_policies.txt      # HR policy document used as knowledge base
├─ requirements.txt     # Python dependencies
├─ README.md            # Project documentation
└─ .env.example         # Example environment variable file (API key)
