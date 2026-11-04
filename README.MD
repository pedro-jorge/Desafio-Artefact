
# Empório da Música Chatbot - Artefact Challenge

This repository contains the implementation of a text-message agent for the fictional store Empório da Música. The agent receives a document with information about the store and has access to a tool for querying a SQLite database of transaction data.

## Prerequisites

- [Python]([www.python.org/downloads](https://www.python.org/downloads/)) 3.14 or higher;
- [Poetry](https://python-poetry.org/docs/#installation) 2.x;
- [Ollama](https://ollama.com) 0.40.14 or higher.

## Environment setup

### 1. Clone the repository

```powershell
git clone https://github.com/pedro-jorge/Desafio-Artefact.git
```

```powershell
cd Desafio-Artefact
```

### 2. Install dependencies

```powershell
poetry install
```

### 3. Run Ollama and Qwen3

```powershell
ollama serve
```

```powershell
ollama run qwen3:8b
```

### 4. Run the app

```powershell
poetry run streamlit run app.py
```

A window with the Streamlit interface will open in your browser.

## Response flow

1. The agent receives, via the prompt, the full documentation about the store and the database schema.
2. If the question requires database access, the agent can run read-only queries to retrieve the necessary information. Otherwise, it answers based solely on the documentation.

## Repository Structure

.
├── app.py                      # Application entry point (Streamlit interface)
├── poetry.lock                 # Dependency lock file
├── pyproject.toml              # Dependencies, metadata, and Poetry configuration
├── data/                       # Folder with the store document, the original CSV data, and the SQLite DB
│   ├── database.db             # Local database (SQLite) queried by the tools
│   ├── desafio_tecnico_ai_*.csv # Source spreadsheets (loaded into the database)
│   └── políticas_da_loja.pdf   # Document with the store policies
├── examples/                   # Example conversations
│   ├── example1_part1.png      # Example 1 (part 1 of 3)
│   ├── example1_part2.png      # Example 1 (part 2 of 3)
│   ├── example1_part3.png      # Example 1 (part 3 of 3)
│   ├── example2.png            # Example 2
│   ├── example3.png            # Example 3
│   └── example4.png            # Example 4
└── src/                        # Application modules
    ├── agent.py                # Agent/LLM definition
    ├── config.py               # Loading of settings, environment variables, and prompt
    ├── prompt.txt              # System prompt
    └── tools.py                # Agent tools (database queries, store document retrieval)


## Technical decisions

| Component                                  | Decision                                               | Rationale                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------ | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Agent approach**                   | Tool calling, with information provided via the prompt | Since the document with the store's information is small and simple (a plain 8-page PDF), it makes sense to process it with LangChain (PyMuPDF) and pass it inside the prompt to the model. The SQLite database schema is also provided, along with a read-only query tool, so the agent can run SQL commands and retrieve any data it needs. |
| **Model and provider**               | Qwen3 8B via Ollama                                    | Without access to a paid API model, such as OpenAI's, and given the usage limits of free models, the decision was to run Qwen3 with 8 billion parameters locally.                                                                                                                                                                             |
| **User interface**                   | Streamlit                                              | Basic user interface for better interaction.                                                                                                                                                                                                                                                                                                  |
| **Conversation history persistence** | No history                                             | Since the model runs locally, the decision was not to keep history, so that the prompt remains complete, can include the document's information, and any SQL queries are not affected.                                                                                                                                                        |
| **Data handling**                    | Conversion to SQLite3                                  | To make it easier for the model to access the data, the CSV tables were converted into a relational database, so that the model can have the schema (via the prompt) and run efficient queries to retrieve the data.                                                                                                                          |

## Known limitations

- **Response time**: because the model runs locally, the chatbot's response time depends directly on the computing power of the machine, although it stays under the five-minute limit recommended by the store's guideline. The implementation was developed on an Apple M4 (8-core integrated GPU) with 16 GB of unified memory (shared between CPU and GPU) and was also tested on a desktop with an AMD Radeon RX 9060 XT with 16 GB. The ideal solution would depend on the available budget and infrastructure: a better adaptation of Qwen3, if the goal were to run on a dedicated machine or on a server on AWS or similar, or the use of an API such as OpenAI's. Both approaches would improve response time.
- **Strategy for handling the store document**: since there is a single document, and it is simple and small, it is feasible to pass it as context to the model inside the prompt. If there were more documents and/or larger documents, we would have to use Retrieval Augmented Generation (RAG) to process them. The decision not to use this approach came down to simplicity and feasibility. RAG would require a greater effort to tune its associated hyperparameters: how to split the chunks, the ideal value of K for retrieval, whether to retrieve context for every question or let the model decide, etc. For a project with a larger scope and timeline, using RAG and running these associated tests would be essential.
- **Model size and use of reasoning** : due to hardware limitations, the model used has only 8 billion parameters, which also limits the quality of its answers. Although Qwen3 has a reasoning parameter, a deeper investigation of Chain of Thought, together with a more robust model (with more parameters, or commercial models such as GPT), could lead to better results on more sophisticated questions. There are cases in which the current model gets confused and fails to apply business rules reasonably (such as applying promotions or cross-referencing data from partial information).
- **Security**: since the interface has no user accounts, the model is free to access and report all the data available in the database. In a scenario where access must be restricted, with a real user who may see only the data related to their own account, a more sophisticated implementation would be necessary. In that case, it would be very risky to rely on the model alone for this security layer, so a restriction should be enforced in code.

## Use of generative AI

Generative AI tools (Claude, ChatGPT, and Gemini) were used in solving this challenge to help develop code functions, set up the environment (Poetry, reproducibility), and suggest possible improvements to the system architecture.
