import customtkinter as ctk
from tkinter import messagebox
from threading import Thread
from Interface.Materia_Prima.Usinas.baixar_anexos import baixar_anexos, baixar_xml




# Importação dos frames de cada usina
from Interface.Materia_Prima.Usinas.aperam_frame import AperamFrame
from Interface.Materia_Prima.Usinas.usiminas_frame import UsiminasFrame
from Interface.Materia_Prima.Usinas.gerdau_frame import GerdauFrame

class MateriaPrimaFrame(ctk.CTkFrame):
    """
    Frame referente à aba 'Notas de Matéria-Prima'.
    Contém as opções de seleção de fornecedores (APERAM, USIMINAS, GERDAU),
    o card 'Baixar Anexos/XML' com caixa de entrada para chave de acesso e opção 'Somente XML',
    e o formulário da usina selecionada.
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
        self.card_panel.grid(row=1, column=0, sticky="ew", padx=30, pady=(10, 10))
        self.card_panel.grid_columnconfigure((0, 1, 2), weight=1)

        # Instrução
        self.lbl_instrucao = ctk.CTkLabel(
            self.card_panel,
            text="SELECIONE O FORNECEDOR PARA LANÇAMENTO",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#1E293B", "#9CA3AF")
        )
        self.lbl_instrucao.grid(row=0, column=0, columnspan=3, pady=(15, 10))

        # Botões de Seleção das Usinas
        # 1. APERAM
        self.btn_aperam = ctk.CTkButton(
            self.card_panel,
            text="🏭  APERAM",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            height=42,
            corner_radius=8,
            command=lambda: self.selecionar_usina("APERAM")
        )
        self.btn_aperam.grid(row=1, column=0, padx=(20, 10), pady=(0, 15), sticky="ew")

        # 2. USIMINAS
        self.btn_usiminas = ctk.CTkButton(
            self.card_panel,
            text="🏭  USIMINAS",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#EA580C",
            hover_color="#C2410C",
            text_color="#FFFFFF",
            height=42,
            corner_radius=8,
            command=lambda: self.selecionar_usina("USIMINAS")
        )
        self.btn_usiminas.grid(row=1, column=1, padx=10, pady=(0, 15), sticky="ew")

        # 3. GERDAU
        self.btn_gerdau = ctk.CTkButton(
            self.card_panel,
            text="🏭  GERDAU",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            height=42,
            corner_radius=8,
            command=lambda: self.selecionar_usina("GERDAU")
        )
        self.btn_gerdau.grid(row=1, column=2, padx=(10, 20), pady=(0, 15), sticky="ew")

        # 3. Card Secundário: Botão "Baixar Anexos/XML"
        self.card_anexos = ctk.CTkFrame(
            self,
            fg_color=("#F0F4F8", "#1E2228"),
            border_color=("#94A3B8", "#2D323E"),
            border_width=1,
            corner_radius=12
        )
        self.card_anexos.grid(row=2, column=0, sticky="ew", padx=30, pady=(0, 10))
        self.card_anexos.grid_columnconfigure(0, weight=1)

        # Botão "Baixar Anexos/XML"
        self.btn_baixar_anexos = ctk.CTkButton(
            self.card_anexos,
            text="📥  Baixar Anexos/XML",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#0052FF",
            hover_color="#003EB8",
            text_color="#FFFFFF",
            height=40,
            corner_radius=8,
            command=self.toggle_frame_anexos
        )
        self.btn_baixar_anexos.pack(fill="x", padx=15, pady=10)

        # Frame que abre ao clicar no botão, contendo o entry para a chave de acesso e checkbox
        self.frame_busca_xml = ctk.CTkFrame(self.card_anexos, fg_color="transparent")

        # Rótulo explicativo para destaque visual
        self.lbl_chave_anexo = ctk.CTkLabel(
            self.frame_busca_xml,
            text="🔑  CHAVE DE ACESSO DA NOTA FISCAL (NFe / XML)",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#1D4ED8", "#60A5FA")
        )
        self.lbl_chave_anexo.pack(anchor="w", padx=5, pady=(0, 4))

        # Caixa de texto (Entry) com borda azul destacada e altura 44px
        self.entry_chave_xml = ctk.CTkEntry(
            self.frame_busca_xml,
            placeholder_text="Digite ou bipe a chave de acesso (44 dígitos) e pressione Enter...",
            font=ctk.CTkFont(size=13),
            fg_color=("#FFFFFF", "#14171C"),
            border_color=("#2563EB", "#3B82F6"),
            border_width=2,
            text_color=("#0F172A", "#FFFFFF"),
            placeholder_text_color=("#64748B", "#94A3B8"),
            height=44,
            corner_radius=8
        )
        self.entry_chave_xml.pack(fill="x", padx=5, pady=(0, 10))
        self.entry_chave_xml.bind("<Return>", lambda event: self.buscar_anexos_xml())

        # Checkbox "Somente XML"
        self.chk_somente_xml = ctk.CTkCheckBox(
            self.frame_busca_xml,
            text="Somente XML",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#0F172A", "#E2E8F0"),
            checkbox_width=20,
            checkbox_height=20,
            corner_radius=4,
            fg_color="#0052FF",
            hover_color="#003EB8"
        )
        self.chk_somente_xml.pack(anchor="w", padx=5, pady=(0, 10))

        # Botão Ação Download
        self.btn_executar_download = ctk.CTkButton(
            self.frame_busca_xml,
            text="📥  INICIAR DOWNLOAD DE ANEXOS/XML",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#0052FF",
            hover_color="#003EB8",
            text_color="#FFFFFF",
            height=40,
            corner_radius=8,
            command=self.buscar_anexos_xml
        )
        self.btn_executar_download.pack(fill="x", padx=5, pady=(0, 10))

        # 4. Dynamic Sub-Container onde os frames das usinas são carregados
        self.usinas_container = ctk.CTkFrame(self, fg_color="transparent")
        self.usinas_container.grid(row=3, column=0, sticky="ew", padx=30, pady=(0, 15))
        self.usinas_container.grid_columnconfigure(0, weight=1)

        # Dicionário de armazenamentos dos frames das usinas
        self.usina_frames = {}
        self.inicializar_frames_usinas()

        # Por padrão, abre o formulário da Aperam
        self.selecionar_usina("APERAM")

    def toggle_frame_anexos(self):
        """Alterna a exibição do frame que contém o entry para a chave de acesso."""
        if self.frame_busca_xml.winfo_ismapped():
            self.frame_busca_xml.pack_forget()
        else:
            self.frame_busca_xml.pack(fill="x", padx=15, pady=(0, 10))
            self.entry_chave_xml.focus_set()

    def buscar_anexos_xml(self):
        """Ação disparada ao pressionar Enter na caixa da chave de acesso ou clicar no botão."""
        chave = self.entry_chave_xml.get().strip()
        somente_xml = bool(self.chk_somente_xml.get())
        if not chave:
            messagebox.showwarning("Chave Não Informada", "Por favor, digite ou bipe a chave de acesso da nota.")
            return

        # Impede chamadas simultâneas se já estiver baixando
        if getattr(self, "_downloading", False):
            return

        self._downloading = True
        self.btn_executar_download.configure(
            text="⏳ BAIXANDO ANEXOS NO OUTLOOK...",
            fg_color="#D97706",
            hover_color="#B45309",
            state="disabled"
        )
        self.btn_baixar_anexos.configure(state="disabled")

        def runner():
            try:
                if not somente_xml:
                    baixar_anexos(chave)
                else:
                    baixar_xml(chave)
            finally:
                def reset_ui():
                    self._downloading = False
                    self.btn_executar_download.configure(
                        text="📥  INICIAR DOWNLOAD DE ANEXOS/XML",
                        fg_color="#0052FF",
                        hover_color="#003EB8",
                        state="normal"
                    )
                    self.btn_baixar_anexos.configure(state="normal")
                    messagebox.showinfo("Download Concluído", f"Busca e download concluídos para a chave:\n{chave}")

                self.after(0, reset_ui)

        Thread(target=runner, daemon=True).start()

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
