import flet as ft
from whatsapp_client import WhatsAppBusinessClient

class LoginPage(ft.Container):
    def __init__(self, page: ft.Page, client: WhatsAppBusinessClient, on_success_callback):
        super().__init__()
        self.page = page
        self.client = client
        self.on_success_callback = on_success_callback

        # Configuration for visual container
        self.alignment = ft.alignment.center
        self.expand = True
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#0f172a", "#1e1b4b"]  # Sleek dark slate to dark indigo gradient
        )

        # UI Input Fields
        self.token_input = ft.TextField(
            label="Meta Access Token",
            password=True,
            can_reveal_password=True,
            border_radius=12,
            border_color="#334155",
            focused_border_color="#10b981",  # Vibrant emerald focused border
            focused_color="#f8fafc",
            label_style=ft.TextStyle(color="#94a3b8"),
            hint_text="EAAG...",
            hint_style=ft.TextStyle(color="#475569"),
            prefix_icon=ft.icons.KEY_ROUNDED,
            prefix_style=ft.TextStyle(color="#10b981"),
            text_style=ft.TextStyle(color="#f1f5f9"),
            cursor_color="#10b981",
        )

        self.phone_id_input = ft.TextField(
            label="Phone Number ID",
            border_radius=12,
            border_color="#334155",
            focused_border_color="#10b981",
            focused_color="#f8fafc",
            label_style=ft.TextStyle(color="#94a3b8"),
            hint_text="e.g., 10849382103982",
            hint_style=ft.TextStyle(color="#475569"),
            prefix_icon=ft.icons.PHONE_ANDROID_ROUNDED,
            prefix_style=ft.TextStyle(color="#10b981"),
            text_style=ft.TextStyle(color="#f1f5f9"),
            cursor_color="#10b981",
        )

        self.business_id_input = ft.TextField(
            label="WhatsApp Business Account ID",
            border_radius=12,
            border_color="#334155",
            focused_border_color="#10b981",
            focused_color="#f8fafc",
            label_style=ft.TextStyle(color="#94a3b8"),
            hint_text="e.g., 20849182390192",
            hint_style=ft.TextStyle(color="#475569"),
            prefix_icon=ft.icons.BUSINESS_CENTER_ROUNDED,
            prefix_style=ft.TextStyle(color="#10b981"),
            text_style=ft.TextStyle(color="#f1f5f9"),
            cursor_color="#10b981",
        )

        # Status & Message label
        self.status_message = ft.Text(
            value="",
            color="#ef4444",  # Default red/error color
            size=13,
            weight=ft.FontWeight.W_500,
            text_align=ft.TextAlign.CENTER,
            visible=False
        )

        # Loading Indicator
        self.spinner = ft.ProgressRing(
            width=24,
            height=24,
            stroke_width=3,
            color="#10b981",
            visible=False
        )

        # Action Button
        self.submit_btn = ft.ElevatedButton(
            text="Verify & Connect",
            icon=ft.icons.LINK_ROUNDED,
            style=ft.ButtonStyle(
                color="#ffffff",
                bgcolor={
                    ft.ControlState.DEFAULT: "#10b981",
                    ft.ControlState.HOVERED: "#059669",
                },
                padding=ft.padding.symmetric(horizontal=24, vertical=16),
                shape=ft.RoundedRectangleBorder(radius=12),
                elevation={"hovered": 5, "default": 2},
            ),
            on_click=self.handle_connect
        )

        # Prepopulate inputs if client already has credentials
        if self.client.access_token:
            self.token_input.value = self.client.access_token
        if self.client.phone_number_id:
            self.phone_id_input.value = self.client.phone_number_id
        if self.client.business_account_id:
            self.business_id_input.value = self.client.business_account_id

        # Render Content
        self.content = ft.Center(
            content=ft.Container(
                width=450,
                padding=36,
                border_radius=24,
                bgcolor="#1e293b",  # Dark slate gray
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color="#090d16",
                    offset=ft.Offset(0, 10),
                ),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        # Header with Logo Icon
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                            controls=[
                                ft.Container(
                                    content=ft.Icon(
                                        name=ft.icons.SETTINGS_INPUT_COMPONENT_ROUNDED,
                                        size=48,
                                        color="#10b981",
                                    ),
                                    bgcolor="#064e3b",
                                    padding=16,
                                    border_radius=30,
                                    margin=ft.margin.only(bottom=10)
                                ),
                                ft.Text(
                                    "WhatsApp Smart Assistant",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color="#f8fafc",
                                ),
                                ft.Text(
                                    "Configure your Official Cloud API credentials",
                                    size=13,
                                    color="#64748b",
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ]
                        ),
                        
                        # Form Fields
                        ft.Column(
                            spacing=15,
                            controls=[
                                self.token_input,
                                self.phone_id_input,
                                self.business_id_input,
                            ]
                        ),
                        
                        # Status message area
                        self.status_message,

                        # Connect Button and Spinner
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=15,
                            controls=[
                                self.submit_btn,
                                self.spinner
                            ]
                        ),

                        # Footer Help Link
                        ft.TextButton(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=5,
                                controls=[
                                    ft.Icon(name=ft.icons.HELP_OUTLINE_ROUNDED, size=14, color="#64748b"),
                                    ft.Text("Where do I find my Meta API credentials?", size=12, color="#64748b", decoration=ft.TextDecoration.UNDERLINE),
                                ]
                            ),
                            on_click=lambda _: self.page.launch_url("https://developers.facebook.com/docs/whatsapp/cloud-api/get-started")
                        )
                    ]
                )
            )
        )

    def show_message(self, text, is_error=True):
        self.status_message.value = text
        self.status_message.color = "#ef4444" if is_error else "#10b981"
        self.status_message.visible = True
        self.page.update()

    def set_loading(self, loading: bool):
        self.submit_btn.disabled = loading
        self.spinner.visible = loading
        if loading:
            self.status_message.visible = False
        self.page.update()

    def handle_connect(self, e):
        token = self.token_input.value.strip()
        phone_id = self.phone_id_input.value.strip()
        biz_id = self.business_id_input.value.strip()

        if not token or not phone_id or not biz_id:
            self.show_message("All fields must be filled in.")
            return

        self.set_loading(True)

        # Run verification check in background to keep UI fully responsive
        def verify_task():
            success, result = self.client.verify_credentials(token, phone_id, biz_id)
            if success:
                # Save credentials to local .env
                self.client.save_credentials(token, phone_id, biz_id)
                self.show_message("Connection Successful! Storing credentials...", is_error=False)
                # Small delay to let user see success state before callback
                import time
                time.sleep(1)
                self.set_loading(False)
                # Trigger completion callback
                self.on_success_callback(result)
            else:
                self.set_loading(False)
                self.show_message(result)

        import threading
        threading.Thread(target=verify_task, daemon=True).start()
