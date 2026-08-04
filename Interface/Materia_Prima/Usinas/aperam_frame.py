import customtkinter as ctk
from tkinter import messagebox
from threading import Thread
from Interface.Materia_Prima.Functions.nota_entrada_aperam import aperam_start


class AperamFrame(ctk.CTkFrame):
    """
    Frame específico para a Usina APERAM.
    Contém 2 campos (Quantidade de Lotes e Chave de Acesso) e 1 botão Iniciar.
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
            text="🏭  USINA SELECIONADA: APERAM",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#1D4ED8", "#60A5FA")
        )
        self.lbl_usina_title.pack(anchor="w", padx=15, pady=10)

        # Campo 1: Quantidade de Lotes da Nota
        self.lbl_lotes = ctk.CTkLabel(
            self.header_box,
            text="QUANTIDADE DE LOTES DA NOTA",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        self.lbl_lotes.pack(anchor="w", padx=15, pady=(5, 4))

        self.entry_lotes = ctk.CTkEntry(
            self.header_box,
            placeholder_text="Ex: 5",
            font=ctk.CTkFont(size=13),
            fg_color=("#FFFFFF", "#14171C"),
            border_color=("#94A3B8", "#2D323E"),
            text_color=("#0F172A", "#FFFFFF"),
            placeholder_text_color=("#64748B", "#6B7280"),
            height=42,
            corner_radius=8
        )
        self.entry_lotes.pack(fill="x", padx=15, pady=(0, 15))

        # Campo 2: Chave de Acesso da Nota
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

        # Botão Iniciar Lançamento APERAM
        self.btn_iniciar = ctk.CTkButton(
            self,
            text="INICIAR LANÇAMENTO APERAM  ▶",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            height=45,
            corner_radius=8,
            command=self.processar_aperam
        )
        self.btn_iniciar.pack(fill="x", padx=25, pady=(0, 20))
        self.entry_chave.bind("<Return>", lambda event: self.processar_aperam())
        

    def processar_aperam(self):
        lotes = self.entry_lotes.get().strip()
        chave = self.entry_chave.get().strip()

        if not lotes or not chave:
            messagebox.showwarning("Campos Incompletos", "Por favor, preencha a quantidade de lotes e a chave de acesso da Nota APERAM.")
            return

        self.btn_iniciar.configure(
            text="⏳ LANÇAMENTO EM ANDAMENTO...",
            fg_color="#D97706",
            hover_color="#B45309",
            state="disabled"
        )

        def runner():
            try:
                aperam_start(chave, lotes)
            finally:
                self.after(0, lambda: self.btn_iniciar.configure(
                    text="INICIAR LANÇAMENTO APERAM  ▶",
                    fg_color="#1D4ED8",
                    hover_color="#1E40AF",
                    state="normal"
                ))

        Thread(target=runner, daemon=True).start()