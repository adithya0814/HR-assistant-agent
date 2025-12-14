# HR Assistant

## Project Overview
This project is an AI-powered HR Assistant designed to answer employee questions based on a company's internal HR policies. It uses a Large Language Model (LLM) from Google (Gemini) to understand and respond to queries in a conversational manner. The assistant is built with Python and uses Streamlit for the user interface, making it easy to create an interactive web-based application.

The core of the application is a predefined set of HR policies and guidelines that act as the primary source of truth for the AI. This ensures that the assistant provides accurate and consistent information to employees.



## Steps to Run the Code
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd hr-assistant-agent
   ```
2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your environment variables:**
   - Create a `.env` file in the root directory.
   - Add your Gemini API key to the `.env` file:
     ```
     GEMINI_API_KEY="your-api-key"
     ```
4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Environment Setup
- **Python:** This project requires Python 3.8 or higher.
- **Virtual Environment:** It is recommended to use a virtual environment to manage project dependencies.
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  ```
- **Dependencies:** The required Python libraries are listed in the `requirements.txt` file.

## Libraries Used
- **streamlit:** For creating the web application and user interface.
- **langchain-google-genai:** For interacting with the Google Gemini LLM.
- **langchain-core:** Provides the core abstractions for building language model applications.
- **langchain-community:** For community-contributed components, including the chat message history.
- **python-dotenv:** For managing environment variables.

## Sample Data Explanation
This project does not require any specific sample data to run. The HR policies and rules are hardcoded in the `app.py` file within the `SYSTEM_CONTEXT` variable. This context provides the AI with the necessary information to answer employee questions.

If you wish to extend the project, you can place relevant data files (e.g., CSVs with employee information, additional policy documents) in the `data` directory. You would then need to modify the application to read and process this data.