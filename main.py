import asyncio
import logging

from fastapi.middleware.cors import CORSMiddleware

from models.index import ChatMessage
from providers.together import query_rag, generate_dialog_header

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from utils.index import get_finished_headless_dialogs, prepend_to_file

logger = logging.getLogger("uvicorn")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def timer():
    """
    Periodically scans for completed headless dialog logs, generates headers, and prepends them to the files.

    Every 30 minutes:
      - Finds markdown logs that haven't been modified in the last 24 hours.
      - For each log:
        - Generates a Markdown-formatted header via LLM.
        - Prepends the header to the file.
        - Logs each action.

    :raises Exception: If file access or header generation fails.
    """
    logger.info("Run dialog handler")
    while True:
        finished_headless_logs = get_finished_headless_dialogs()
        logger.info(f"Found {finished_headless_logs} logs to be managed")
        for log_file in finished_headless_logs:
            header = await generate_dialog_header(log_file)
            prepend_to_file(log_file, header.content)
            logger.info(f"Header was added to the {log_file}")

        await asyncio.sleep(60 * 30)  # 30 min delay


app.mount("/public", StaticFiles(directory="public"), name="public")


@app.get("/")
async def read_root():
    # result = model.invoke(input="Hello World")
    return {"Hello": "world"}


@app.post("/chat/{chat_id}")
async def ask(chat_id: str, message: ChatMessage):
    return {"response": await query_rag(message, chat_id)}


asyncio.ensure_future(timer())
