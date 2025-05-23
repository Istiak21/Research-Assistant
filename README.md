# 🔍 AI Research Assistant Building and Deployment

## 📌 Overview

The **AI Research Assistant** is an interactive Streamlit web application that leverages Meta’s `meta-llama/Llama-3-8b-chat-hf` model to help users generate structured research reports on any topic of interest.  

The app performs the following workflow:
1. **Generates three tailored research questions** for the given topic.
2. **Performs web searches on Google** for those questions using a headless Chrome browser.
3. **Extracts relevant content from top search results**.
4. **Summarizes the collected findings into a clean, well-structured research report** using an LLM.

---

## 🚀 Key Features

- AI-generated research questions for any topic.
- Automated web research powered by **Selenium** and **headless Chrome**.
- AI-generated summaries using Meta's Llama 3 model from Together.ai API.
- Clean, interactive web UI built with **Streamlit**.
- Option to reset and run multiple research sessions.

---

## 🛠️ Technologies & Libraries

- Python
- [Streamlit](https://streamlit.io/)
- [Together.ai](https://www.together.ai/)
- [Selenium](https://selenium.dev/)
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager)
- [LangChain](https://python.langchain.com/)
- [dotenv](https://pypi.org/project/python-dotenv/)

---

### 🖥️ Launch the Streamlit App

In your terminal, navigate to the project directory and run:

```bash
streamlit run Assistant.py
```

This will open the AI Research Assistant web interface in your browser.

---

**## 📊 Example Usage**

- Enter a topic like **"Latest advancements in renewable energy"**
- Click **Start Research**
- View AI-generated research questions
- Let the app scrape content from Google results
- Review the automatically summarized research report

---

## 📣 Acknowledgements

[Hugging Face](https://huggingface.co) for hosting the LLM "Llama-3-8b-chat-hf"

[Together.ai](https://together.ai) for providing the LLM API.

[Streamlit](https://streamlit.io) for making app deployment simple.

[Selenium](https://www.selenium.dev) and [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) for browser automation.


