# Formatter

Clean and format your meeting notes in one click, optionally using templates.
Uses the OpenAI API for the behind-the-scene magic. Get your key [here](https://platform.openai.com/api-keys).

## Get started

1. Clone the repo or download the zip file.

2. Install the dependencies with

```python
pip install openai streamlit
```

3. Open the terminal in the formatter directory and run `streamlit run app.py`

4. If prompted, enter your OpenAI API key, press enter to save and refresh the page.

That's it, you are now ready to go, enjoy!

## Modes

Formatter has 3 modes of operation:
- **Clean**: The most basic mode, it just instructs the LLM to fix typos and grammatical mistakes. It will also try to un-abbreviate some words if it can.
- **Format**: The star of the show, it instructs the LLM to format your notes according to a template you have created. See below for an example.
- **Summarize**: Just as the name implies, it instructs the LLM to summarize the given text. No particular formatting is applied here.

The system prompts are in the `app.py` main file if you'd like to tweak or extend them.

## Setup the templates

Formatter really shines once you've got your templates set up. You'll need to select the "Format" mode selector to use them.
Templates are just markdown files (`.md`) where you create a skeleton of what your final note will look like.

Typically, you will use markdown headings that the LLM will follow to structure your notes. I also strongly suggest to explain the contents of the subheading between brackets. Here's an example for a barebones note organizer:

```markdown
# Stakeholders
[Who are the stakeholders?]

# Context
[What is the context of the meeting? What is the project being discussed? Put all the miscellaneous information here.]

# Next Steps
[What are the next steps? Assign them to a shareholder if possible.]
```

That is a basic example but it should give you a decent idea of what a template should look like. Since the LLM reads your template, then tries to format your notes according to the template, your imagination is the limit here.