
import os
from dotenv import load_dotenv
load_dotenv()

WEBUI_PORT = int(os.getenv("WEBUI_PORT", 8060))

from pathlib import Path
import tempfile

import gradio as gr

import torch.multiprocessing as mp

MODEL_CACHE_DIR = Path("./models")
MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ["HF_HOME"] = str(MODEL_CACHE_DIR)
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

TEMP_PATH = Path("temp")
TEMP_PATH.mkdir(parents=True, exist_ok=True)

tempfile.tempdir = str(TEMP_PATH)

from echo_studio.gemini_cli import GeminiCLI, GeminiCLIUI

if gr.NO_RELOAD:
    manager = None

def set_manager(manager_local):
    global manager
    manager = manager_local

def get_manager():
    global manager
    return manager

if gr.NO_RELOAD and __name__ == "__main__":
    ctx = mp.get_context("spawn")
    manager = ctx.Manager()
    set_manager(manager)

if not gr.NO_RELOAD:
    manager = get_manager()

gemini_cli = GeminiCLI(manager)

if __name__ != "__mp_main__":
    gemini_cli_ui = GeminiCLIUI(gemini_cli)

    with gr.Blocks() as demo:
        with gr.Tabs():
            with gr.Tab("Gemini CLI") as llm:
                gemini_cli_ui.upload_file_state.render()
                gemini_cli_ui.chatbot.render()
                with gr.Row():
                    with gr.Column(scale=2):
                        gemini_cli_ui.system_prompt_text.render()
                        gemini_cli_ui.prompt_text.render()
                    with gr.Column(scale=1):
                        gemini_cli_ui.file_upload.render()
                    with gr.Column(scale=1):
                        gemini_cli_ui.send_btn.render()

    gemini_cli_ui.reg_events(demo)

if __name__ == "__main__":
    demo.queue()
    demo.launch(
        server_name="127.0.0.1",
        server_port=WEBUI_PORT,
        share=False,
        allowed_paths=[],
        inbrowser=False,
    )