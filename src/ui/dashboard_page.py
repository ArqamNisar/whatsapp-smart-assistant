import customtkinter as ctk
import datetime
from whatsapp_client import WhatsAppBusinessClient

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, client: WhatsAppBusinessClient, verified_info, on_logout_callback):
        super().__init__(parent, fg_color="#0f172a") # Sleek slate-to-black matching dashboard
        self.client = client
        self.verified_info = verified_info
        self.on_logout_callback = on_logout_callback

        # Verified Info Extraction
        self.phone_num = verified_info.get("display_phone_number", "Business Account")
        self.verified_name = verified_info.get("verified_name", "WhatsApp Business")
        self.quality_rating = verified_info.get("quality_rating", "GREEN")

        # Set up state
        self.active_tab = "chats" # chats, groups, announcements
        self.active_chat_name = "John Doe"
        self.active_chat_type = "Customer"

        # Build Main Layout
        self.setup_ui()
        self.load_tab_data()
        
        # Add default messages
        self.messages_container.after(100, self.setup_default_messages)

    def setup_ui(self):
        # 1. Header Frame
        header = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=16, height=75)
        header.pack(fill="x", pady=(0, 15))
        header.pack_propagate(False)

        # Header Info Left
        info_left = ctk.CTkFrame(header, fg_color="transparent")
        info_left.pack(side="left", padx=20, pady=10)

        name_row = ctk.CTkFrame(info_left, fg_color="transparent")
        name_row.pack(anchor="w")

        status_dot = ctk.CTkFrame(name_row, width=8, height=8, corner_radius=4, fg_color="#10b981")
        status_dot.pack(side="left", padx=(0, 8))

        name_label = ctk.CTkLabel(
            name_row, 
            text=self.verified_name, 
            font=ctk.CTkFont(family="Inter", size=18, weight="bold"),
            text_color="#f8fafc"
        )
        name_label.pack(side="left")

        phone_label = ctk.CTkLabel(
            info_left,
            text=f"Active • {self.phone_num}",
            font=ctk.CTkFont(family="Inter", size=12),
            text_color="#94a3b8"
        )
        phone_label.pack(anchor="w", padx=16)

        # Header Info Right (Status badge & Logout)
        info_right = ctk.CTkFrame(header, fg_color="transparent")
        info_right.pack(side="right", padx=20, pady=10)

        quality_badge = ctk.CTkFrame(info_right, fg_color="#064e3b", corner_radius=20)
        quality_badge.pack(side="left", padx=(0, 15))

        quality_label = ctk.CTkLabel(
            quality_badge,
            text=f"Quality: {self.quality_rating}",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#10b981"
        )
        quality_label.pack(padx=12, pady=6)

        logout_btn = ctk.CTkButton(
            info_right,
            text="Disconnect API",
            fg_color="#ef4444",
            hover_color="#dc2626",
            text_color="#ffffff",
            width=130,
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            corner_radius=10,
            command=self.handle_logout
        )
        logout_btn.pack(side="right")

        # 2. Main Middle Area (Split screen)
        middle_area = ctk.CTkFrame(self, fg_color="transparent")
        middle_area.pack(fill="both", expand=True, pady=(0, 15))

        # Left sub-panel
        left_sub = ctk.CTkFrame(middle_area, fg_color="#1e293b", corner_radius=16, width=320)
        left_sub.pack(side="left", fill="both", padx=(0, 15))
        left_sub.pack_propagate(False)

        # Tab button row inside left_sub
        tab_row = ctk.CTkFrame(left_sub, fg_color="transparent")
        tab_row.pack(fill="x", padx=15, pady=(15, 10))

        self.tab_chats_btn = ctk.CTkButton(
            tab_row,
            text="Chats",
            height=32,
            font=ctk.CTkFont(family="Inter", size=11, weight="bold"),
            command=lambda: self.change_tab("chats")
        )
        self.tab_chats_btn.pack(side="left", expand=True, fill="x", padx=2)

        self.tab_groups_btn = ctk.CTkButton(
            tab_row,
            text="Groups",
            height=32,
            font=ctk.CTkFont(family="Inter", size=11, weight="bold"),
            command=lambda: self.change_tab("groups")
        )
        self.tab_groups_btn.pack(side="left", expand=True, fill="x", padx=2)

        self.tab_announcements_btn = ctk.CTkButton(
            tab_row,
            text="Announce",
            height=32,
            font=ctk.CTkFont(family="Inter", size=11, weight="bold"),
            command=lambda: self.change_tab("announcements")
        )
        self.tab_announcements_btn.pack(side="left", expand=True, fill="x", padx=2)

        # Divider
        divider1 = ctk.CTkFrame(left_sub, fg_color="#334155", height=1)
        divider1.pack(fill="x", padx=15, pady=(5, 10))

        list_title = ctk.CTkLabel(
            left_sub,
            text="CONVERSATIONS",
            font=ctk.CTkFont(family="Inter", size=11, weight="bold"),
            text_color="#64748b"
        )
        list_title.pack(anchor="w", padx=15, pady=(0, 5))

        # Scrollable Chat/Items container
        self.chat_list_container = ctk.CTkScrollableFrame(
            left_sub, 
            fg_color="transparent",
            scrollbar_button_color="#334155"
        )
        self.chat_list_container.pack(fill="both", expand=True, padx=10, pady=(0, 15))

        # Right sub-panel (Thread view)
        self.right_sub = ctk.CTkFrame(middle_area, fg_color="#1e293b", corner_radius=16)
        self.right_sub.pack(side="right", fill="both", expand=True)

        # Active Chat Title Banner
        self.chat_banner = ctk.CTkFrame(self.right_sub, fg_color="transparent", height=60)
        self.chat_banner.pack(fill="x", padx=20, pady=(15, 5))
        self.chat_banner.pack_propagate(False)

        self.chat_title_name = ctk.CTkLabel(
            self.chat_banner,
            text=self.active_chat_name,
            font=ctk.CTkFont(family="Inter", size=16, weight="bold"),
            text_color="#f8fafc"
        )
        self.chat_title_name.pack(anchor="w", pady=(5, 0))

        self.chat_title_desc = ctk.CTkLabel(
            self.chat_banner,
            text=f"Conversation • {self.active_chat_type}",
            font=ctk.CTkFont(family="Inter", size=11),
            text_color="#94a3b8"
        )
        self.chat_title_desc.pack(anchor="w")

        meta_badge = ctk.CTkFrame(self.chat_banner, fg_color="transparent", border_width=1, border_color="#0284c7", corner_radius=10)
        meta_badge.pack(side="right", anchor="ne", pady=10)
        meta_badge_label = ctk.CTkLabel(meta_badge, text="Meta Verified Chat", text_color="#0284c7", font=ctk.CTkFont(family="Inter", size=10))
        meta_badge_label.pack(padx=8, pady=3)

        divider2 = ctk.CTkFrame(self.right_sub, fg_color="#334155", height=1)
        divider2.pack(fill="x", padx=20, pady=5)

        # Message Scroll Area
        self.messages_container = ctk.CTkScrollableFrame(
            self.right_sub, 
            fg_color="#0f172a", 
            corner_radius=12,
            scrollbar_button_color="#334155"
        )
        self.messages_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Message input row
        input_row = ctk.CTkFrame(self.right_sub, fg_color="transparent")
        input_row.pack(fill="x", padx=20, pady=(5, 20))

        self.reply_input = ctk.CTkEntry(
            input_row,
            placeholder_text="Simulate sending a reply...",
            fg_color="#0f172a",
            border_color="#334155",
            text_color="#f8fafc",
            placeholder_text_color="#475569",
            corner_radius=12,
            height=40
        )
        self.reply_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.reply_input.bind("<Return>", lambda e: self.simulate_reply())

        send_btn = ctk.CTkButton(
            input_row,
            text="Send",
            fg_color="#10b981",
            hover_color="#059669",
            text_color="#ffffff",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            corner_radius=12,
            width=80,
            height=40,
            command=self.simulate_reply
        )
        send_btn.pack(side="right")

        # 3. Webhook Console Panel (Shows live listening info)
        self.webhook_panel = ctk.CTkFrame(self, fg_color="#0b0f19", border_width=1, border_color="#1e293b", corner_radius=12, height=120)
        self.webhook_panel.pack(fill="x")
        self.webhook_panel.pack_propagate(False)

        console_title_row = ctk.CTkFrame(self.webhook_panel, fg_color="transparent")
        console_title_row.pack(fill="x", padx=15, pady=(10, 5))

        console_title = ctk.CTkLabel(
            console_title_row,
            text="Webhook Console Feed",
            font=ctk.CTkFont(family="Inter", size=12, weight="bold"),
            text_color="#94a3b8"
        )
        console_title.pack(side="left")

        live_lbl = ctk.CTkLabel(
            console_title_row,
            text="Live",
            font=ctk.CTkFont(family="Inter", size=11, weight="bold"),
            text_color="#10b981"
        )
        live_lbl.pack(side="right")

        self.webhook_logs = ctk.CTkScrollableFrame(
            self.webhook_panel,
            fg_color="transparent",
            scrollbar_button_color="#1e293b",
            height=60
        )
        self.webhook_logs.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # Initial logs
        self.log_console("[SYSTEM] Local Webhook server initiated on http://localhost:8000/webhook", "#10b981")
        self.log_console("[SYSTEM] Status: Listening... (Setup ngrok to map Meta public URL)", "#64748b")

    def log_console(self, text, color="#64748b"):
        log_text = ctk.CTkLabel(
            self.webhook_logs,
            text=text,
            font=ctk.CTkFont(family="Courier", size=11),
            text_color=color,
            anchor="w",
            justify="left"
        )
        log_text.pack(fill="x", anchor="w", pady=1)
        # Scroll to bottom
        try:
            self.webhook_logs._parent_canvas.yview_moveto(1.0)
        except Exception:
            pass

    def change_tab(self, tab_id):
        self.active_tab = tab_id
        self.load_tab_data()

    def update_tab_buttons(self):
        # Update colors to show active tab
        for tab_name, btn in [("chats", self.tab_chats_btn), ("groups", self.tab_groups_btn), ("announcements", self.tab_announcements_btn)]:
            if tab_name == self.active_tab:
                btn.configure(fg_color="#064e3b", border_color="#10b981", text_color="#10b981", border_width=1)
            else:
                btn.configure(fg_color="#1e293b", border_color="#334155", text_color="#94a3b8", border_width=1)

    def load_tab_data(self):
        self.update_tab_buttons()
        
        # Clear chat list container children
        for widget in self.chat_list_container.winfo_children():
            widget.destroy()

        if self.active_tab == "chats":
            data = [
                {"name": "John Doe", "subtitle": "Hi! Is the Smart Assistant online?", "time": "14:48", "color": "#0284c7", "type": "Customer"},
                {"name": "Jane Smith", "subtitle": "Thanks for the quick response.", "time": "Yesterday", "color": "#f59e0b", "type": "Customer"},
                {"name": "Alice Johnson", "subtitle": "Can you check my reservation?", "time": "Monday", "color": "#10b981", "type": "VIP Client"},
            ]
        elif self.active_tab == "groups":
            data = [
                {"name": "Team Alerts", "subtitle": "Webhook: Deployment successful.", "time": "12:30", "color": "#8b5cf6", "type": "Internal Team"},
                {"name": "Project Alpha", "subtitle": "Bob: Meeting shifted to 3 PM.", "time": "10:15", "color": "#ec4899", "type": "Project Group"},
            ]
        else: # announcements
            data = [
                {"name": "Meta Broadcast", "subtitle": "API version v20.0 upgrades active.", "time": "July 1", "color": "#10b981", "type": "System Broadcast"},
                {"name": "System Health", "subtitle": "No outages reported in Meta Graph.", "time": "June 30", "color": "#06b6d4", "type": "System Logs"},
            ]

        for item in data:
            item_frame = ctk.CTkFrame(self.chat_list_container, fg_color="#0f172a", border_width=1, border_color="#334155", corner_radius=10, height=55)
            item_frame.pack(fill="x", pady=4, padx=5)
            item_frame.pack_propagate(False)

            # Click handler to load the item
            # We bind to the frame and child labels
            click_cmd = lambda i=item: self.select_conversation(i)
            item_frame.bind("<Button-1>", lambda e, cmd=click_cmd: cmd())

            # Avatar
            avatar = ctk.CTkFrame(item_frame, fg_color=item["color"], width=30, height=30, corner_radius=15)
            avatar.pack(side="left", padx=10, pady=10)
            avatar.pack_propagate(False)
            avatar.bind("<Button-1>", lambda e, cmd=click_cmd: cmd())

            initials = ctk.CTkLabel(avatar, text=item["name"][:2], text_color="#ffffff", font=ctk.CTkFont(family="Inter", size=10, weight="bold"))
            initials.place(relx=0.5, rely=0.5, anchor="center")
            initials.bind("<Button-1>", lambda e, cmd=click_cmd: cmd())

            # Text content
            txt_box = ctk.CTkFrame(item_frame, fg_color="transparent")
            txt_box.pack(side="left", fill="both", expand=True, pady=6)
            txt_box.bind("<Button-1>", lambda e, cmd=click_cmd: cmd())

            lbl_name = ctk.CTkLabel(txt_box, text=item["name"], font=ctk.CTkFont(family="Inter", size=12, weight="bold"), text_color="#f8fafc", anchor="w")
            lbl_name.pack(fill="x")
            lbl_name.bind("<Button-1>", lambda e, cmd=click_cmd: cmd())

            lbl_sub = ctk.CTkLabel(txt_box, text=item["subtitle"], font=ctk.CTkFont(family="Inter", size=10), text_color="#64748b", anchor="w")
            lbl_sub.pack(fill="x")
            lbl_sub.bind("<Button-1>", lambda e, cmd=click_cmd: cmd())

            # Time
            lbl_time = ctk.CTkLabel(item_frame, text=item["time"], font=ctk.CTkFont(family="Inter", size=9), text_color="#475569")
            lbl_time.pack(side="right", padx=10, pady=15)
            lbl_time.bind("<Button-1>", lambda e, cmd=click_cmd: cmd())

    def select_conversation(self, item):
        self.active_chat_name = item["name"]
        self.active_chat_type = item["type"]
        self.chat_title_name.configure(text=self.active_chat_name)
        self.chat_title_desc.configure(text=f"Conversation • {self.active_chat_type}")
        
        # Load mock thread messages based on the name
        for widget in self.messages_container.winfo_children():
            widget.destroy()
            
        if item["name"] == "John Doe":
            self.setup_default_messages()
        else:
            self.add_chat_bubble(f"Welcome to {item['name']} thread.", is_incoming=True, timestamp="10:00")
            self.add_chat_bubble(f"This is a simulated archive for {item['type']}.", is_incoming=True, timestamp="10:01")

    def setup_default_messages(self):
        for widget in self.messages_container.winfo_children():
            widget.destroy()
        self.add_chat_bubble("Hello! Welcome to the WhatsApp Business Smart Assistant. How can we help you?", is_incoming=True, timestamp="14:40")
        self.add_chat_bubble("Hi! Is the Smart Assistant online?", is_incoming=False, timestamp="14:48")
        self.add_chat_bubble("Yes, connection is live. Your webhook listens in the background.", is_incoming=True, timestamp="14:49")

    def add_chat_bubble(self, text, is_incoming, timestamp):
        bubble_frame = ctk.CTkFrame(self.messages_container, fg_color="transparent")
        bubble_frame.pack(fill="x", pady=6, padx=5)

        # Bubble content
        bg_color = "#1e293b" if is_incoming else "#064e3b"
        border_color = "#334155" if is_incoming else "#10b981"
        
        card = ctk.CTkFrame(
            bubble_frame, 
            fg_color=bg_color, 
            border_width=1, 
            border_color=border_color, 
            corner_radius=12
        )
        
        # Alignment
        if is_incoming:
            card.pack(side="left", fill="both", padx=(0, 80))
        else:
            card.pack(side="right", fill="both", padx=(80, 0))

        # Text inside bubble
        lbl_msg = ctk.CTkLabel(
            card, 
            text=text, 
            font=ctk.CTkFont(family="Inter", size=12),
            text_color="#f1f5f9",
            wraplength=300,
            justify="left",
            anchor="w"
        )
        lbl_msg.pack(padx=12, pady=(8, 4), anchor="w")

        # Info inside bubble
        info_row = ctk.CTkFrame(card, fg_color="transparent")
        info_row.pack(fill="x", padx=12, pady=(0, 6), anchor="e")

        lbl_time = ctk.CTkLabel(
            info_row, 
            text=timestamp, 
            font=ctk.CTkFont(family="Inter", size=9),
            text_color="#94a3b8"
        )
        lbl_time.pack(side="left")

        if not is_incoming:
            lbl_check = ctk.CTkLabel(
                info_row, 
                text="  ✓✓", 
                font=ctk.CTkFont(family="Inter", size=9),
                text_color="#10b981"
            )
            lbl_check.pack(side="right")

        # Scroll to bottom
        try:
            self.messages_container._parent_canvas.yview_moveto(1.0)
        except Exception:
            pass

    def simulate_reply(self):
        val = self.reply_input.get().strip()
        if not val:
            return
        
        # Append message bubble
        now = datetime.datetime.now().strftime("%H:%M")
        self.add_chat_bubble(val, is_incoming=False, timestamp=now)
        self.reply_input.delete(0, "end")
        
        # Log to webhook console
        self.log_console(f"[OUTGOING] Simulated reply sent to API: \"{val}\"", "#64748b")

    def handle_logout(self):
        self.client.clear_credentials()
        self.on_logout_callback()
