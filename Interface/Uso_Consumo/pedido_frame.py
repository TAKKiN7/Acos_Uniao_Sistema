import customtkinter as ctk
from tkinter import messagebox

class PedidoFrame(ctk.CTkFrame):
    """
    Frame individual para operação de Pedido no módulo de Uso e Consumo.
    Contém um campo (CTkEntry) para leitura/digitação da chave e botão INICIAR.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)

        # Card Principal da Operação
        self.card = ctk.CTkFrame(
            self,
            fg_color=("#F0F4F8", "#1E2228"),
            border_color=("#94A3B8", "#2D323E"),
            border_width=1,
            corner_radius=12
        )
        self.card.grid(row=0, column=0, sticky="ew", padx=0, pady=10)
        self.card.grid_columnconfigure(0, weight=1)

        # Título da Operação
        self.lbl_titulo = ctk.CTkLabel(
            self.card,
            text="📋  GESTÃO DE PEDIDOS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_titulo.pack(anchor="w", padx=25, pady=(20, 5))

        self.lbl_desc = ctk.CTkLabel(
            self.card,
            text="Digite ou bipe a chave de acesso correspondente ao pedido de uso e consumo.",
            font=ctk.CTkFont(size=12),
            text_color=("#475569", "#9CA3AF")
        )
        self.lbl_desc.pack(anchor="w", padx=25, pady=(0, 20))

        # Divisor
        self.div = ctk.CTkFrame(self.card, height=1, fg_color=("#CBD5E1", "#2D323E"))
        self.div.pack(fill="x", padx=25, pady=(0, 20))

        # Label do Campo de Chave
        self.lbl_chave = ctk.CTkLabel(
            self.card,
            text="CHAVE DE ACESSO DO PEDIDO",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        self.lbl_chave.pack(anchor="w", padx=25, pady=(0, 6))

        # Entry para leitura/digitação da chave
        self.entry_chave = ctk.CTkEntry(
            self.card,
            placeholder_text="🔑  Digite ou bipe a chave de acesso (44 dígitos)...",
            font=ctk.CTkFont(size=13),
            fg_color=("#E2E8F0", "#14171C"),
            border_color=("#94A3B8", "#2D323E"),
            text_color=("#0F172A", "#FFFFFF"),
            placeholder_text_color=("#475569", "#6B7280"),
            height=45,
            corner_radius=8
        )
        self.entry_chave.pack(fill="x", padx=25, pady=(0, 20))

        # Botão Iniciar
        self.btn_iniciar = ctk.CTkButton(
            self.card,
            text="INICIAR  ▶",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            height=45,
            corner_radius=8,
            command=self.iniciar_processamento
        )
        self.btn_iniciar.pack(fill="x", padx=25, pady=(0, 25))

    def iniciar_processamento(self):
        chave = self.entry_chave.get().strip()
        if not chave:
            messagebox.showwarning("Chave Não Informada", "Por favor, digite ou bipe a chave de acesso do pedido.")
        else:
            messagebox.showinfo("Pedido Iniciado", f"Processamento do Pedido iniciado com sucesso!\nChave: {chave}")
