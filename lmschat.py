# /// script
# dependencies = [
#   "lmstudio",
#   "typer"
# ]
# ///


import asyncio
import typer
import lmstudio as lms


app = typer.Typer()


@app.command()
def chat_with_lms(
    prompt: str = typer.Argument(..., help="The prompt to send to the LM Studio model")
):
    asyncio.run(_chat_with_lms(prompt))


async def _chat_with_lms(prompt: str):
    async with lms.AsyncClient() as client:
        model = await client.llm.model("openai/gpt-oss-20b")
        result = await model.respond(prompt)

        print(result)


if __name__ == "__main__":
    chat_with_lms("Hello, world!")