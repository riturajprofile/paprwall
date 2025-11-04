    def setup_ui(self):
        """Setup the user interface with hero section layout (15% hero + 85% main with 40-60 split)."""
        
        # ===== HERO SECTION (15% height) =====
        hero_section = tk.Frame(
            self.root,
            bg=self.colors['hero_bg'],
            height=105  # 15% of 700px
        )
        hero_section.pack(side=tk.TOP, fill=tk.X)
        hero_section.pack_propagate(False)
        
        # Logo + Title (Left)
        logo_frame = tk.Frame(hero_section, bg=self.colors['hero_bg'])
        logo_frame.pack(side=tk.LEFT, padx=30, pady=20)
        
        tk.Label(
            logo_frame,
            text="Papr",
            font=self.fonts['logo'],
            bg=self.colors['hero_bg'],
            fg=self.colors['accent_blue']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            logo_frame,
            text="Wall",
            font=self.fonts['logo'],
            bg=self.colors['hero_bg'],
            fg=self.colors['accent_purple']
        ).pack(side=tk.LEFT)
        
        tk.Label(
            logo_frame,
            text="  |  Modern Wallpaper Manager",
            font=self.fonts['hero_title'],
            bg=self.colors['hero_bg'],
            fg=self.colors['text_secondary']
        ).pack(side=tk.LEFT, padx=(10, 0))
        
        # Quick Actions (Right)
        actions_frame = tk.Frame(hero_section, bg=self.colors['hero_bg'])
        actions_frame.pack(side=tk.RIGHT, padx=30, pady=20)
        
        # Random Button
        tk.Button(
            actions_frame,
            text="🎲 Random",
            command=self.fetch_random_wallpaper,
            bg=self.colors['accent_blue'],
            fg='white',
            font=self.fonts['button'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Folder Button
        tk.Button(
            actions_frame,
            text="📁 Local",
            command=self.open_wallpapers_folder,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=self.fonts['button'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Status Label
        self.status_label = tk.Label(
            actions_frame,
            text="● Ready",
            font=self.fonts['body'],
            bg=self.colors['hero_bg'],
            fg=self.colors['success_green']
        )
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # ===== MAIN SECTION (85% height) =====
        main_section = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_section.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        # ==== LEFT PANEL (40%) ====
        left_panel = tk.Frame(main_section, bg=self.colors['bg_secondary'], width=560)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        left_panel.pack_propagate(False)
        
        # --- TOP: Preview Section (60% of left panel) ---
        preview_section = tk.Frame(left_panel, bg='black', height=357)  # 60% of 595
        preview_section.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        preview_section.pack_propagate(False)
        
        # Preview Canvas
        self.preview_canvas = tk.Canvas(
            preview_section,
            bg='#000000',
            highlightthickness=2,
            highlightbackground=self.colors['border']
        )
        self.preview_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Resolution Badge (overlay on canvas)
        self.resolution_label = tk.Label(
            self.preview_canvas,
            text="1920×1080",
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary'],
            font=self.fonts['small'],
            padx=10,
            pady=5
        )
        
        # Quote Overlay Frame (bottom of canvas)
        self.quote_frame = tk.Frame(self.preview_canvas, bg='#000000', height=60)
        
        self.quote_text = tk.Label(
            self.quote_frame,
            text='"Change your wallpaper, change your mood"',
            fg=self.colors['text_primary'],
            bg='#000000',
            font=self.fonts['quote'],
            wraplength=500,
            justify='left'
        )
        self.quote_text.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Placeholder
        self.placeholder_id = self.preview_canvas.create_text(
            280, 178,
            text="🖼️\n\nLoading wallpaper...",
            font=('Segoe UI', 16),
            fill='#666666',
            justify=tk.CENTER
        )
        
        # --- BOTTOM: Controls Section (40% of left panel) ---
        controls_section = tk.Frame(left_panel, bg=self.colors['bg_secondary'])
        controls_section.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        # History Section
        history_label = tk.Label(
            controls_section,
            text="Recent History",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=self.fonts['heading'],
            anchor='w'
        )
        history_label.pack(fill=tk.X, padx=15, pady=(10, 5))
        
        # History thumbnails (horizontal scrollable)
        history_canvas = tk.Canvas(
            controls_section,
            bg=self.colors['bg_secondary'],
            height=90,
            highlightthickness=0
        )
        history_canvas.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.history_container = tk.Frame(history_canvas, bg=self.colors['bg_secondary'])
        history_canvas.create_window((0, 0), window=self.history_container, anchor='nw')
        
        # URL Fetch Section
        url_label = tk.Label(
            controls_section,
            text="IMAGE URL",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_muted'],
            font=self.fonts['small'],
            anchor='w'
        )
        url_label.pack(fill=tk.X, padx=15, pady=(5, 3))
        
        self.url_entry = tk.Entry(
            controls_section,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=self.fonts['body'],
            relief=tk.FLAT,
            bd=1,
            insertbackground=self.colors['text_primary']
        )
        self.url_entry.pack(fill=tk.X, padx=15, pady=(0, 8))
        self.url_entry.insert(0, "https://picsum.photos/1920/1080")
        
        self.fetch_btn = tk.Button(
            controls_section,
            text="⬇ Fetch Wallpaper",
            command=self.fetch_from_url,
            bg=self.colors['accent_blue'],
            fg='white',
            font=self.fonts['button'],
            relief=tk.FLAT,
            cursor="hand2",
            pady=10
        )
        self.fetch_btn.pack(fill=tk.X, padx=15, pady=(0, 8))
        
        # Browse Local File
        browse_button = tk.Button(
            controls_section,
            text="📁 Browse Local File",
            command=self.browse_file,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=self.fonts['body'],
            relief=tk.FLAT,
            bd=1,
            cursor="hand2",
            pady=10
        )
        browse_button.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # ==== RIGHT PANEL (60%) ====
        right_panel = tk.Frame(main_section, bg=self.colors['bg_primary'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Scrollable container for right panel
        right_canvas = tk.Canvas(right_panel, bg=self.colors['bg_primary'], highlightthickness=0)
        right_scrollbar = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=right_canvas.yview)
        right_content = tk.Frame(right_canvas, bg=self.colors['bg_primary'])
        
        right_content.bind(
            "<Configure>",
            lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all"))
        )
        
        right_canvas.create_window((0, 0), window=right_content, anchor='nw')
        right_canvas.configure(yscrollcommand=right_scrollbar.set)
        
        right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        right_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # --- Wallpaper Type Selector ---
        type_card = tk.LabelFrame(
            right_content,
            text="Wallpaper Themes",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=self.fonts['heading'],
            relief=tk.FLAT,
            bd=10
        )
        type_card.pack(fill=tk.X, padx=20, pady=(15, 15))
        
        # Grid layout: 5 columns x 2 rows
        for idx, (name, value) in enumerate(self.wallpaper_types):
            row = idx // 5
            col = idx % 5
            
            type_button = tk.Radiobutton(
                type_card,
                text=name,
                variable=self.selected_type,
                value=value,
                bg=self.colors['bg_tertiary'],
                fg=self.colors['text_secondary'],
                selectcolor=self.colors['accent_blue'],
                font=self.fonts['body'],
                relief=tk.FLAT,
                indicatoron=False,
                width=11,
                height=2,
                cursor='hand2',
                activebackground=self.colors['bg_hover']
            )
            type_button.grid(row=row, column=col, padx=4, pady=4, sticky='ew')
        
        # --- Auto-Rotation Settings ---
        rotation_card = tk.LabelFrame(
            right_content,
            text="Auto-Rotation",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=self.fonts['heading'],
            relief=tk.FLAT,
            bd=10
        )
        rotation_card.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Toggle & Interval
        toggle_frame = tk.Frame(rotation_card, bg=self.colors['bg_secondary'])
        toggle_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.auto_rotate_var = tk.BooleanVar(value=False)
        toggle_check = ttk.Checkbutton(
            toggle_frame,
            text="Enable Auto-Rotate",
            variable=self.auto_rotate_var,
            command=self.toggle_auto_rotate
        )
        toggle_check.pack(side=tk.LEFT)
        
        tk.Label(
            toggle_frame,
            text="Interval:",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            font=self.fonts['body']
        ).pack(side=tk.LEFT, padx=(20, 5))
        
        self.interval_entry = tk.Entry(
            toggle_frame,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=self.fonts['body'],
            width=6,
            relief=tk.FLAT
        )
        self.interval_entry.insert(0, "60")
        self.interval_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            toggle_frame,
            text="min",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            font=self.fonts['small']
        ).pack(side=tk.LEFT, padx=5)
        
        apply_btn = tk.Button(
            toggle_frame,
            text="Apply",
            command=self.apply_interval,
            bg=self.colors['accent_blue'],
            fg='white',
            font=self.fonts['button'],
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=5
        )
        apply_btn.pack(side=tk.LEFT, padx=10)
        
        # Timer display
        self.timer_label = tk.Label(
            rotation_card,
            text="Next change: --:--",
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_blue'],
            font=self.fonts['subheading']
        )
        self.timer_label.pack(pady=(0, 10))
        
        # --- Current Wallpaper Info ---
        current_card = tk.LabelFrame(
            right_content,
            text="Current Wallpaper",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=self.fonts['heading'],
            relief=tk.FLAT,
            bd=10
        )
        current_card.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        self.current_text = tk.Text(
            current_card,
            height=4,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_secondary'],
            font=self.fonts['body'],
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.current_text.pack(fill=tk.X, padx=10, pady=10)
        self.current_text.insert(1.0, "No wallpaper set yet")
        self.current_text.config(state=tk.DISABLED)
        
        # --- Favorites (Horizontal Scrollable) ---
        favorites_card = tk.LabelFrame(
            right_content,
            text="❤️ Favorites",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=self.fonts['heading'],
            relief=tk.FLAT,
            bd=10
        )
        favorites_card.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        fav_canvas = tk.Canvas(
            favorites_card,
            bg=self.colors['bg_secondary'],
            height=100,
            highlightthickness=0
        )
        fav_canvas.pack(fill=tk.X, padx=10, pady=10)
        
        self.favorites_container = tk.Frame(fav_canvas, bg=self.colors['bg_secondary'])
        fav_canvas.create_window((0, 0), window=self.favorites_container, anchor='nw')
        
        # --- Primary Action Buttons ---
        action_frame = tk.Frame(right_content, bg=self.colors['bg_primary'])
        action_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.set_button = tk.Button(
            action_frame,
            text="✓ Set Wallpaper",
            command=self.set_wallpaper,
            state=tk.DISABLED,
            bg=self.colors['success_green'],
            fg='white',
            font=('Segoe UI', 14, 'bold'),
            relief=tk.FLAT,
            cursor='hand2',
            height=2
        )
        self.set_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.favorite_button = tk.Button(
            action_frame,
            text="❤️",
            command=self.add_to_favorites,
            state=tk.DISABLED,
            bg=self.colors['warning_yellow'],
            fg='white',
            font=('Segoe UI', 18),
            relief=tk.FLAT,
            cursor='hand2',
            width=4,
            height=2
        )
        self.favorite_button.pack(side=tk.RIGHT)
        
        # Progress bar (initially hidden)
        self.progress = ttk.Progressbar(
            right_content,
            mode='indeterminate',
            length=200
        )
        
        # Store additional widgets that will be referenced
        self.preview_size_label = self.resolution_label
        self.file_entry = self.url_entry  # Reuse URL entry for file path display
        self.auto_fetch_btn = self.fetch_btn  # Can be extended later
