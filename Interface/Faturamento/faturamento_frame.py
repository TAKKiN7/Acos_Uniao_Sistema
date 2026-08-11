import threading
import customtkinter as ctk
from tkinter import messagebox

try:
    from Interface.Faturamento.função_faturamento.faturamento import iniciar as iniciar_faturamento
except ImportError:
    from .função_faturamento.faturamento import iniciar as iniciar_faturamento


class FaturamentoFrame(ctk.CTkFrame):
    """
    Frame do Módulo de Faturamento do Sistema AÇOS UNIÃO MANAGER.
    Contém os cards de controle e acionamento das automações de faturamento.
    """
    COR_CARD_BG = ("#F0F4F8", "#1E2228")
    COR_CARD_BORDER = ("#94A3B8", "#2D323E")

    def __init__(self, parent, usuario_logado="Operador Sistema", dados_usuario=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.usuario_logado = usuario_logado
        self.dados_usuario = dados_usuario or {}
        self.executando = False

        # Configuração do Grid
        self.grid_columnconfigure(0, weight=1)

        # 1. Cabeçalho da Seção
        self._criar_header()

        # 2. Container dos Cards
        self._criar_cards()

    def _criar_header(self):
        """Cria o cabeçalho superior da aba Faturamento."""
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 15))

        self.lbl_modulo = ctk.CTkLabel(
            self.header_frame,
            text="MÓDULO DE FATURAMENTO",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        self.lbl_modulo.pack(anchor="w")

        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame,
            text="Gestão & Automação de Faturamento",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_titulo.pack(anchor="w", pady=(2, 0))

    def _criar_cards(self):
        """Cria a área de cards operacionais do faturamento."""
        self.cards_container = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_container.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.cards_container.grid_columnconfigure(0, weight=1)

        # Card 1: Execução da Automação de Faturamento
        self.card_automacao = ctk.CTkFrame(
            self.cards_container,
            fg_color=self.COR_CARD_BG,
            border_color=self.COR_CARD_BORDER,
            border_width=1,
            corner_radius=12
        )
        self.card_automacao.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.card_automacao.grid_columnconfigure(0, weight=1)

        # Header do Card
        card_header = ctk.CTkFrame(self.card_automacao, fg_color="transparent")
        card_header.pack(fill="x", padx=20, pady=(20, 10))

        lbl_card_title = ctk.CTkLabel(
            card_header,
            text="⚡  Automação de Faturamento",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        lbl_card_title.pack(side="left")

        # Divisor
        divisor = ctk.CTkFrame(self.card_automacao, height=1, fg_color=self.COR_CARD_BORDER)
        divisor.pack(fill="x", padx=20, pady=(0, 15))

        # Conteúdo Explicativo
        card_body = ctk.CTkFrame(self.card_automacao, fg_color="transparent")
        card_body.pack(fill="x", padx=20, pady=(0, 15))

        lbl_desc = ctk.CTkLabel(
            card_body,
            text=(
                "Executa a sequência automatizada de faturamento do sistema (rotinas MTM194, MTM724 e MTM237).\n"
                "Para prosseguir cada etapa após iniciar, utilize o botão lateral do mouse (x2) ou cancele com (x)."
            ),
            font=ctk.CTkFont(size=13),
            text_color=("#475569", "#94A3B8"),
            justify="left"
        )
        lbl_desc.pack(anchor="w", pady=(0, 15))

        # Painel de Ações do Card (Botão + Badge de Status)
        card_actions = ctk.CTkFrame(self.card_automacao, fg_color="transparent")
        card_actions.pack(fill="x", padx=20, pady=(0, 20))

        self.btn_iniciar = ctk.CTkButton(
            card_actions,
            text="🚀  INICIAR FATURAMENTO AUTOMÁTICO",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#EA580C",
            hover_color="#C2410C",
            text_color="#FFFFFF",
            height=45,
            corner_radius=8,
            command=self._iniciar_processo_faturamento
        )
        self.btn_iniciar.pack(side="left", padx=(0, 15))

        self.lbl_status = ctk.CTkLabel(
            card_actions,
            text="🟢  Status: Pronto para iniciar",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#16A34A", "#4ADE80")
        )
        self.lbl_status.pack(side="left")

    def _iniciar_processo_faturamento(self):
        """Inicia a função de faturamento em uma thread separada para não travar a interface gráfica."""
        if self.executando:
            messagebox.showwarning("Aviso", "A automação de faturamento já está em execução!")
            return

        confirmar = messagebox.askyesno(
            "Confirmar Automação",
            "Deseja iniciar o processo automatizado de faturamento?"
        )
        if not confirmar:
            return

        self.executando = True
        self.btn_iniciar.configure(state="disabled", fg_color="#64748B", text="⏳  EM EXECUÇÃO...")
        self.lbl_status.configure(
            text="🟡  Status: Automação em execução...",
            text_color=("#D97706", "#FBBF24")
        )

        # Thread para rodar o processo sem travar o Tkinter
        thread = threading.Thread(target=self._executar_thread_faturamento, daemon=True)
        thread.start()

    def _executar_thread_faturamento(self):
        """Executa a função `iniciar` da pasta função_faturamento."""
        try:
            iniciar_faturamento()
            # Atualiza o status na thread principal do Tkinter
            self.after(0, self._finalizar_execucao, True, "Automação finalizada com sucesso!")
        except Exception as e:
            self.after(0, self._finalizar_execucao, False, str(e))

    def _finalizar_execucao(self, sucesso, mensagem):
        """Restaura o estado do botão e atualiza o status após o término da thread."""
        self.executando = False
        self.btn_iniciar.configure(state="normal", fg_color="#EA580C", text="🚀  INICIAR FATURAMENTO AUTOMÁTICO")

        if sucesso:
            self.lbl_status.configure(
                text="🟢  Status: Concluído com sucesso",
                text_color=("#16A34A", "#4ADE80")
            )
            messagebox.showinfo("Sucesso", mensagem)
        else:
            self.lbl_status.configure(
                text="🔴  Status: Erro ou cancelado",
                text_color=("#DC2626", "#F87171")
            )
            messagebox.showerror("Erro no Faturamento", f"Ocorreu um erro durante a automação:\n{mensagem}")
