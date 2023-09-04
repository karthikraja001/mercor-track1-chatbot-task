# Linkedin Job Finder Bot - Mercor Hackathon Track1

This is a bot based on on automation of job searching in Linkedin using textbase framework and open-ai api using python. This is the task of Mercor Hackathon track-1 chatbot deployment.

Commands: 
start - the bot starts with the prompt question.

Job Finder
after this, enter the sentence of your job requirements,
eg. Show me jobs based on ML Engineering in chennai.
Recommend me jobs based on SDE1 in coimbatore as entry level or associate level

Company Overview
eg. Tell me about amazon
Give me an overview about google

## Installation
Make sure you have `python version >=3.9.0`, it's always good to follow the [docs](https://docs.textbase.ai/get-started/installation) 👈🏻
### 1. Through pip
```bash
pip install textbase-client
```

### 2. Local installation
Clone the repository and install the dependencies using [Poetry](https://python-poetry.org/) (you might have to [install Poetry](https://python-poetry.org/docs/#installation) first).

For proper details see [here]()

```bash
git clone https://github.com/cofactoryai/textbase
cd textbase
poetry shell
poetry install
```

## Start development server

> If you're using the default template, **remember to set the OpenAI API key** in `main.py`.

Run the following command:
- if installed locally
    ```bash
    poetry run python textbase/textbase_cli.py test
    ```
- if installed through pip
    ```bash
    textbase-client test
    ```
Response:
```bash
Path to the main.py file: examples/openai-bot/main.py # You can create a main.py by yourself and add that path here. NOTE: The path should not be in quotes
```
