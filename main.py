import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import webbrowser
import time
from openai import OpenAI
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

MODEL_ORDER = [
    "gpt-4.1",
    "gpt-4o",
    "gpt-4.1-mini",
    "gpt-4o-mini",
    "o3-mini",
    "gpt-5",
    "gpt-5-thinking"
]

IMAGE_SIZES = {
    "1280x720 (HD)": "1280x720",
    "2560x1440 (2K)": "2560x1440",
    "3840x2160 (4K)": "3840x2160",
    "7680x4320 (8K)": "7680x4320"
}

def syntax_highlight(text_widget, content):
    text_widget.configure(state="normal")
    text_widget.delete("1.0", "end")

    keywords = r"\b(def|return|if|else|elif|for|while|import|from|class|try|except|with|as|lambda|pass|break|continue|yield|async|await)\b"
    strings = r"(\".*?\"|\'.*?\')"
    comments = r"(\#.*?$)"
    numbers = r"\b\d+\b"

    idx = 0
    for line in content.split("\n"):
        text_widget.insert("end", line + "\n")
        line_start = f"{idx + 1}.0"
        line_end = f"{idx + 1}.end"

        for match in re.finditer(keywords, line):
            start = f"{idx + 1}.{match.start()}"
            end = f"{idx + 1}.{match.end()}"
            text_widget.tag_add("keyword", start, end)

        for match in re.finditer(strings, line):
            start = f"{idx + 1}.{match.start()}"
            end = f"{idx + 1}.{match.end()}"
            text_widget.tag_add("string", start, end)

        for match in re.finditer(comments, line):
            start = f"{idx + 1}.{match.start()}"
            end = f"{idx + 1}.{match.end()}"
            text_widget.tag_add("comment", start, end)

        for match in re.finditer(numbers, line):
            start = f"{idx + 1}.{match.start()}"
            end = f"{idx + 1}.{match.end()}"
            text_widget.tag_add("number", start, end)

        idx += 1

    text_widget.tag_config("keyword", foreground="#FF79C6")
    text_widget.tag_config("string", foreground="#F1FA8C")
    text_widget.tag_config("comment", foreground="#6272A4")
    text_widget.tag_config("number", foreground="#8BE9FD")

    text_widget.configure(state="disabled")

def clickable_label(master, text, url):
    label = ctk.CTkLabel(master, text=text, font=("Segoe UI", 16), text_color="cyan", cursor="hand2")
    label.bind("<Button-1>", lambda e: webbrowser.open_new(url))
    return label

class AIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Yashvir Gaming AI Tool")
        self.geometry("1283x906")
        self.resizable(True, True)

        self.api_key_var = ctk.StringVar()
        self.model_var = ctk.StringVar(value=MODEL_ORDER[0])
        self.size_var = ctk.StringVar(value="1280x720 (HD)")

        ctk.CTkLabel(self, text="API Key:", font=("Segoe UI", 14)).pack(pady=5)
        ctk.CTkEntry(self, textvariable=self.api_key_var, show="*", width=500).pack(pady=5)

        ctk.CTkLabel(self, text="Select Model:", font=("Segoe UI", 14)).pack(pady=5)
        ctk.CTkOptionMenu(self, values=MODEL_ORDER, variable=self.model_var).pack(pady=5)

        self.input_box = ctk.CTkTextbox(self, width=800, height=200)
        self.input_box.pack(pady=10)

        self.output_box = ctk.CTkTextbox(self, width=800, height=300)
        self.output_box.pack(pady=10)
        self.output_box.configure(state="disabled")

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Send", command=self.send_prompt).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Generate Image", command=self.generate_image).grid(row=0, column=1, padx=5)

        ctk.CTkLabel(self, text="Image Size:", font=("Segoe UI", 14)).pack(pady=5)
        ctk.CTkOptionMenu(self, values=list(IMAGE_SIZES.keys()), variable=self.size_var).pack(pady=5)

        clickable_label(self, "Made with ♥ By Yashvir Gaming\nTelegram: https://t.me/therealyashvirgaming", "https://t.me/therealyashvirgaming").pack(pady=10)

    def send_prompt(self):
        threading.Thread(target=self._send_prompt_thread).start()

    def _send_prompt_thread(self):
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showerror("Error", "Please enter your API key.")
            return

        prompt = self.input_box.get("1.0", "end").strip()
        if not prompt:
            return

        client = OpenAI(api_key=api_key)
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", "Thinking...\n")
        self.output_box.configure(state="disabled")

        try:
            response = client.chat.completions.create(
                model=self.model_var.get(),
                messages=[{"role": "user", "content": prompt}],
            )
            output = response.choices[0].message.content
            if re.search(r"\b(def|class|import|from|function|var|let|const)\b", output):
                syntax_highlight(self.output_box, output)
            else:
                self.output_box.configure(state="normal")
                self.output_box.delete("1.0", "end")
                self.output_box.insert("end", output)
                self.output_box.configure(state="disabled")
        except Exception as e:
            self.output_box.configure(state="normal")
            self.output_box.delete("1.0", "end")
            self.output_box.insert("end", f"Error: {e}")
            self.output_box.configure(state="disabled")

    def generate_image(self):
        threading.Thread(target=self._generate_image_thread).start()

    def _generate_image_thread(self):
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showerror("Error", "Please enter your API key.")
            return

        prompt = self.input_box.get("1.0", "end").strip()
        if not prompt:
            return

        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", "Please wait... Generating image. Estimated time: ~10 seconds\n")
        self.output_box.configure(state="disabled")

        client = OpenAI(api_key=api_key)
        try:
            size = IMAGE_SIZES[self.size_var.get()]
            result = client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                size=size
            )
            image_url = result.data[0].url
            filename = f"generated_image_{int(time.time())}.png"
            import requests
            img_data = requests.get(image_url).content
            with open(filename, "wb") as f:
                f.write(img_data)
            self.output_box.configure(state="normal")
            self.output_box.delete("1.0", "end")
            self.output_box.insert("end", f"Image saved as {filename}\nURL: {image_url}")
            self.output_box.configure(state="disabled")
        except Exception as e:
            self.output_box.configure(state="normal")
            self.output_box.delete("1.0", "end")
            self.output_box.insert("end", f"Error: {e}")
            self.output_box.configure(state="disabled")

if __name__ == "__main__":
    app = AIApp()
    app.mainloop()
