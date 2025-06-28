
from pathlib import Path


import gradio as gr

import subprocess
import json
import shutil

INPUT_PATH = Path("inputs")
INPUT_PATH.mkdir(parents=True, exist_ok=True)
UPLOAD_PATH = INPUT_PATH / "upload"
UPLOAD_PATH.mkdir(parents=True, exist_ok=True)

class GeminiCLIUI:
    def __init__(self, gemini_cli):
        self.upload_file_state = gr.State(value=None)
        self.gemini_cli: GeminiCLI = gemini_cli
        
        self.chatbot = gr.Chatbot(value=[], label="ログ", type="messages")
        self.system_prompt_text = gr.TextArea(value="あなたは優秀なAIアシスタントです。回答は日本語で回答してください。", label="システムプロンプト")
        self.prompt_text = gr.TextArea(value="", label="プロンプト")
        self.file_upload = gr.File(label="ファイル", file_count="multiple")

        self.send_btn = gr.Button("送信")

    def reg_events(self, demo: gr.Blocks):
        with demo:
            def on_change_file(files):
                if files is not None:
                    upload_paths = []
                    for file in files:
                        file = Path(file)
                        upload_path = UPLOAD_PATH / file.name
                        shutil.copyfile(str(file), str(upload_path))
                        print("on_change_file", file, upload_path)
                        upload_paths.append(str(upload_path))
                    return upload_paths
                return None

            self.file_upload.change(on_change_file, inputs=[self.file_upload], outputs=[self.upload_file_state])

            def on_click_send(system_prompt, prompt, files, history: list):
                print("on_click_send", prompt, files)
                sp = [{"role": "system", "content": system_prompt}]
                if files is not None:
                    file_prompt = ""
                    for file in files:
                        file_prompt = file_prompt + f"@'{file}' "
                    prompt = f"{file_prompt} {prompt}"
                history.append({"role": "user", "content": prompt})
                yield gr.update(value="", interactive=False), gr.update(value=None), gr.update(value=None), gr.update(value=history)

                stdout, stderr = self.gemini_cli.send_chat(sp + history)
                print("responce", stdout, stderr)
                if stdout != "":
                    history.append({"role": "assistant", "content": stdout})
                if stderr != "":
                    history.append({"role": "assistant", "content": f"<span style=\"color: red\">エラーが発生</span>  \n{stderr}"})
                yield gr.update(interactive=True), gr.update(), gr.update(), gr.update(value=history)

            self.send_btn.click(
                on_click_send,
                inputs=[self.system_prompt_text, self.prompt_text, self.upload_file_state, self.chatbot],
                outputs=[self.prompt_text, self.upload_file_state, self.file_upload, self.chatbot],
            )

class GeminiCLI:
    def __init__(self, manager):
        self.manager = manager

    def send_chat(self, history):
        print("send_chat", history)
        json_data = json.dumps(history, ensure_ascii=False)
        responce = subprocess.run([
            "npx", "gemini.cmd", "-p", json_data
        ], capture_output=True, text=True, encoding="utf-8")
        return responce.stdout.strip(), responce.stderr.strip()