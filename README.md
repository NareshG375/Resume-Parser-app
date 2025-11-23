AI Resume Parser App (LangChain + Google Gemini)

This project is an AI-powered Resume Parser built using LangChain and Google Gemini models.
It extracts structured information from resumes (PDF, DOCX, text) and outputs clean, machine-readable JSON data.

The app is ideal for:

    1.HR / Recruitment automation

    2.Job portals

    3. ATS systems

    4. Resume analysis tools

🚀 Features

✔ Upload resume (PDF / DOCX / TXT)
✔ Extract structured data (Skills, Education, Experience, Projects, Summary, Contact info)
✔ Uses LangChain + Google Gemini LLM
✔ Customizable extraction prompts
✔ Clean JSON output
✔ REST API support
✔ Frontend UI (React/HTML optional)
✔ Error handling for corrupted files
✔ Ready for deployment on Render, Vercel, AWS, etc.


🧠 Tech Stack
 
LLM   :- Google Gemini
AI Framework:-LangChain
Backend:- 	Python 
Frontend:-  Streamlit


⚙️ Installation

1️⃣ Clone the repo

https://github.com/NareshG375/Resume-Parser-app.git


cd Resume-Parser-ap

2️⃣ Install dependencies

pip install -r requirements.txt

3️⃣ Add Google Gemini API Key


   Create .env file

   GEMINI_API_KEY = "YOUR_API_KEY"

▶️ Run the Backend 

    streamlit run app.py
