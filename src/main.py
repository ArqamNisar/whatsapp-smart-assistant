import flet as ft
import time
from whatsapp_client import WhatsAppBusinessClient
from ui.login_page import LoginPage
from ui.dashboard_page import DashboardPage

def main(page: ft.Page):
    # App Window settings
    page.title = "WhatsApp Smart Assistant Console"
    page.window_width = 950
    page.window_height = 700
    page.window_min_width = 850
    page.window_min_height = 600
    page.window_resizable = True
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0f172a"

    # Initialize client
    client = WhatsAppBusinessClient()

    # Loading screen layout while verifying existing credentials on startup
    loading_screen = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#0f172a", "#1e1b4b"]
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.ProgressRing(color="#10b981", width=50, height=50, stroke_width=4),
                ft.Text("Checking saved API credentials...", size=14, color="#94a3b8")
            ]
        )
    )

    # Put the loading screen initially
    page.add(loading_screen)
    page.update()

    def show_login_page():
        page.controls.clear()
        login_view = LoginPage(
            page=page,
            client=client,
            on_success_callback=show_dashboard_page
        )
        page.add(login_view)
        page.update()

    def show_dashboard_page(verified_info):
        page.controls.clear()
        dashboard_view = DashboardPage(
            page=page,
            client=client,
            verified_info=verified_info,
            on_logout_callback=show_login_page
        )
        page.add(dashboard_view)
        page.update()

    # Startup validation routing
    def check_saved_credentials():
        if client.access_token and client.phone_number_id and client.business_account_id:
            # Try to verify stored credentials
            success, result = client.verify_credentials(
                client.access_token,
                client.phone_number_id,
                client.business_account_id
            )
            if success:
                show_dashboard_page(result)
            else:
                # Credentials exist but failed check (e.g. expired token)
                show_login_page()
        else:
            # No credentials stored
            show_login_page()

    # Run check in background to prevent startup freeze
    import threading
    threading.Thread(target=check_saved_credentials, daemon=True).start()

if __name__ == "__main__":
    ft.app(target=main)
