import customtkinter as ctk
from tkinter import messagebox as msg
from Database.estoque import database

class EntradaFrame(ctk.CTkFrame):
    """
    Frame para registro de Entrada de Material no Almoxarifado.
    Soma a quantidade informada ao estoque atual do produto.
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
            text=f"📥  Entrada de Material (Cód: {self.codigo})",
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

        # Nome do Produto (Desabilitado)
        lbl_nome = ctk.CTkLabel(
            form_box,
            text="PRODUTO SELECIONADO",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        lbl_nome.grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.entry_nome = ctk.CTkEntry(
            form_box,
            font=ctk.CTkFont(size=13),
            state="disabled",
            fg_color=("#E2E8F0", "#14171C"),
            border_color=("#94A3B8", "#2D323E"),
            text_color=("#475569", "#9CA3AF"),
            height=40,
            corner_radius=8
        )
        self.entry_nome.configure(state="normal")
        self.entry_nome.insert(0, str(self.values[1]))
        self.entry_nome.configure(state="disabled")
        self.entry_nome.grid(row=0, column=0, sticky="ew", padx=(0, 15), pady=(20, 0))

        # Quantidade de Entrada
        lbl_qtd = ctk.CTkLabel(
            form_box,
            text="QUANTIDADE DE ENTRADA",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        lbl_qtd.grid(row=0, column=1, sticky="w", pady=(0, 4))

        self.entry_qtd = ctk.CTkEntry(
            form_box,
            placeholder_text="Qtd",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#E2E8F0", "#14171C"),
            border_color=("#0891B2", "#0891B2"),
            text_color=("#0F172A", "#FFFFFF"),
            justify="center",
            height=40,
            corner_radius=8
        )
        self.entry_qtd.grid(row=0, column=1, sticky="ew", pady=(20, 0))
        self.entry_qtd.focus_set()

        # Botões de Ação
        btn_box = ctk.CTkFrame(self, fg_color="transparent")
        btn_box.pack(fill="x", padx=25, pady=(5, 20))
        btn_box.grid_columnconfigure((0, 1), weight=1)

        self.btn_confirmar = ctk.CTkButton(
            btn_box,
            text="✓  Confirmar Entrada",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#0891B2",
            hover_color="#0E7490",
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
        quantidade_str = self.entry_qtd.get().strip()

        try:
            qtd_entrada = int(quantidade_str)
            if qtd_entrada <= 0:
                raise ValueError("Quantidade deve ser maior que zero")
        except ValueError:
            msg.showerror("Quantidade Inválida", "Informe uma quantidade de entrada válida maior que zero.")
            return

        item = database.consultar_produto_codigo(self.codigo, master=self)
        if not item:
            msg.showerror("Erro", "Produto não encontrado no banco de dados!")
            return

        quantidade_atual = int(item[-1])
        quantidade_nova = quantidade_atual + qtd_entrada

        produto_nome = str(self.values[1])
        new_values = (produto_nome, quantidade_nova, self.codigo)

        database.atualizar_produto(self.codigo, new_values, master=self)
        msg.showinfo("Entrada Realizada", f"Entrada de {qtd_entrada} unidades registrada!\nNovo estoque: {quantidade_nova}")
        
        if self.callback_sucesso:
            self.callback_sucesso()

    def cancelar(self):
        if self.callback_cancelar:
            self.callback_cancelar()
