import customtkinter as ctk
from tkinter import messagebox
from threading import Thread
from Interface.Materia_Prima.Functions.nota_entrada_gerdau import gerdau_start

class GerdauFrame(ctk.CTkFrame):
    """
    Frame específico para a Usina GERDAU.
    Contém 1 campo (Chave de Acesso) e 1 botão Iniciar.
    """
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=("#F0F4F8", "#1E2228"),
            border_color=("#94A3B8", "#2D323E"),
            border_width=1,
            corner_radius=12
        )

        self.grid_columnconfigure(0, weight=1)

        # Cabeçalho da Usina Selecionada
        self.header_box = ctk.CTkFrame(self, fg_color=("#E2E8F0", "#171A1F"), corner_radius=8)
        self.header_box.pack(fill="x", padx=25, pady=(20, 15))

        self.lbl_usina_title = ctk.CTkLabel(
            self.header_box,
            text="🏭  USINA SELECIONADA: GERDAU",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#1D4ED8", "#60A5FA")
        )
        self.lbl_usina_title.pack(anchor="w", padx=15, pady=10)

        # Campo 1: Chave de Acesso da Nota
        self.lbl_chave = ctk.CTkLabel(
            self.header_box,
            text="CHAVE DE ACESSO DA NOTA",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        self.lbl_chave.pack(anchor="w", padx=15, pady=(5, 4))

        self.entry_chave = ctk.CTkEntry(
            self.header_box,
            placeholder_text="Digite a chave de acesso (44 dígitos)...",
            font=ctk.CTkFont(size=13),
            fg_color=("#FFFFFF", "#14171C"),
            border_color=("#94A3B8", "#2D323E"),
            text_color=("#0F172A", "#FFFFFF"),
            placeholder_text_color=("#64748B", "#6B7280"),
            height=42,
            corner_radius=8
        )
        self.entry_chave.pack(fill="x", padx=15, pady=(0, 20))

        # Botão Iniciar Lançamento GERDAU
        self.btn_iniciar = ctk.CTkButton(
            self,
            text="INICIAR LANÇAMENTO GERDAU  ▶",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            height=45,
            corner_radius=8,
            command=self.processar_gerdau
        )
        self.btn_iniciar.pack(fill="x", padx=25, pady=(0, 20))

        self.entry_chave.bind("<Return>", self.processar_gerdau)
        self.entry_chave.bind("<KP_Enter>", self.processar_gerdau)
        self.entry_chave.focus_set()

    def processar_gerdau(self, e=None):
        chave = self.entry_chave.get().strip()

        if not chave:
            messagebox.showwarning("Campo Vazio", "Por favor, preencha a chave de acesso da Nota GERDAU.")
            return

        self.btn_iniciar.configure(
            text="⏳ LANÇAMENTO EM ANDAMENTO...",
            fg_color="#D97706",
            hover_color="#B45309",
            state="disabled"
        )

        def runner():
            try:
                gerdau_start(chave)
            finally:
                self.after(0, lambda: self.btn_iniciar.configure(
                    text="INICIAR LANÇAMENTO GERDAU  ▶",
                    fg_color="#1D4ED8",
                    hover_color="#1E40AF",
                    state="normal"
                ))

        Thread(target=runner, daemon=True).start()
