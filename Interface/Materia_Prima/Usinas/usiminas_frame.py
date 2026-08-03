import customtkinter as ctk
from tkinter import messagebox
from Interface.Materia_Prima.Functions.nota_entrada_usiminas import usiminas_start



class UsiminasFrame(ctk.CTkFrame):
    """
    Frame específico para a Usina USIMINAS.
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
            text="🏭  USINA SELECIONADA: USIMINAS",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#EA580C", "#FF7A00")
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

        # Botão Iniciar Lançamento USIMINAS
        self.btn_iniciar = ctk.CTkButton(
            self,
            text="INICIAR LANÇAMENTO USIMINAS  ▶",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#EA580C",
            hover_color="#C2410C",
            text_color="#FFFFFF",
            height=45,
            corner_radius=8,
            command=self.processar_usiminas
        )
        self.btn_iniciar.pack(fill="x", padx=25, pady=(0, 20))
        self.entry_chave.bind("<Return>", lambda event: self.processar_usiminas())

    def processar_usiminas(self):
        chave = self.entry_chave.get().strip()

        if not chave:
            messagebox.showwarning("Campo Vazio", "Por favor, preencha a chave de acesso da Nota USIMINAS.")
        else:
            #messagebox.showinfo("Lançamento USIMINAS", f"Processando USIMINAS:\n• Chave: {chave}")
            usiminas_start(chave)
            