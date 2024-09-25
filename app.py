import streamlit as st
from openai import OpenAI
import pyclip
import os

st.set_page_config(page_title="Formatter", page_icon="🧠", layout="wide")

st.title("Formatter")

try:
    api_key = os.environ["OPENAI_API_KEY"]
except KeyError:
    st.error("OpenAI API key not found. Please enter your key below, press Enter and refresh the page. Your key will be stored on your system.")
    os_key = st.text_input("API Key", type="password")
    if os_key:
        os.environ["OPENAI_API_KEY"] = os_key
    st.stop()

client = OpenAI(api_key=api_key)

st.write('Welcome to Formatter. Use GPT-4o to format your notes. Upload your text or file and select a template to get started.')

mode = st.radio("Mode", ["Clean", "Format", "Summarize"], horizontal=True)


if mode == 'Format':
    templates = os.listdir("templates")
    templates = [t for t in templates if t.endswith(".md")]
    templates = [t.replace(".md", "").capitalize() for t in templates]
    if len(templates) == 0:
        templates = None
        st.error("No templates found in the templates/ folder. Please refer to the README and add some templates to get started.")
        st.stop()
    elif len(templates) <= 5:
        temp_list = [t.replace(".md", "").capitalize() for t in templates]
        template = st.radio('Template', temp_list, horizontal=True, help="Edit your templates in the templates/ folder. See the README for more information.")
    else:
        template = st.selectbox("Template", templates, help="Edit your templates in the templates/ folder. See the README for more information.")

    if template:
        template_content = open(f"templates/{template.lower()}.md").read()


file = st.file_uploader("Upload a file", type=["txt", "md"], help="Upload a text or markdown file")

if file:
    text = file.getvalue().decode("utf-8")
else:
    st.write("Or")
    text = st.text_area("Enter your text here")



# Instructions
if mode == 'Clean':
    clean_instructions = """
    You are a note-taking assistant. Your task is to clean the text of any typos, error or grammatical mistakes. You MUST NOT format the text suing markdown or anything else. You must strive to keep the text as close to the original as possible. You are not allowed to add or remove any information from the text. Keep the words in their written language. The text can be in French, English or a mix of both. Here is the text you need to clean:
    \n
    """

elif mode == 'Format':
    format_instructions = f"""
    You are a note-taking assistant. Your task is to clean the text of any typos, error or grammatical mistakes and format the text according to the given template. You may use the markdown syntax to format the text. You are not allowed to add or remove any information from the text. Keep the words in their written language. The text can be in French, English or a mix of both. Keep your response in the text's primary language.
    Here the template you need to use:
    {template_content}

    Here is the text you need to format:
    """

else:
    summarize_instructions = """
    You are a note-taking assistant. Your task is to summarize the text. You are not allowed to add or remove any information from the text. Keep the words in their written language. The text can be in French, English or a mix of both. Keep your response in the text's primary language. Here is the text you need to summarize:
    """


def send_payload(text):
    instructions = clean_instructions if mode == 'Clean' else format_instructions if mode == 'Format' else summarize_instructions

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": text}
        ]
    )

    return response.choices[0].message.content


if text:
    btn = st.button("Process")

    if btn:
        with st.spinner("Processing your text, please wait..."):
            output = send_payload(text)
            st.write(output)
            pyclip.copy(output)
            st.toast("Output copied to clipboard!", icon="📋")

