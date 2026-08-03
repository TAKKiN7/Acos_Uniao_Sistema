import customtkinter as ctk

from Interface.Uso_Consumo.pedido_frame import PedidoFrame
from Interface.Uso_Consumo.cadastrar_produtos_frame import CadastrarProdutosFrame
from Interface.Uso_Consumo.lancar_nota_frame import LancarNotaFrame

class UsoConsumoFrame(ctk.CTkFrame):
    """
    Frame principal do módulo 'Notas de Uso e Consumo'.
    Contém 3 botões de navegação: Pedido, Cadastrar Produtos e Lançar Nota.
    Exibe dinamicamente o frame individual da operação selecionada.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)

        # 1. Header Section
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 10))

        self.lbl_modulo = ctk.CTkLabel(
            self.header_frame,
            text="SUPRIMENTOS & ESTOQUE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        self.lbl_modulo.pack(anchor="w")

        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame,
            text="Notas de Uso e Consumo",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_titulo.pack(anchor="w", pady=(2, 0))

        # 2. Card Panel com os 3 Botões de Seleção
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
            text="SELECIONE A OPERAÇÃO DESEJADA",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#1E293B", "#9CA3AF")
        )
        self.lbl_instrucao.grid(row=0, column=0, columnspan=3, pady=(20, 15))

        # Botão 1: Pedido
        self.btn_pedido = ctk.CTkButton(
            self.card_panel,
            text="📋  PEDIDO",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            height=45,
            corner_radius=8,
            command=lambda: self.selecionar_operacao("pedido")
        )
        self.btn_pedido.grid(row=1, column=0, padx=(30, 10), pady=(0, 20), sticky="ew")

        # Botão 2: Cadastrar Produtos
        self.btn_cadastrar = ctk.CTkButton(
            self.card_panel,
            text="🏷️  CADASTRAR PRODUTOS",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            height=45,
            corner_radius=8,
            command=lambda: self.selecionar_operacao("cadastrar_produtos")
        )
        self.btn_cadastrar.grid(row=1, column=1, padx=10, pady=(0, 20), sticky="ew")

        # Botão 3: Lançar Nota
        self.btn_lancar = ctk.CTkButton(
            self.card_panel,
            text="📄  LANÇAR NOTA",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#EA580C",
            hover_color="#C2410C",
            text_color="#FFFFFF",
            height=45,
            corner_radius=8,
            command=lambda: self.selecionar_operacao("lancar_nota")
        )
        self.btn_lancar.grid(row=1, column=2, padx=(10, 30), pady=(0, 20), sticky="ew")

        # 3. Dynamic Sub-Container onde os frames individuais serão carregados
        self.sub_container = ctk.CTkFrame(self, fg_color="transparent")
        self.sub_container.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.sub_container.grid_columnconfigure(0, weight=1)
        self.sub_container.grid_rowconfigure(0, weight=1)

        # Dicionário de armazenamento dos frames das operações
        self.operacao_frames = {}
        self.inicializar_frames_operacoes()

        # Seleção padrão inicial: Pedido
        self.selecionar_operacao("pedido")

    def inicializar_frames_operacoes(self):
        """Instancia os 3 frames individuais dentro do container."""
        # Frame Pedido
        frame_pedido = PedidoFrame(self.sub_container)
        frame_pedido.grid(row=0, column=0, sticky="nsew")
        self.operacao_frames["pedido"] = frame_pedido

        # Frame Cadastrar Produtos
        frame_cadastrar = CadastrarProdutosFrame(self.sub_container)
        frame_cadastrar.grid(row=0, column=0, sticky="nsew")
        self.operacao_frames["cadastrar_produtos"] = frame_cadastrar

        # Frame Lançar Nota
        frame_lancar = LancarNotaFrame(self.sub_container)
        frame_lancar.grid(row=0, column=0, sticky="nsew")
        self.operacao_frames["lancar_nota"] = frame_lancar

    def selecionar_operacao(self, chave_operacao):
        """Alterna a exibição do frame individual e destaca o botão selecionado."""
        if chave_operacao in self.operacao_frames:
            self.operacao_frames[chave_operacao].tkraise()

        botoes = {
            "pedido": (self.btn_pedido, "#1D4ED8"),
            "cadastrar_produtos": (self.btn_cadastrar, "#1D4ED8"),
            "lancar_nota": (self.btn_lancar, "#EA580C")
        }

        for op_key, (btn, color) in botoes.items():
            if op_key == chave_operacao:
                btn.configure(
                    fg_color=color,
                    border_width=3,
                    border_color="#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#0F172A"
                )
            else:
                btn.configure(
                    fg_color=color,
                    border_width=0
                )
