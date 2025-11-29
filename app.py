import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# ========== BACKEND CONFIGURATION ==========
# 1. Define the Model Name here (User cannot see this)
# Options: "gemini-1.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-pro"
BACKEND_MODEL_NAME = "gemini-2.5-flash"

# 2. Retrieve API Key from Secrets or Environment Variables
API_KEY = "AIzaSyCa-nFtq37AtNbPtlnzVTk-rrDkxfzStUY"

# ========== STREAMLIT PAGE CONFIG ==========
st.set_page_config(page_title="HR Assistant", page_icon="💼")
st.title("💼 HR Assistant - Sample IT Solutions")
st.caption("Ask me about leaves, policies, and benefits.")

# ========== SIDEBAR (CLEANED UP) ==========
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=100)
    st.markdown("### Employee Helpdesk")
    st.markdown("This assistant is connected to the official **HR Policy Document (2025)**.")
    
    st.divider()
    
    # Only "Clear History" remains visible to the user
    if st.button("Start New Conversation"):
        st.session_state.langchain_messages = []
        st.rerun()

# ========== SYSTEM INSTRUCTIONS (CONTEXT) ==========
# ========== SYSTEM INSTRUCTIONS (CONTEXT) ==========
SYSTEM_CONTEXT = """
You are "Sam," the HR Assistant for 'Sample IT Solutions Pvt. Ltd.'.

### **STRICT RESPONSE GUIDELINES:**
1.  **Brevity is Key:** Your answers must be **extremely concise (1-2 sentences maximum)**.
2.  **Source of Truth:** Answer ONLY based on the "HR POLICY & SCOPE" below.
3.  **Unknowns:** If a topic is not listed below, say: "Please contact HR directly at hr@sampleitsolutions.com."
4.  **Tone:** Professional, direct, and helpful.

---

### **HR POLICY & SCOPE DOCUMENT**

#### **1. Holidays & Calendar**
* **Public Holidays:** The company observes 10 paid public holidays per year (e.g., Independence Day, Diwali, Christmas).
* **Current Month Status:** For specific dates in the current month, please refer to the "Holiday Calendar 2025" PDF on the intranet portal.
* **Optional Holidays:** Employees can choose 2 additional "Restricted Holidays" (RH) from the approved list.

#### **2. Employment Policy & Types**
* **Probation:** All new joiners serve a 6-month probation period. Confirmation depends on performance review.
* **Notice Period:** * **During Probation:** 15 Days.
    * **Confirmed Employees:** 60 Days (2 Months).
* **Employment Types:** Full-time (40 hours/week) and Contractual (as per project duration).

#### **3. Recruitment & Onboarding**
* **Hiring:** HR handles job postings, screening, interviews, and background checks.
* **Onboarding:** New employees must submit educational certificates, ID proofs, and previous employment letters.

#### **4. Compensation, Payroll & Benefits**
* **Salary Cycle:** Salaries are credited on the last working day of the month.
* **Tax:** HR issues Form 16 annually. Investment proofs must be submitted by Jan 20th.
* **Insurance:** Health insurance covers Employee + Spouse + 2 Children + Parents (Sum insured: ₹5L).

#### **5. Working Hours, Attendance & Shifts**
* **Timings:** 9:30 AM to 6:30 PM (Mon-Fri). Grace time up to 9:45 AM.
* **Work Mode:** Hybrid (3 days office / 2 days WFH).

#### **6. Leave Policy (Jan - Dec)**
* **Allowances:** 12 Casual Leaves (CL), 12 Sick Leaves (SL), 15 Earned Leaves (EL).
* **Maternity/Paternity:** 26 weeks (Maternity) / 10 days (Paternity).
* **LWP:** Uninformed absence > 2 days is treated as Leave Without Pay.

#### **7. Separation (Exit Policy)**
* **Resignation:** Must be submitted via the HR Portal.
* **Settlement (FnF):** Processed within 45 days of the last working day.

#### **8. Culture & Employee Relations**
* **POSH:** Zero-tolerance policy for harassment. Complaints go to the Internal Committee.
* **Dress Code:** Smart casuals (Mon-Thu), Jeans/T-shirts (Fri).
"""

# ========== LANGCHAIN LOGIC ==========

# 1. Check if Key Exists
if not API_KEY:
    st.error("⚠️ Server Error: API Key not found. Please contact the administrator to configure 'GEMINI_API_KEY' in secrets.")
    st.stop()

# 2. Setup Memory
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("Hello! I am Sam. How can I assist you with HR policies today?")

# 3. Define Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_CONTEXT),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ]
)

# 4. Initialize Chain
try:
    llm = ChatGoogleGenerativeAI(
        model=BACKEND_MODEL_NAME,
        google_api_key=API_KEY,
        temperature=0.3,
        convert_system_message_to_human=True
    )
    
    chain = prompt | llm
    
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: msgs,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

except Exception as e:
    st.error(f"Internal configuration error: {e}")
    st.stop()

# 5. Render Chat UI
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# 6. Handle Input
if user_input := st.chat_input("Type your question here..."):
    st.chat_message("human").write(user_input)

    with st.chat_message("ai"):
        with st.spinner("Thinking..."):
            try:
                config = {"configurable": {"session_id": "any"}}
                response = chain_with_history.invoke({"input": user_input}, config)
                st.write(response.content)
            except Exception as e:
                st.error(f"An error occurred: {e}")