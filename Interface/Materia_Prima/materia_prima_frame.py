import customtkinter as ctk

# Importação dos frames de cada usina
from Interface.Materia_Prima.aperam_frame import AperamFrame
from Interface.Materia_Prima.usiminas_frame import UsiminasFrame
from Interface.Materia_Prima.gerdau_frame import GerdauFrame

class MateriaPrimaFrame(ctk.CTkFrame):
    """
    Frame referente à aba 'Notas de Matéria-Prima'.
    Contém as opções de seleção de fornecedores (APERAM, USIMINAS, GERDAU)
    e exibe dinamicamente o frame correspondente à usina selecionada.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)

        # 1. Header Section
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 10))
        
        self.lbl_modulo = ctk.CTkLabel(
            self.header_frame, 
            text="MÓDULO ADMINISTRATIVO", 
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        self.lbl_modulo.pack(anchor="w")

        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame, 
            text="Notas de Matéria-Prima", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_titulo.pack(anchor="w", pady=(2, 0))

        # 2. Main Card Panel (Seleção de Fornecedor)
        self.card_panel = ctk.CTkFrame(
            self,
            fg_color=("#F0F4F8", "#1E2228"),
            border_color=("#94A3B8", "#2D323E"),
            border_width=1,
            corner_radius=12
        )
        self.card_panel.grid(row=1, column=0, sticky="ew", padx=30, pady=(10, 15))
        self.card_panel.grid_columnconfigure((0, 1, 2), weight=1)

        # Instrução
        self.lbl_instrucao = ctk.CTkLabel(
            self.card_panel,
            text="SELECIONE O FORNECEDOR PARA LANÇAMENTO",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#1E293B", "#9CA3AF")
        )
        self.lbl_instrucao.grid(row=0, column=0, columnspan=3, pady=(20, 15))

        # Botões de Seleção das Usinas
        # 1. APERAM
        self.btn_aperam = ctk.CTkButton(
            self.card_panel,
            text="🏭  APERAM",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            height=45,
            corner_radius=8,
            command=lambda: self.selecionar_usina("APERAM")
        )
        self.btn_aperam.grid(row=1, column=0, padx=(30, 10), pady=(0, 20), sticky="ew")

        # 2. USIMINAS
        self.btn_usiminas = ctk.CTkButton(
            self.card_panel,
            text="🏭  USIMINAS",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#EA580C",
            hover_color="#C2410C",
            text_color="#FFFFFF",
            height=45,
            corner_radius=8,
            command=lambda: self.selecionar_usina("USIMINAS")
        )
        self.btn_usiminas.grid(row=1, column=1, padx=10, pady=(0, 20), sticky="ew")

        # 3. GERDAU
        self.btn_gerdau = ctk.CTkButton(
            self.card_panel,
            text="🏭  GERDAU",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            height=45,
            corner_radius=8,
            command=lambda: self.selecionar_usina("GERDAU")
        )
        self.btn_gerdau.grid(row=1, column=2, padx=(10, 30), pady=(0, 20), sticky="ew")

        # 3. Dynamic Sub-Container onde os frames das usinas serão carregados
        self.usinas_container = ctk.CTkFrame(self, fg_color="transparent")
        self.usinas_container.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.usinas_container.grid_columnconfigure(0, weight=1)
        self.usinas_container.grid_rowconfigure(0, weight=1)

        # Dicionário de armazenamentos dos frames das usinas
        self.usina_frames = {}
        self.inicializar_frames_usinas()

        # Por padrão, abre o formulário da Aperam
        self.selecionar_usina("APERAM")

    def inicializar_frames_usinas(self):
        """Instancia os 3 frames individuais de cada usina dentro do container."""
        # Frame APERAM
        frame_aperam = AperamFrame(self.usinas_container)
        frame_aperam.grid(row=0, column=0, sticky="nsew")
        self.usina_frames["APERAM"] = frame_aperam

        # Frame USIMINAS
        frame_usiminas = UsiminasFrame(self.usinas_container)
        frame_usiminas.grid(row=0, column=0, sticky="nsew")
        self.usina_frames["USIMINAS"] = frame_usiminas

        # Frame GERDAU
        frame_gerdau = GerdauFrame(self.usinas_container)
        frame_gerdau.grid(row=0, column=0, sticky="nsew")
        self.usina_frames["GERDAU"] = frame_gerdau

    def selecionar_usina(self, nome_usina):
        """Alterna a exibição do frame da usina e destaca o botão correspondente."""
        # Eleva o frame da usina escolhida
        if nome_usina in self.usina_frames:
            self.usina_frames[nome_usina].tkraise()

        # Atualiza a aparência e destaque dos botões das usinas
        botoes = {
            "APERAM": (self.btn_aperam, "#1D4ED8", "#1E40AF"),
            "USIMINAS": (self.btn_usiminas, "#EA580C", "#C2410C"),
            "GERDAU": (self.btn_gerdau, "#1D4ED8", "#1E40AF")
        }

        for usina_key, (btn, color, hover) in botoes.items():
            if usina_key == nome_usina:
                # Usina Selecionada: Borda destacada e alto brilho
                btn.configure(
                    fg_color=color, 
                    border_width=3, 
                    border_color="#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#0F172A"
                )
            else:
                # Usinas não selecionadas: Aparência padrão sem borda
                btn.configure(
                    fg_color=color, 
                    border_width=0
                )
