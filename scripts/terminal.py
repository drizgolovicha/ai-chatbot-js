# ANSI escape codes for colors
import os
import sys
import asyncio
import utils.index as utils
from dotenv import load_dotenv

load_dotenv()  # noqa: E402

from models.index import ChatMessage
from providers.rag_agent import AIAgent
from providers.providers import LMStudioProvider, TogetherProvider


async def run():
    # model = LMStudioProvider(host=os.environ.get('LM_STUDIO_HOST'), model_name="qwen/qwen3-8b")
    # free_model = LMStudioProvider(host=os.environ.get('LM_STUDIO_HOST'), model_name="qwen/qwen3-8b", temperature=0.5)
    model = TogetherProvider(model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free")
    free_model = TogetherProvider(model_name="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", temperature=0.5)

    llm = AIAgent(model=model, free_model=free_model)

    while True:
        user_input = input(utils.YELLOW + "Ask a query about your documents (or type 'quit' to exit): " + utils.RESET_COLOR)
        if user_input.lower() == 'quit':
            break
        elif len(user_input) < 1:
            continue

        response = await llm.query(ChatMessage(question=user_input))
        print(utils.NEON_GREEN + "Response: \n\n" + response + utils.RESET_COLOR)


if __name__ == "__main__":
    asyncio.run(run())
