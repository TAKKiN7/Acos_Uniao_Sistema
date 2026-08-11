import subprocess
import os
import customtkinter as ctk
from tkinter import messagebox


class TiFrame(ctk.CTkFrame):
    """
    Frame do Módulo de TI do Sistema AÇOS UNIÃO MANAGER.
    Exibe um painel de cards com atalhos para os principais programas e utilitários do Windows.
    """
    COR_CARD_BG = ("#F0F4F8", "#1E2228")
    COR_CARD_BORDER = ("#94A3B8", "#2D323E")

    FERRAMENTAS = [
        {
            "id": "mstsc",
            "titulo": "🖥️  Área de Trabalho Remota",
            "comando": "mstsc.exe",
            "desc": "Conexão de Área de Trabalho Remota (MSTSC) para acesso a servidores e estações.",
            "badge": "mstsc.exe",
            "shell": False
        },
        {
            "id": "taskmgr",
            "titulo": "📊  Gerenciador de Tarefas",
            "comando": "taskmgr.exe",
            "desc": "Monitoramento de processos em execução, uso de CPU, memória e desempenho.",
            "badge": "taskmgr.exe",
            "shell": False
        },
        {
            "id": "diskmgmt",
            "titulo": "💾  Gerenciador de Disco",
            "comando": "diskmgmt.msc",
            "desc": "Gerenciamento de partições de disco, volumes, formatação e alocação de armazenamento.",
            "badge": "diskmgmt.msc",
            "shell": True
        },
        {
            "id": "printers",
            "titulo": "🖨️  Scanners e Impressoras",
            "comando": "control printers",
            "desc": "Visualização e configuração de impressoras, scanners e dispositivos de impressão.",
            "badge": "control printers",
            "shell": True
        },
        {
            "id": "ncpa",
            "titulo": "🌐  Conexões de Rede",
            "comando": "ncpa.cpl",
            "desc": "Gerenciamento de adaptadores de rede, endereços IP, conexões Ethernet e Wi-Fi.",
            "badge": "ncpa.cpl",
            "shell": True
        },
        {
            "id": "msinfo",
            "titulo": "💻  Informações do Sistema",
            "comando": "msinfo32.exe",
            "desc": "Relatório detalhado sobre hardware, componentes, drivers e sistema operacional.",
            "badge": "msinfo32.exe",
            "shell": False
        },
        {
            "id": "control",
            "titulo": "⚙️  Painel de Controle",
            "comando": "control.exe",
            "desc": "Acesso rápido às configurações clássicas e ferramentas administrativas do Windows.",
            "badge": "control.exe",
            "shell": False
        },
        {
            "id": "cmd",
            "titulo": "⌨️  Prompt de Comando",
            "comando": "cmd.exe",
            "desc": "Abre o terminal de linha de comando do Windows (CMD).",
            "badge": "cmd.exe / start",
            "shell": True,
            "custom_cmd": "start cmd.exe"
        }
    ]

    def __init__(self, parent, usuario_logado="Operador Sistema", dados_usuario=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.usuario_logado = usuario_logado
        self.dados_usuario = dados_usuario or {}

        # Configuração do Grid Principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Cabeçalho do Módulo
        self._criar_header()

        # 2. Área de Cards Responsiva (Scrollable)
        self._criar_area_cards()

    def _criar_header(self):
        """Cria o cabeçalho superior da aba de TI."""
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 15))

        self.lbl_modulo = ctk.CTkLabel(
            self.header_frame,
            text="TECNOLOGIA DA INFORMAÇÃO & SUPORTE",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        self.lbl_modulo.pack(anchor="w")

        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame,
            text="Módulo TI • Utilitários do Windows",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_titulo.pack(anchor="w", pady=(2, 0))

    def _criar_area_cards(self):
        """Cria um frame rolável com a grade de cards das ferramentas de TI."""
        self.scroll_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        self.scroll_container.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.scroll_container.grid_columnconfigure((0, 1), weight=1)

        for index, item in enumerate(self.FERRAMENTAS):
            linha = index // 2
            coluna = index % 2
            self._criar_card_ferramenta(self.scroll_container, item, linha, coluna)

    def _criar_card_ferramenta(self, parent, item, linha, coluna):
        """Constrói o card individual de uma ferramenta do Windows."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.COR_CARD_BG,
            border_color=self.COR_CARD_BORDER,
            border_width=1,
            corner_radius=12
        )
        card.grid(row=linha, column=coluna, sticky="nsew", padx=10, pady=10)
        card.grid_columnconfigure(0, weight=1)

        # Cabeçalho do Card
        card_header = ctk.CTkFrame(card, fg_color="transparent")
        card_header.pack(fill="x", padx=18, pady=(15, 8))

        lbl_titulo = ctk.CTkLabel(
            card_header,
            text=item["titulo"],
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        lbl_titulo.pack(side="left")

        # Badge do comando
        lbl_badge = ctk.CTkLabel(
            card_header,
            text=f" {item['badge']} ",
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color=("#CBD5E1", "#2D323E"),
            text_color=("#334155", "#94A3B8"),
            corner_radius=4
        )
        lbl_badge.pack(side="right")

        # Divisor
        div = ctk.CTkFrame(card, height=1, fg_color=self.COR_CARD_BORDER)
        div.pack(fill="x", padx=18, pady=(0, 10))

        # Descrição da ferramenta
        lbl_desc = ctk.CTkLabel(
            card,
            text=item["desc"],
            font=ctk.CTkFont(size=12),
            text_color=("#475569", "#94A3B8"),
            justify="left",
            wraplength=380
        )
        lbl_desc.pack(anchor="w", padx=18, pady=(0, 15))

        # Botão de Ação para Executar
        btn_abrir = ctk.CTkButton(
            card,
            text="▶️  ABRIR PROGRAMA",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            height=38,
            corner_radius=8,
            command=lambda i=item: self._executar_ferramenta(i)
        )
        btn_abrir.pack(anchor="e", padx=18, pady=(0, 15))

    def _executar_ferramenta(self, item):
        """Executa a ferramenta do Windows sem congelar a interface gráfica."""
        comando = item.get("custom_cmd", item["comando"])
        usar_shell = item.get("shell", False)

        try:
            if usar_shell or " " in comando or comando.endswith(".msc") or comando.endswith(".cpl"):
                # Para utilitários do painel de controle (.msc, .cpl) ou atalhos com argumentos
                subprocess.Popen(f"start {comando}", shell=True)
            else:
                subprocess.Popen([comando])
        except Exception as e:
            # Tenta fallback via os.system("start ...")
            try:
                os.system(f"start {comando}")
            except Exception as ex2:
                messagebox.showerror(
                    "Erro ao Abrir Programa",
                    f"Não foi possível iniciar a ferramenta '{item['titulo']}':\n\n{e}"
                )
