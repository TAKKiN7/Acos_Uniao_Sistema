import customtkinter as ctk
from tkinter import messagebox as msg
from Database.estoque import database

class EditarFrame(ctk.CTkFrame):
    """
    Frame para edição de produtos existentes no Almoxarifado.
    Totalmente integrado via CTkFrame (sem janelas secundárias).
    """
    def __init__(self, parent, values, callback_sucesso=None, callback_cancelar=None):
        super().__init__(
            parent,
            fg_color=("#F0F4F8", "#1E2228"),
            border_color=("#94A3B8", "#2D323E"),
            border_width=1,
            corner_radius=12
        )
        self.values = values
        self.codigo = values[0]
        self.callback_sucesso = callback_sucesso
        self.callback_cancelar = callback_cancelar

        self.grid_columnconfigure(0, weight=1)
        self.criar_layout()

    def criar_layout(self):
        # Cabeçalho do Card
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(20, 10))

        lbl_titulo = ctk.CTkLabel(
            header,
            text=f"✏️  Editar Produto (Cód: {self.codigo})",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        lbl_titulo.pack(side="left")

        # Divisor
        div = ctk.CTkFrame(self, height=1, fg_color=("#CBD5E1", "#2D323E"))
        div.pack(fill="x", padx=25, pady=(0, 15))

        # Form
        form_box = ctk.CTkFrame(self, fg_color="transparent")
        form_box.pack(fill="x", padx=25, pady=(0, 15))
        form_box.grid_columnconfigure(0, weight=3)
        form_box.grid_columnconfigure(1, weight=1)

        # Nome do Produto
        lbl_nome = ctk.CTkLabel(
            form_box,
            text="NOME DO PRODUTO",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        lbl_nome.grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.entry_nome = ctk.CTkEntry(
            form_box,
            font=ctk.CTkFont(size=13),
            fg_color=("#E2E8F0", "#14171C"),
            border_color=("#94A3B8", "#2D323E"),
            text_color=("#0F172A", "#FFFFFF"),
            height=40,
            corner_radius=8
        )
        self.entry_nome.insert(0, str(self.values[1]))
        self.entry_nome.grid(row=1, column=0, sticky="ew", padx=(0, 15))

        # Quantidade em Estoque
        lbl_qtd = ctk.CTkLabel(
            form_box,
            text="QUANTIDADE EM ESTOQUE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        lbl_qtd.grid(row=0, column=1, sticky="w", pady=(0, 4))

        self.entry_qtd = ctk.CTkEntry(
            form_box,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#E2E8F0", "#14171C"),
            border_color=("#0891B2", "#0891B2"),
            text_color=("#0F172A", "#FFFFFF"),
            justify="center",
            height=40,
            corner_radius=8
        )
        self.entry_qtd.insert(0, str(self.values[2]))
        self.entry_qtd.grid(row=1, column=1, sticky="ew")

        # Botões de Ação
        btn_box = ctk.CTkFrame(self, fg_color="transparent")
        btn_box.pack(fill="x", padx=25, pady=(5, 20))
        btn_box.grid_columnconfigure((0, 1), weight=1)

        self.btn_confirmar = ctk.CTkButton(
            btn_box,
            text="✓  Salvar Alterações",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            height=40,
            corner_radius=8,
            command=self.confirmar
        )
        self.btn_confirmar.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.btn_cancelar = ctk.CTkButton(
            btn_box,
            text="✕  Cancelar",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#6B7280",
            hover_color="#4B5563",
            text_color="#FFFFFF",
            height=40,
            corner_radius=8,
            command=self.cancelar
        )
        self.btn_cancelar.grid(row=0, column=1, padx=(8, 0), sticky="ew")

    def confirmar(self):
        produto = self.entry_nome.get().strip()
        quantidade_str = self.entry_qtd.get().strip()

        if not produto:
            msg.showerror("Campo Obrigatório", "Por favor, preencha o Nome do Produto.")
            return

        try:
            qtd = int(quantidade_str)
            if qtd < 0:
                raise ValueError("Quantidade negativa")
        except ValueError:
            msg.showerror("Quantidade Inválida", "A quantidade deve ser um número inteiro maior ou igual a 0.")
            return

        new_values = (produto, qtd, self.codigo)
        database.atualizar_produto(self.codigo, new_values, master=self)

        msg.showinfo("Sucesso", "Produto atualizado com sucesso!")
        if self.callback_sucesso:
            self.callback_sucesso()

    def cancelar(self):
        if self.callback_cancelar:
            self.callback_cancelar()
