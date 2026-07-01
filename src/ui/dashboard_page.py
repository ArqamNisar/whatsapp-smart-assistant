import flet as ft
from whatsapp_client import WhatsAppBusinessClient

class DashboardPage(ft.Container):
    def __init__(self, page: ft.Page, client: WhatsAppBusinessClient, verified_info, on_logout_callback):
        super().__init__()
        self.page = page
        self.client = client
        self.verified_info = verified_info
        self.on_logout_callback = on_logout_callback

        # Configuration for outer container
        self.expand = True
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#0f172a", "#020617"]  # Very deep premium slate-to-black gradient
        )
        self.padding = 24

        # Verified Info Extraction
        self.phone_num = verified_info.get("display_phone_number", "Business Account")
        self.verified_name = verified_info.get("verified_name", "WhatsApp Business")
        self.quality_rating = verified_info.get("quality_rating", "GREEN")

        # Set up state
        self.active_tab = "chats" # chats, groups, announcements
        self.chat_list_container = ft.Column(spacing=10, scroll=ft.ScrollMode.ADAPTIVE)
        self.messages_container = ft.Column(spacing=12, scroll=ft.ScrollMode.ADAPTIVE)
        
        # Header / Top Bar
        self.header = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.icons.SUPPORT_AGENT_ROUNDED, color="#10b981", size=28),
                            bgcolor="#064e3b",
                            padding=10,
                            border_radius=12
                        ),
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(self.verified_name, size=18, weight=ft.FontWeight.BOLD, color="#f8fafc"),
                                ft.Row(
                                    spacing=5,
                                    controls=[
                                        ft.Container(width=8, height=8, bgcolor="#10b981", border_radius=4),
                                        ft.Text(f"Active • {self.phone_num}", size=12, color="#94a3b8")
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                # Quick Status Cards
                ft.Row(
                    spacing=15,
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                spacing=5,
                                controls=[
                                    ft.Icon(ft.icons.SHIELD_ROUNDED, size=14, color="#10b981"),
                                    ft.Text(f"Quality: {self.quality_rating}", size=11, color="#10b981", weight=ft.FontWeight.W_600)
                                ]
                            ),
                            bgcolor="#064e3b",
                            padding=ft.padding.symmetric(horizontal=12, vertical=6),
                            border_radius=20,
                        ),
                        ft.IconButton(
                            icon=ft.icons.LOGOUT_ROUNDED,
                            icon_color="#ef4444",
                            tooltip="Disconnect API Key",
                            on_click=self.handle_logout
                        )
                    ]
                )
            ]
        )

        # Tab Buttons
        self.tab_chats_btn = self.create_tab_button("Chats", ft.icons.CHAT_BUBBLE_OUTLINE_ROUNDED, "chats")
        self.tab_groups_btn = self.create_tab_button("Groups", ft.icons.GROUPS_ROUNDED, "groups")
        self.tab_announcements_btn = self.create_tab_button("Announcements", ft.icons.CAMPAIGN_ROUNDED, "announcements")
        
        self.tab_row = ft.Row(
            spacing=10,
            controls=[
                self.tab_chats_btn,
                self.tab_groups_btn,
                self.tab_announcements_btn
            ]
        )

        # Build Mock Data views
        self.load_tab_data()

        # Webhook Console Panel (Shows live listening info)
        self.webhook_logs = ft.Column(
            spacing=5,
            scroll=ft.ScrollMode.END,
            controls=[
                ft.Text("[SYSTEM] Local Webhook server initiated on http://localhost:8000/webhook", color="#10b981", size=11, font_family="monospace"),
                ft.Text("[SYSTEM] Status: Listening... (Setup ngrok to map Meta public URL)", color="#64748b", size=11, font_family="monospace"),
            ]
        )

        self.webhook_panel = ft.Container(
            padding=16,
            bgcolor="#0b0f19",
            border=ft.border.all(1, "#1e293b"),
            border_radius=12,
            height=120,
            content=ft.Column(
                spacing=5,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Webhook Console Feed", size=12, weight=ft.FontWeight.BOLD, color="#94a3b8"),
                            ft.Text("Live", size=10, color="#10b981", weight=ft.FontWeight.BOLD)
                        ]
                    ),
                    ft.Divider(height=1, color="#1e293b"),
                    ft.Container(content=self.webhook_logs, expand=True)
                ]
            )
        )

        # Main Layout Assembly
        self.content = ft.Column(
            expand=True,
            spacing=20,
            controls=[
                self.header,
                ft.Divider(height=1, color="#1e293b"),
                # Main split area
                ft.Row(
                    expand=True,
                    spacing=20,
                    controls=[
                        # Left side: Navigation tabs + List of items
                        ft.Container(
                            width=320,
                            bgcolor="#1e293b",
                            border_radius=16,
                            padding=16,
                            content=ft.Column(
                                spacing=15,
                                controls=[
                                    self.tab_row,
                                    ft.Divider(height=1, color="#334155"),
                                    ft.Text("CONVERSATIONS", size=11, weight=ft.FontWeight.BOLD, color="#64748b"),
                                    ft.Container(content=self.chat_list_container, expand=True)
                                ]
                            )
                        ),
                        
                        # Right side: Detail view / Chat thread simulator
                        ft.Container(
                            expand=True,
                            bgcolor="#1e293b",
                            border_radius=16,
                            padding=20,
                            content=ft.Column(
                                spacing=15,
                                controls=[
                                    # Active chat title banner
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Row(
                                                spacing=10,
                                                controls=[
                                                    ft.CircleAvatar(bgcolor="#0284c7", content=ft.Text("JD", color="#ffffff")),
                                                    ft.Column(
                                                        spacing=2,
                                                        controls=[
                                                            ft.Text("John Doe", size=15, weight=ft.FontWeight.BOLD, color="#f8fafc"),
                                                            ft.Text("+1 (555) 0199 • Customer", size=11, color="#94a3b8")
                                                        ]
                                                    )
                                                ]
                                            ),
                                            ft.Container(
                                                content=ft.Text("Meta Verified Chat", size=10, color="#0284c7"),
                                                border=ft.border.all(1, "#0284c7"),
                                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                                border_radius=10
                                            )
                                        ]
                                    ),
                                    ft.Divider(height=1, color="#334155"),
                                    
                                    # Message Bubbles Box
                                    ft.Container(
                                        content=self.messages_container,
                                        expand=True,
                                        alignment=ft.alignment.bottom_left
                                    ),
                                    
                                    # Quick message simulator input
                                    ft.Row(
                                        spacing=10,
                                        controls=[
                                            ft.TextField(
                                                hint_text="Simulate sending a reply...",
                                                hint_style=ft.TextStyle(color="#475569"),
                                                border_radius=12,
                                                border_color="#334155",
                                                focused_border_color="#10b981",
                                                text_style=ft.TextStyle(color="#f1f5f9"),
                                                expand=True,
                                                shift_enter=True,
                                                on_submit=self.simulate_reply
                                            ),
                                            ft.IconButton(
                                                icon=ft.icons.SEND_ROUNDED,
                                                icon_color="#ffffff",
                                                bgcolor="#10b981",
                                                on_click=self.simulate_reply
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                ),
                
                # Bottom status bar console
                self.webhook_panel
            ]
        )

    def create_tab_button(self, text, icon, tab_id):
        is_active = (tab_id == self.active_tab)
        return ft.Container(
            content=ft.Row(
                spacing=5,
                controls=[
                    ft.Icon(icon, size=16, color="#10b981" if is_active else "#94a3b8"),
                    ft.Text(text, size=12, weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL, color="#ffffff" if is_active else "#94a3b8")
                ]
            ),
            bgcolor="#064e3b" if is_active else "#1e293b",
            border=ft.border.all(1, "#10b981" if is_active else "#334155"),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border_radius=8,
            cursor=ft.MouseCursor.POINTER,
            on_click=lambda _: self.change_tab(tab_id)
        )

    def change_tab(self, tab_id):
        self.active_tab = tab_id
        # Redraw tab buttons
        self.tab_chats_btn.bgcolor = "#064e3b" if tab_id == "chats" else "#1e293b"
        self.tab_chats_btn.border = ft.border.all(1, "#10b981" if tab_id == "chats" else "#334155")
        
        self.tab_groups_btn.bgcolor = "#064e3b" if tab_id == "groups" else "#1e293b"
        self.tab_groups_btn.border = ft.border.all(1, "#10b981" if tab_id == "groups" else "#334155")

        self.tab_announcements_btn.bgcolor = "#064e3b" if tab_id == "announcements" else "#1e293b"
        self.tab_announcements_btn.border = ft.border.all(1, "#10b981" if tab_id == "announcements" else "#334155")

        self.load_tab_data()
        self.page.update()

    def load_tab_data(self):
        self.chat_list_container.controls.clear()
        
        if self.active_tab == "chats":
            data = [
                {"name": "John Doe", "subtitle": "Hi! Is the Smart Assistant online?", "time": "14:48", "color": "#0284c7"},
                {"name": "Jane Smith", "subtitle": "Thanks for the quick response.", "time": "Yesterday", "color": "#f59e0b"},
                {"name": "Alice Johnson", "subtitle": "Can you check my reservation?", "time": "Monday", "color": "#10b981"},
            ]
        elif self.active_tab == "groups":
            data = [
                {"name": "Team Alerts", "subtitle": "Webhook: Deployment successful.", "time": "12:30", "color": "#8b5cf6"},
                {"name": "Project Alpha", "subtitle": "Bob: Meeting shifted to 3 PM.", "time": "10:15", "color": "#ec4899"},
            ]
        else: # announcements
            data = [
                {"name": "Meta Broadcast", "subtitle": "API version v20.0 upgrades active.", "time": "July 1", "color": "#10b981"},
                {"name": "System Health", "subtitle": "No outages reported in Meta Graph.", "time": "June 30", "color": "#06b6d4"},
            ]

        for item in data:
            self.chat_list_container.controls.append(
                ft.Container(
                    padding=10,
                    border_radius=10,
                    bgcolor="#0f172a",
                    border=ft.border.all(1, "#334155"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=10,
                                controls=[
                                    ft.CircleAvatar(bgcolor=item["color"], radius=16, content=ft.Text(item["name"][:2], size=10, color="#ffffff")),
                                    ft.Column(
                                        spacing=2,
                                        controls=[
                                            ft.Text(item["name"], size=13, weight=ft.FontWeight.BOLD, color="#f8fafc"),
                                            ft.Text(item["subtitle"], size=11, color="#64748b", max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, width=150)
                                        ]
                                    )
                                ]
                            ),
                            ft.Text(item["time"], size=10, color="#475569")
                        ]
                    )
                )
            )

        # Set up a few default mock chat messages inside the thread view
        self.messages_container.controls.clear()
        self.messages_container.controls.extend([
            self.chat_bubble("Hello! Welcome to the WhatsApp Business Smart Assistant. How can we help you?", is_incoming=True, timestamp="14:40"),
            self.chat_bubble("Hi! Is the Smart Assistant online?", is_incoming=False, timestamp="14:48"),
            self.chat_bubble("Yes, connection is live. Your webhook listens in the background.", is_incoming=True, timestamp="14:49"),
        ])

    def chat_bubble(self, text, is_incoming, timestamp):
        return ft.Row(
            alignment=ft.MainAxisAlignment.START if is_incoming else ft.MainAxisAlignment.END,
            controls=[
                ft.Container(
                    content=ft.Column(
                        spacing=4,
                        controls=[
                            ft.Text(text, size=13, color="#f1f5f9"),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    ft.Text(timestamp, size=9, color="#94a3b8"),
                                    ft.Icon(ft.icons.DONE_ALL_ROUNDED, size=12, color="#10b981") if not is_incoming else ft.Container()
                                ]
                            )
                        ]
                    ),
                    bgcolor="#1e293b" if is_incoming else "#064e3b", # Incoming is slate, Outgoing is green
                    border=ft.border.all(1, "#334155" if is_incoming else "#10b981"),
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    border_radius=ft.border_radius.only(
                        top_left=12, top_right=12, 
                        bottom_left=0 if is_incoming else 12, 
                        bottom_right=12 if is_incoming else 0
                    ),
                    max_width=400,
                )
            ]
        )

    def simulate_reply(self, e):
        # We simulate appending a reply, and posting a webhook console log
        text_field = e.control if isinstance(e.control, ft.TextField) else e.control.parent.controls[0]
        val = text_field.value.strip()
        if not val:
            return
        
        # Append message bubble
        import datetime
        now = datetime.datetime.now().strftime("%H:%M")
        self.messages_container.controls.append(self.chat_bubble(val, is_incoming=False, timestamp=now))
        text_field.value = ""
        
        # Log to Console Feed
        self.webhook_logs.controls.append(
            ft.Text(f"[OUTGOING] Simulated reply sent to API: \"{val}\"", color="#64748b", size=11, font_family="monospace")
        )
        
        self.page.update()

    def handle_logout(self, e):
        self.client.clear_credentials()
        self.on_logout_callback()
