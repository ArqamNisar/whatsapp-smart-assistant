import customtkinter as ctk
import threading
import time
from whatsapp_client import WhatsAppBusinessClient

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, client: WhatsAppBusinessClient, on_success_callback):
        # We initialize the frame with a nice background (dark/slate color)
        # Using a dark theme matching WhatsApp.
        super().__init__(parent, fg_color="#0f172a") # Sleek dark slate
        self.client = client
        self.on_success_callback = on_success_callback
        
        # Center card frame
        card = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=24, border_width=1, border_color="#334155", width=450, height=520)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)
        
        # Header / Title
        title_label = ctk.CTkLabel(
            card, 
            text="WhatsApp Smart Assistant", 
            font=ctk.CTkFont(family="Inter", size=24, weight="bold"),
            text_color="#f8fafc"
        )
        title_label.pack(pady=(36, 5))
        
        subtitle_label = ctk.CTkLabel(
            card,
            text="Configure your Official Cloud API credentials",
            font=ctk.CTkFont(family="Inter", size=13),
            text_color="#64748b"
        )
        subtitle_label.pack(pady=(0, 25))
        
        # Form inputs
        # Token Input
        token_label = ctk.CTkLabel(
            card,
            text="Meta Access Token",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#94a3b8"
        )
        token_label.pack(anchor="w", padx=40, pady=(10, 2))
        
        self.token_input = ctk.CTkEntry(
            card,
            placeholder_text="EAAG...",
            show="*", # Password mode
            fg_color="#0f172a",
            border_color="#334155",
            text_color="#f8fafc",
            placeholder_text_color="#475569",
            corner_radius=12,
            height=40
        )
        self.token_input.pack(fill="x", padx=40, pady=(0, 10))
        
        # Phone ID Input
        phone_id_label = ctk.CTkLabel(
            card,
            text="Phone Number ID",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#94a3b8"
        )
        phone_id_label.pack(anchor="w", padx=40, pady=(10, 2))
        
        self.phone_id_input = ctk.CTkEntry(
            card,
            placeholder_text="e.g., 10849382103982",
            fg_color="#0f172a",
            border_color="#334155",
            text_color="#f8fafc",
            placeholder_text_color="#475569",
            corner_radius=12,
            height=40
        )
        self.phone_id_input.pack(fill="x", padx=40, pady=(0, 10))
        
        # Business ID Input
        business_id_label = ctk.CTkLabel(
            card,
            text="WhatsApp Business Account ID",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#94a3b8"
        )
        business_id_label.pack(anchor="w", padx=40, pady=(10, 2))
        
        self.business_id_input = ctk.CTkEntry(
            card,
            placeholder_text="e.g., 20849182390192",
            fg_color="#0f172a",
            border_color="#334155",
            text_color="#f8fafc",
            placeholder_text_color="#475569",
            corner_radius=12,
            height=40
        )
        self.business_id_input.pack(fill="x", padx=40, pady=(0, 15))
        
        # Status / Error Label
        self.status_message = ctk.CTkLabel(
            card,
            text="",
            font=ctk.CTkFont(family="Inter", size=12),
            text_color="#ef4444",
            wraplength=370
        )
        self.status_message.pack(fill="x", padx=40, pady=(5, 5))
        
        # Connect Button
        self.submit_btn = ctk.CTkButton(
            card,
            text="Verify & Connect",
            fg_color="#10b981", # Emerald green
            hover_color="#059669",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
            corner_radius=12,
            height=42,
            command=self.handle_connect
        )
        self.submit_btn.pack(fill="x", padx=40, pady=(5, 10))
        
        # Loading Indicator (determinate progress bar used as loading)
        self.progress_bar = ctk.CTkProgressBar(
            card,
            orientation="horizontal",
            mode="indeterminate",
            fg_color="#1e293b",
            progress_color="#10b981",
            height=4
        )
        # We don't pack it initially, we only show it when loading
        
        # Help link
        help_btn = ctk.CTkButton(
            card,
            text="Where do I find my Meta API credentials? ↗",
            fg_color="transparent",
            hover_color="#334155",
            text_color="#64748b",
            font=ctk.CTkFont(family="Inter", size=11, underline=True),
            height=20,
            command=self.open_help_url
        )
        help_btn.pack(pady=(10, 15))
        
        # Prepopulate fields
        if self.client.access_token:
            self.token_input.insert(0, self.client.access_token)
        if self.client.phone_number_id:
            self.phone_id_input.insert(0, self.client.phone_number_id)
        if self.client.business_account_id:
            self.business_id_input.insert(0, self.client.business_account_id)

    def open_help_url(self):
        import webbrowser
        webbrowser.open("https://developers.facebook.com/docs/whatsapp/cloud-api/get-started")

    def show_message(self, text, is_error=True):
        self.status_message.configure(
            text=text,
            text_color="#ef4444" if is_error else "#10b981"
        )

    def set_loading(self, loading: bool):
        if loading:
            self.submit_btn.configure(state="disabled")
            self.progress_bar.pack(fill="x", padx=40, pady=(0, 10))
            self.progress_bar.start()
            self.status_message.configure(text="")
        else:
            self.submit_btn.configure(state="normal")
            self.progress_bar.stop()
            self.progress_bar.pack_forget()

    def handle_connect(self):
        token = self.token_input.get().strip()
        phone_id = self.phone_id_input.get().strip()
        biz_id = self.business_id_input.get().strip()

        if not token or not phone_id or not biz_id:
            self.show_message("All fields must be filled in.", is_error=True)
            return

        self.set_loading(True)

        def verify_task():
            success, result = self.client.verify_credentials(token, phone_id, biz_id)
            # Use after() to update UI thread-safely
            self.after(0, self.on_verification_complete, success, result, token, phone_id, biz_id)

        threading.Thread(target=verify_task, daemon=True).start()

    def on_verification_complete(self, success, result, token, phone_id, biz_id):
        if success:
            self.client.save_credentials(token, phone_id, biz_id)
            self.show_message("Connection Successful! Storing credentials...", is_error=False)
            
            # Navigate to dashboard after 1 second delay
            self.after(1000, lambda: [self.set_loading(False), self.on_success_callback(result)])
        else:
            self.set_loading(False)
            self.show_message(result, is_error=True)
