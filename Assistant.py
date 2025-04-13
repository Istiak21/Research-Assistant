import os
import time
import streamlit as st
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from together import Together
from langchain_core.language_models import BaseLLM
from langchain_core.outputs import LLMResult, Generation
from typing import Any, List, Optional

# Load environment variables
load_dotenv()

# Set up Streamlit page
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state variables
if 'research_started' not in st.session_state:
    st.session_state.research_started = False
    st.session_state.research_complete = False
    st.session_state.questions = []
    st.session_state.findings = []
    st.session_state.report = ""

# Initialize Together AI client
@st.cache_resource
def init_client():
    return Together(api_key=os.getenv("TOGETHER_API_KEY"))

client = init_client()

class TogetherAILLM(BaseLLM):
    model: str = "meta-llama/Llama-3-8b-chat-hf"
    temperature: float = 0.7
    max_tokens: int = 2048
    
    def _generate(self, prompts: List[str], **kwargs) -> LLMResult:
        generations = []
        for prompt in prompts:
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                **kwargs
            )
            generations.append([Generation(text=response.choices[0].message.content)])
        return LLMResult(generations=generations)
    
    def _llm_type(self) -> str:
        return "together_ai"

@st.cache_resource
def load_llm():
    return TogetherAILLM()

llm = load_llm()

@st.cache_resource
def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def chrome_research(query: str, max_results: int = 3) -> str:
    driver = get_chrome_driver()
    try:
        driver.get(f"https://www.google.com/search?q={query}")
        time.sleep(2)
        results = []
        links = driver.find_elements(By.CSS_SELECTOR, "div.g a")[:max_results]
        
        for i, link in enumerate(links):
            href = link.get_attribute("href")
            if href and href.startswith("http"):
                driver.execute_script(f"window.open('{href}');")
                driver.switch_to.window(driver.window_handles[i+1])
                time.sleep(2)
                try:
                    visible_text = driver.find_element(By.TAG_NAME, "body").text
                    results.append(visible_text[:5000])
                except Exception as e:
                    st.warning(f"Error extracting text: {str(e)}")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        
        return "\n\n".join(results)
    except Exception as e:
        st.error(f"Research error: {str(e)}")
        return f"Research failed: {str(e)}"

def run_research(topic: str):
    st.session_state.research_started = True
    st.session_state.research_complete = False
    
    with st.status("Starting research...", expanded=True) as status:
        st.write("Generating research questions...")
        questions = llm.generate([f"Generate 3 specific research questions about {topic}"]).generations[0][0].text
        st.session_state.questions = [q.strip() for q in questions.split("\n") if q.strip()][:3]
        
        st.write("Researching each question...")
        findings = []
        for i, question in enumerate(st.session_state.questions):
            st.write(f"Researching: {question}")
            research = chrome_research(question)
            findings.append(research)
            st.write(f"Completed {i+1}/{len(st.session_state.questions)}")
        st.session_state.findings = findings
        
        st.write("Compiling final report...")
        report = llm.generate([
            f"Summarize these findings about {topic}:\n{'\n'.join(findings)}\n\n"
            "Provide a well-structured report with key points."
        ]).generations[0][0].text
        st.session_state.report = report
        
        status.update(label="Research complete!", state="complete")
        st.session_state.research_complete = True

# UI Components
st.title("🔍 AI Research Assistant")
st.write("Enter a topic below to generate a research report")

topic = st.text_input("Research topic", placeholder="e.g., 'Latest advancements in renewable energy'")

if st.button("Start Research") and topic:
    run_research(topic)

if st.session_state.research_started:
    if st.session_state.research_complete:
        st.subheader("Research Questions")
        for i, question in enumerate(st.session_state.questions, 1):
            st.write(f"{i}. {question}")
        
        st.subheader("Final Report")
        st.write(st.session_state.report)
        
        if st.button("New Research"):
            st.session_state.research_started = False
            st.session_state.research_complete = False
            st.session_state.questions = []
            st.session_state.findings = []
            st.session_state.report = ""
            st.rerun()
    else:
        st.write("Research in progress...")
        st.spinner()
