import customtkinter as ctk
import datetime

class StatusFrame(ctk.CTkFrame):
    """
    Frame Inicial (Status / Home) do Sistema AÇOS UNIÃO MANAGER.
    Exibido logo após o login como tela de boas-vindas e resumo do sistema.
    """
    COR_LARANJA = "#EA580C"
    COR_AZUL = "#0052FF"
    COR_CARD_BG = ("#E2E8F0", "#181B20")
    COR_CARD_BORDER = ("#CBD5E1", "#262B34")

    def __init__(self, master, usuario_logado="Operador Sistema", dados_usuario=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.usuario_logado = usuario_logado
        self.dados_usuario = dados_usuario or {}
        
        self.nome_exibicao = self.dados_usuario.get("nome", usuario_logado)
        self.perfil = self.dados_usuario.get("perfil", "operador").upper()
        self.modulos = self.dados_usuario.get("modulos", [])

        # Configuração do Layout do Frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Construção dos Componentes Visuais
        self._criar_banner_boas_vindas()
        self._criar_cards_resumo()
        self._criar_rodape_orientacao()

    def _criar_banner_boas_vindas(self):
        """Banner principal de recepção com nome do usuário e badge de perfil."""
        banner = ctk.CTkFrame(
            self,
            fg_color=self.COR_CARD_BG,
            border_color=self.COR_CARD_BORDER,
            border_width=1,
            corner_radius=12
        )
        banner.grid(row=0, column=0, padx=25, pady=(25, 15), sticky="ew")
        banner.grid_columnconfigure(0, weight=1)

        # Container do texto do banner
        box_texto = ctk.CTkFrame(banner, fg_color="transparent")
        box_texto.pack(side="left", padx=25, pady=20, fill="x", expand=True)

        # Título de Boas-Vindas
        lbl_saudacao = ctk.CTkLabel(
            box_texto,
            text=f"Bem-vindo(a), {self.nome_exibicao}! 👋",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        lbl_saudacao.pack(anchor="w")

        # Subtítulo informativo
        lbl_sub = ctk.CTkLabel(
            box_texto,
            text="Sistema Integrado de Gerenciamento e Controle de Produção • AÇOS UNIÃO",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=("#475569", "#94A3B8")
        )
        lbl_sub.pack(anchor="w", pady=(4, 0))

        # Badge com Perfil e Status
        box_badge = ctk.CTkFrame(banner, fg_color="transparent")
        box_badge.pack(side="right", padx=25, pady=20)

        badge_cor = self.COR_LARANJA if self.perfil == "ADMIN" else self.COR_AZUL
        badge_perfil = ctk.CTkFrame(box_badge, fg_color=badge_cor, corner_radius=6)
        badge_perfil.pack(anchor="e", pady=(0, 6))

        lbl_badge = ctk.CTkLabel(
            badge_perfil,
            text=f" PERFIL: {self.perfil} ",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color="#FFFFFF"
        )
        lbl_badge.pack(padx=8, pady=3)

        lbl_data = ctk.CTkLabel(
            box_badge,
            text=f"Acesso em {datetime.datetime.now().strftime('%d/%m/%Y')}",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=("#475569", "#94A3B8")
        )
        lbl_data.pack(anchor="e")

    def _criar_cards_resumo(self):
        """Grid com cards informativos sobre o sistema, módulos e status."""
        grid_cards = ctk.CTkFrame(self, fg_color="transparent")
        grid_cards.grid(row=1, column=0, padx=25, pady=10, sticky="ew")
        grid_cards.grid_columnconfigure((0, 1, 2), weight=1)

        # Card 1: Sobre o Sistema
        self._criar_card(
            grid_cards,
            col=0,
            icone="🏭",
            titulo="Sobre o Sistema",
            descricao="Gerenciamento unificado de recepção de materiais, validação de Notas Fiscais (XML), fretes CTE e controle de produção da AÇOS UNIÃO."
        )

        # Card 2: Seus Módulos Liberados
        if "*" in self.modulos or self.perfil == "ADMIN":
            desc_modulos = "Você possui acesso completo (Administrador) a todos os módulos operacionais do sistema."
        else:
            modulos_fmt = ", ".join([m.replace("_", " ").title() for m in self.modulos])
            desc_modulos = f"Módulos liberados para seu usuário: {modulos_fmt}."

        self._criar_card(
            grid_cards,
            col=1,
            icone="🛡️",
            titulo="Permissões de Acesso",
            descricao=desc_modulos
        )

        # Card 3: Status Operacional
        self._criar_card(
            grid_cards,
            col=2,
            icone="🟢",
            titulo="Status Operacional",
            descricao="• Sistema: Online\n• Banco de Dados: Conectado\n• Leitores XML: Operacionais\n• Versão: v1.0.4 Stable"
        )

    def _criar_card(self, parent, col, icone, titulo, descricao):
        """Cria um card padronizado."""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.COR_CARD_BG,
            border_color=self.COR_CARD_BORDER,
            border_width=1,
            corner_radius=10
        )
        card.grid(row=0, column=col, padx=8, pady=5, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)

        # Cabeçalho do Card
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(16, 8))

        lbl_icon = ctk.CTkLabel(
            header,
            text=icone,
            font=ctk.CTkFont(size=20)
        )
        lbl_icon.pack(side="left", padx=(0, 8))

        lbl_title = ctk.CTkLabel(
            header,
            text=titulo,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        lbl_title.pack(side="left")

        # Divisor interno do card
        div = ctk.CTkFrame(card, height=1, fg_color=self.COR_CARD_BORDER)
        div.pack(fill="x", padx=16, pady=(0, 10))

        # Descrição
        lbl_desc = ctk.CTkLabel(
            card,
            text=descricao,
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=("#334155", "#CBD5E1"),
            wraplength=260,
            justify="left"
        )
        lbl_desc.pack(anchor="w", padx=16, pady=(0, 16))

    def _criar_rodape_orientacao(self):
        """Card inferior orientando o usuário a selecionar um módulo no menu lateral."""
        box_info = ctk.CTkFrame(
            self,
            fg_color=("#E2E8F0", "#181B20"),
            border_color=("#CBD5E1", "#262B34"),
            border_width=1,
            corner_radius=10
        )
        box_info.grid(row=2, column=0, padx=25, pady=(15, 25), sticky="nsew")
        box_info.grid_columnconfigure(0, weight=1)

        box_conteudo = ctk.CTkFrame(box_info, fg_color="transparent")
        box_conteudo.place(relx=0.5, rely=0.5, anchor="center")

        lbl_dica = ctk.CTkLabel(
            box_conteudo,
            text="👈  Para iniciar as operações, escolha um dos módulos no menu lateral à esquerda.",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.COR_LARANJA
        )
        lbl_dica.pack(pady=10)
