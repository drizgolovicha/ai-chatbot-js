# README.md

## Overview

This project implements a personal AI assistant leveraging a Retrieval-Augmented Generation (RAG) system with a UI developed in pure JavaScript. The assistant is designed to replicate all steps that a user might perform themselves, offering a robust guide for building a similar bot. The UI can be seamlessly injected into any website by referencing the JavaScript link, ensuring ease of integration.

---

## Key Features
- **Fully Configurable RAG-Based AI Assistant:** The assistant uses a RAG system to provide precise, context-aware responses.
- **UI Built with Pure JavaScript:** Easily embed the assistant into any website using a simple JS link.
- **Local and Remote AI Provider Support:** Supports local LLMs like Llama or external providers for faster, scalable processing.
- **End-to-End Guide:** Comprehensive setup instructions covering data preparation, vector database creation, and API deployment.

---

## Setting Up the Project

Follow these steps to set up and run the project locally:

### 1. Create a Virtual Environment
To isolate project dependencies, create a virtual environment using Python:

```bash
python3 -m venv env
```

### 2. Activate the Virtual Environment
Activate the virtual environment:

- **Windows:**
  ```bash
  .\env\Scripts\activate
  ```

- **macOS/Linux:**
  ```bash
  source env/bin/activate
  ```

### 3. Install Dependencies
Install the required dependencies listed in `requirements.txt`:

```bash
pip3 install -r requirements.txt
```

### 4. Llama LLM Preparation (For Local Integration)
1. Download and install OLLAMA from [here](https://ollama.com/download).
2. Pull a Llama LLM locally, e.g., [Llama 3.2](https://ollama.com/library/llama3.2):
   ```bash
   ollama run llama3.2
   ```
3. For embeddings, install the `mxbai-embed-large` network:
   ```bash
   ollama pull mxbai-embed-large
   ```

#### 4.1 Data Preparation
Prepare your assistant with knowledge about your company or service:
1. Update `data/links.txt` with the web links to scrape data from, one URL per line. Example:
   ```
   https://www.microsoft.com/en-us/about
   https://news.microsoft.com/facts-about-microsoft/
   https://news.microsoft.com/source/
   ```
2. Run the `scrapper.py` script to parse and save data in markdown format:
   ```bash
   python3 scrapper.py
   ```

#### 4.2 Data Ingestion
To store the parsed data in a vector database:
1. Use ChromaDB, which works efficiently with SQLite.
2. Run the `ingest.py` script to populate the database:
   ```bash
   python3 ingest.py
   ```

Once completed, the assistant is ready for use.

### 5. Run the API
Start the API server using FastAPI:
```bash
fastapi run
```

### 5.1 Setting Up Automated Source Synchronization (Optional)
To keep your knowledge base automatically updated with the latest content from your sources, you can set up a cron job to run the source synchronization script periodically.

1. **Make the script executable:**
   ```bash
   chmod +x scripts/source_sync.py
   ```

2. **Test the synchronization script:**
   ```bash
   python3 scripts/source_sync.py
   ```

3. **Set up a cron job** to run the synchronization automatically:
   ```bash
   crontab -e
   ```

4. **Add the following line** to run synchronization every hour (adjust the schedule as needed):
   ```bash
   0 * * * * cd /path/to/your/ai-chatbot-js && /path/to/your/env/bin/python scripts/source_sync.py >> logs/sync.log 2>&1
   ```

   **Alternative schedules:**
   - Every 6 hours: `0 */6 * * *`
   - Daily at 2 AM: `0 2 * * *`
   - Every 30 minutes: `*/30 * * * *`

5. **Create logs directory** (if it doesn't exist):
   ```bash
   mkdir -p logs
   ```

**Note:** Replace `/path/to/your/ai-chatbot-js` and `/path/to/your/env/bin/python` with your actual project path and Python virtual environment path.

### 5.2 Switching Between Providers
The project supports multiple providers for processing AI queries:

1. **Default Local Llama Provider:**
   Ensure the local Llama network is running as described in Step 4.

2. **Alternative Provider - Together.ai:**
  - Register at [Together.ai](https://www.together.ai/).
  - Obtain your API key.
  - Create a `.env` file with the following content:
    ```
    USER_AGENT="MyBot/1.0 (+https://mydomain.com/info)"
    TOGETHER_API_KEY="<YOUR KEY>"
    CHROMA_DIR="<YOUR_DIR>"
    ```
  - Update `main.py` to switch the provider:
    ```python
    from providers.ollama import query_rag
    ```
    Change to:
    ```python
    from providers.together import query_rag
    ```
  - Restart the service to apply changes.

### 6. Verify the Setup
Open the browser and navigate to [http://127.0.0.1:8000/public/chat.html](http://127.0.0.1:8000/public/chat.html). Test the bot's functionality and start interacting with your assistant.
As an alternative you can open [http://127.0.0.1:8000/public/iframe.html](http://127.0.0.1:8000/public/iframe.html) to see how it can be ingested on you custom page.

---

## Final
Let me know you have any questions

---

## License
This project is licensed under the [MIT License](LICENSE).

---

### Notes
- For optimal results, ensure the AI is trained on relevant and up-to-date data.
- The project is designed for flexibility, enabling integration with various providers and customization of the RAG pipeline.

