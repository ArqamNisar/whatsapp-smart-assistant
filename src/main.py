import customtkinter as ctk
import threading
import time
from whatsapp_client import WhatsAppBusinessClient
from ui.login_page import LoginPage
from ui.dashboard_page import DashboardPage

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("WhatsApp Smart Assistant Console")
        self.geometry("950x700")
        self.minsize(850, 600)
        
        # Set default theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize WhatsApp client
        self.client = WhatsAppBusinessClient()

        # Current view frame tracker
        self.current_view = None

        # Build initial Loading View
        self.show_loading_view()

        # Check credentials in background
        threading.Thread(target=self.check_saved_credentials, daemon=True).start()

    def clear_current_view(self):
        if self.current_view is not None:
            self.current_view.destroy()
            self.current_view = None

    def show_loading_view(self):
        self.clear_current_view()
        
        # Loading Frame
        self.current_view = ctk.CTkFrame(self, fg_color="#0f172a")
        self.current_view.pack(fill="both", expand=True)

        # Centered container
        container = ctk.CTkFrame(self.current_view, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        loading_label = ctk.CTkLabel(
            container,
            text="Checking saved API credentials...",
            font=ctk.CTkFont(family="Inter", size=14),
            text_color="#94a3b8"
        )
        loading_label.pack(pady=(0, 20))

        progress = ctk.CTkProgressBar(
            container,
            orientation="horizontal",
            mode="indeterminate",
            fg_color="#1e293b",
            progress_color="#10b981",
            width=250,
            height=6
        )
        progress.pack()
        progress.start()

    def show_login_page(self):
        self.clear_current_view()
        self.current_view = LoginPage(
            parent=self,
            client=self.client,
            on_success_callback=self.show_dashboard_page
        )
        self.current_view.pack(fill="both", expand=True)

    def show_dashboard_page(self, verified_info):
        self.clear_current_view()
        self.current_view = DashboardPage(
            parent=self,
            client=self.client,
            verified_info=verified_info,
            on_logout_callback=self.show_login_page
        )
        self.current_view.pack(fill="both", expand=True)

    def check_saved_credentials(self):
        # Simulate check delay for visual transition
        time.sleep(1)
        
        if self.client.access_token and self.client.phone_number_id and self.client.business_account_id:
            success, result = self.client.verify_credentials(
                self.client.access_token,
                self.client.phone_number_id,
                self.client.business_account_id
            )
            if success:
                self.after(0, self.show_dashboard_page, result)
            else:
                self.after(0, self.show_login_page)
        else:
            self.after(0, self.show_login_page)

if __name__ == "__main__":
    app = App()
    app.mainloop()
