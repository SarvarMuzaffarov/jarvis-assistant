"""
JARVIS - GUI Moduli
Iron Man uslubidagi interfeys (CustomTkinter)
"""

import customtkinter as ctk
import threading
from datetime import datetime


class JarvisGUI:
    def __init__(self, on_text_input=None, on_mic_toggle=None, on_close=None):
        self.on_text_input = on_text_input
        self.on_mic_toggle = on_mic_toggle
        self.on_close = on_close
        self.is_listening = False
        self.root = None
        self.chat_display = None
        self.colors = {
            "bg_dark": "#0a0a0f", "bg_medium": "#121218",
            "bg_light": "#1a1a24", "accent": "#00d4ff",
            "accent_red": "#ff3333", "text_primary": "#ffffff",
            "text_secondary": "#8888aa", "border": "#2a2a3a",
            "input_bg": "#15151f", "button_hover": "#0099cc",
        }
    
    def start(self):
        self._create_window()
        self.root.mainloop()
    
    def _create_window(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root = ctk.CTk()
        self.root.title("J.A.R.V.I.S - AI Yordamchi")
        self.root.geometry("900x650")
        self.root.configure(fg_color=self.colors["bg_dark"])
        self.root.minsize(700, 500)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._create_header()
        self._create_chat_area()
        self._create_input_area()
        self._create_status_bar()


    def _create_header(self):
        header = ctk.CTkFrame(self.root, height=60, fg_color=self.colors["bg_medium"], corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=20, pady=10)
        ctk.CTkLabel(title_frame, text="⚡ J.A.R.V.I.S",
                    font=ctk.CTkFont(size=22, weight="bold"),
                    text_color=self.colors["accent"]).pack(side="left")
        ctk.CTkLabel(title_frame, text="  |  AI Yordamchi v1.0",
                    font=ctk.CTkFont(size=12),
                    text_color=self.colors["text_secondary"]).pack(side="left", padx=(10, 0))
        self.time_label = ctk.CTkLabel(header, text="", font=ctk.CTkFont(size=12),
                                       text_color=self.colors["text_secondary"])
        self.time_label.pack(side="right", padx=20)
        self._update_time()
        self.status_dot = ctk.CTkLabel(header, text="● Tayyor", font=ctk.CTkFont(size=12),
                                       text_color="#00ff88")
        self.status_dot.pack(side="right", padx=10)
    
    def _create_chat_area(self):
        chat_frame = ctk.CTkFrame(self.root, fg_color=self.colors["bg_dark"])
        chat_frame.pack(fill="both", expand=True, padx=15, pady=(10, 5))
        self.chat_display = ctk.CTkTextbox(chat_frame, font=ctk.CTkFont(size=14),
            fg_color=self.colors["bg_dark"], text_color=self.colors["text_primary"],
            border_width=1, border_color=self.colors["border"], corner_radius=12, wrap="word")
        self.chat_display.pack(fill="both", expand=True)
        self.chat_display.configure(state="disabled")
        self._add_welcome_message()
    
    def _create_input_area(self):
        input_frame = ctk.CTkFrame(self.root, height=60, fg_color=self.colors["bg_medium"], corner_radius=12)
        input_frame.pack(fill="x", padx=15, pady=(5, 10))
        input_frame.pack_propagate(False)
        self.mic_button = ctk.CTkButton(input_frame, text="🎤", width=45, height=40,
            fg_color=self.colors["bg_light"], hover_color=self.colors["accent"],
            corner_radius=20, command=self._toggle_mic)
        self.mic_button.pack(side="left", padx=(10, 5), pady=10)
        self.text_input = ctk.CTkEntry(input_frame, placeholder_text="Buyruq yoki savol yozing...",
            font=ctk.CTkFont(size=14), fg_color=self.colors["input_bg"],
            border_color=self.colors["border"], text_color=self.colors["text_primary"],
            corner_radius=20, height=40)
        self.text_input.pack(side="left", fill="x", expand=True, padx=5, pady=10)
        self.text_input.bind("<Return>", self._send_message)
        self.send_button = ctk.CTkButton(input_frame, text="➤", width=45, height=40,
            fg_color=self.colors["accent"], hover_color=self.colors["button_hover"],
            corner_radius=20, font=ctk.CTkFont(size=18), command=lambda: self._send_message(None))
        self.send_button.pack(side="right", padx=(5, 10), pady=10)
    
    def _create_status_bar(self):
        status_frame = ctk.CTkFrame(self.root, height=30, fg_color=self.colors["bg_medium"], corner_radius=0)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)
        self.status_label = ctk.CTkLabel(status_frame,
            text="🟢 Tayyor | 🎤 Mikrofon o'chirilgan | 🌐 Internet ulangan",
            font=ctk.CTkFont(size=11), text_color=self.colors["text_secondary"])
        self.status_label.pack(side="left", padx=15)


    def _add_welcome_message(self):
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Xayrli tong"
        elif hour < 18:
            greeting = "Xayrli kun"
        else:
            greeting = "Xayrli kech"
        welcome = (f"⚡ {greeting}, xo'jayin!\n"
                   f"Men Jarvis — sizning shaxsiy AI yordamchingizman.\n"
                   f"Savolingiz bo'lsa yozing yoki 🎤 tugmasini bosing.\n"
                   f"{'─' * 50}\n")
        self.add_message("jarvis", welcome)
    
    def add_message(self, role, text):
        if not self.chat_display:
            return
        self.chat_display.configure(state="normal")
        timestamp = datetime.now().strftime("%H:%M")
        if role == "user":
            prefix = f"\n👤 Siz [{timestamp}]:\n"
        elif role == "jarvis":
            prefix = f"\n⚡ Jarvis [{timestamp}]:\n"
        else:
            prefix = f"\n📌 Tizim [{timestamp}]:\n"
        self.chat_display.insert("end", prefix)
        self.chat_display.insert("end", f"{text}\n")
        self.chat_display.insert("end", f"{'─' * 50}\n")
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")
    
    def update_status(self, text):
        if self.status_label:
            self.status_label.configure(text=text)
    
    def set_listening(self, is_listening):
        self.is_listening = is_listening
        if is_listening:
            self.mic_button.configure(fg_color=self.colors["accent_red"], text="🔴")
            self.update_status("🔴 Tinglayapman... | Gapiring!")
        else:
            self.mic_button.configure(fg_color=self.colors["bg_light"], text="🎤")
            self.update_status("🟢 Tayyor | 🎤 Mikrofon o'chirilgan")
    
    def show_thinking(self):
        self.update_status("⏳ O'ylayapman...")
    
    def hide_thinking(self):
        self.update_status("🟢 Tayyor")
    
    def _send_message(self, event):
        text = self.text_input.get().strip()
        if text:
            self.text_input.delete(0, "end")
            self.add_message("user", text)
            if self.on_text_input:
                threading.Thread(target=self.on_text_input, args=(text,), daemon=True).start()
    
    def _toggle_mic(self):
        self.is_listening = not self.is_listening
        self.set_listening(self.is_listening)
        if self.on_mic_toggle:
            self.on_mic_toggle(self.is_listening)
    
    def _update_time(self):
        now = datetime.now().strftime("%H:%M:%S | %d.%m.%Y")
        if self.time_label:
            self.time_label.configure(text=now)
        if self.root:
            self.root.after(1000, self._update_time)
    
    def _on_close(self):
        if self.on_close:
            self.on_close()
        self.root.destroy()
    
    def clear_chat(self):
        if self.chat_display:
            self.chat_display.configure(state="normal")
            self.chat_display.delete("1.0", "end")
            self.chat_display.configure(state="disabled")
            self._add_welcome_message()
