import customtkinter as ctk

class StatusFrame(ctk.CTkFrame):
    """
    Frame Inicial (Status / Home) do Sistema AÇOS UNIÃO MANAGER.
    Exibe a saudação inicial e o card 'Sobre' com informações do sistema.
    """
    COR_CARD_BG = ("#E2E8F0", "#181B20")
    COR_CARD_BORDER = ("#CBD5E1", "#262B34")

    def __init__(self, master, usuario_logado="Operador Sistema", dados_usuario=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.usuario_logado = usuario_logado
        self.dados_usuario = dados_usuario or {}
        self.nome_exibicao = self.dados_usuario.get("nome", usuario_logado)

        # Configuração do Layout do Frame
        self.grid_columnconfigure(0, weight=1)

        # 1. Cabeçalho com Saudação
        self.box_header = ctk.CTkFrame(self, fg_color="transparent")
        self.box_header.grid(row=0, column=0, padx=30, pady=(30, 15), sticky="w")

        lbl_saudacao = ctk.CTkLabel(
            self.box_header,
            text=f"Bem-vindo(a), {self.nome_exibicao}! 👋",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        lbl_saudacao.pack(anchor="w")

        lbl_sub = ctk.CTkLabel(
            self.box_header,
            text="Sistema integrado para auxílio de tarefas • AÇOS UNIÃO",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=("#475569", "#94A3B8")
        )
        lbl_sub.pack(anchor="w", pady=(4, 0))

        # 2. Card Sobre
        self.card_sobre = ctk.CTkFrame(
            self,
            fg_color=self.COR_CARD_BG,
            border_color=self.COR_CARD_BORDER,
            border_width=1,
            corner_radius=12
        )
        self.card_sobre.grid(row=1, column=0, padx=30, pady=10, sticky="ew")
        self.card_sobre.grid_columnconfigure(0, weight=1)

        # Cabeçalho do Card
        header = ctk.CTkFrame(self.card_sobre, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))

        lbl_icon = ctk.CTkLabel(
            header,
            text="ℹ️",
            font=ctk.CTkFont(size=22)
        )
        lbl_icon.pack(side="left", padx=(0, 10))

        lbl_title = ctk.CTkLabel(
            header,
            text="Sobre",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        lbl_title.pack(side="left")

        # Linha divisória
        div = ctk.CTkFrame(self.card_sobre, height=1, fg_color=self.COR_CARD_BORDER)
        div.pack(fill="x", padx=20, pady=(0, 12))

        # Conteúdo do Card
        box_conteudo = ctk.CTkFrame(self.card_sobre, fg_color="transparent")
        box_conteudo.pack(anchor="w", padx=20, pady=(0, 20))

        lbl_criado = ctk.CTkLabel(
            box_conteudo,
            text="• Criado por: Tk",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=("#1E293B", "#E2E8F0")
        )
        lbl_criado.pack(anchor="w", pady=2)

        lbl_versao = ctk.CTkLabel(
            box_conteudo,
            text="• Versão: 1.0",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=("#475569", "#94A3B8")
        )
        lbl_versao.pack(anchor="w", pady=2)

        lbl_desc = ctk.CTkLabel(
            box_conteudo,
            text="• Sistema integrado para auxílio de tarefas e automação de processos.",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=("#64748B", "#64748B")
        )
        lbl_desc.pack(anchor="w", pady=(6, 0))

        # 3. Card de Orientação (Escolha o módulo no menu lateral)
        self.card_orientacao = ctk.CTkFrame(
            self,
            fg_color=self.COR_CARD_BG,
            border_color=self.COR_CARD_BORDER,
            border_width=1,
            corner_radius=12
        )
        self.card_orientacao.grid(row=2, column=0, padx=30, pady=(15, 30), sticky="ew")
        self.card_orientacao.grid_columnconfigure(0, weight=1)

        box_orientacao = ctk.CTkFrame(self.card_orientacao, fg_color="transparent")
        box_orientacao.pack(padx=20, pady=20, fill="x")

        lbl_dica = ctk.CTkLabel(
            box_orientacao,
            text="👈  Para iniciar as operações, escolha um dos módulos no menu lateral à esquerda.",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color="#EA580C"
        )
        lbl_dica.pack(anchor="w")
