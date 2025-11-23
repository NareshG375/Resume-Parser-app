import os,json
from dotenv import load_dotenv
import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,TextLoader
from langchain_core.prompts import PromptTemplate


# load env  file 
load_dotenv()
api_key  = os.getenv('GOOGLE_API_KEY')

llm  = ChatGoogleGenerativeAI(model='gemini-2.5-flash',google_api_key = api_key)


PROMPT_TEMPLATE = """     

You are an expert resume parser. Give the resume text,extract the  following fields  and return a valid single json object 



{{
  "Name" :"...",
  "Email":"...",
  "Phone":"...",
  "LinkedIn":"...",
  "Skills":"...",
  "Education":"...",
  "Experience":"...",
  "Projects":"...",
  "Certification":"...",
  "Language":"..."
 
}}

Rules:

- If a filed cannot found, set it values to "No idea"
- Keep Only valid JSON (no extra comuntary)
- Keep lists as arrays, and keep Experience/Projects as arrays of short strings.


Resume Text :

{text}

"""



prompt  = PromptTemplate(template=PROMPT_TEMPLATE,input_variables=["text"])


print(prompt)

 

def  load_resume_docs(uploaded_file):

    temp_path  = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f: 
        f.write(uploaded_file.getbuffer())

    if uploaded_file.name.endswith(".pdf"):
        loader  = PyPDFLoader(temp_path)
    
    elif uploaded_file.name.endswith(".txt"):
        loader  = TextLoader(temp_path)

    elif uploaded_file.name.endswith(".docx"):
        loader  = Docx2txtLoader(temp_path) 
    else:
          return None       
    
    documents =  loader.load()
    return documents



def main():
    
    st.set_page_config(page_title="Resue Parser", page_icon='',layout="centered")
    st.title("Resume Parser")
    uploaded_file  = st.file_uploader("Select file", type=[".pdf",".txt",".docx"])
    if uploaded_file:
        with st.spinner("Loading Text.."):

            print(uploaded_file)
            docs = load_resume_docs(uploaded_file)

            print(docs)

            if not docs:
                st.error("Unsupported File  tye")
                return 
            
        st.subheader("Preview text ")
        full_text = "\n\n".join([d.page_content for d in docs])
        preview_text = full_text[:4000]
        st.text_area("Preview", value=preview_text, height=200)

        if st.button("Ask LLM"):
            with st.spinner("Sending to LLM..."):
                full_text = "\n\n".join([d.page_content for d in docs]) 
                formatted_prompt = prompt.format(text=full_text) 

                print("formatted prompt", formatted_prompt)
                try:
                    response = llm.invoke(formatted_prompt)

                    if hasattr(response,'content'):
                       response_str  = response.content

                    else:
                        response_str = response

                    # Clean up response_str if needed (e.g., remove ```json fences)

                    cleaned = response_str.strip()
                    if cleaned.startswith("```"):
                        cleaned = cleaned.lstrip("```json").lstrip("```").strip()
                        last_brace = cleaned.rfind('}')
                        if last_brace != -1:
                            cleaned = cleaned[:last_brace+1]
                        parsed = json.loads(cleaned)
                        st.subheader("Parsed JSON – formatted")
                        st.code(parsed, language="json")

                except json.JSONDecodeError as jde:
                        st.error(f"JSON parse failed: {jde}")
                        st.stop()
                except Exception as e:
                        st.error(f"LLM invocation failed: {e}")
                        st.stop()

           



if  __name__ =='__main__':
    main()