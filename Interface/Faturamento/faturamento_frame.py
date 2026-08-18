import threading
import customtkinter as ctk
from tkinter import messagebox

try:
    from Interface.Faturamento.função_faturamento.faturamento import iniciar as iniciar_faturamento
    from Interface.Faturamento.função_faturamento.enviar_emails_vendedores import enviar_emails_vendedores
    from Interface.Faturamento.função_faturamento.relatorio_diario_mes import gerar_relatorio_diario_mes
    from Interface.Faturamento.função_faturamento.relatorio_faturamento_diario import gerar_relatorio_faturamento_diario
    from Interface.Faturamento.calculadora_icms import CalculadoraICMSModal
except ImportError:
    from .função_faturamento.faturamento import iniciar as iniciar_faturamento
    from .função_faturamento.enviar_emails_vendedores import enviar_emails_vendedores
    from .função_faturamento.relatorio_diario_mes import gerar_relatorio_diario_mes
    from .função_faturamento.relatorio_faturamento_diario import gerar_relatorio_faturamento_diario
    from .calculadora_icms import CalculadoraICMSModal


class FaturamentoFrame(ctk.CTkFrame):
    """
    Frame do Módulo de Faturamento do Sistema AÇOS UNIÃO MANAGER.
    Contém os cards de controle e acionamento das automações e relatórios de faturamento.
    """
    COR_CARD_BG = ("#F0F4F8", "#1E2228")
    COR_CARD_BORDER = ("#94A3B8", "#2D323E")

    def __init__(self, parent, usuario_logado="Operador Sistema", dados_usuario=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.usuario_logado = usuario_logado
        self.dados_usuario = dados_usuario or {}

        # Flags de controle de execução por card
        self.executando = {
            "automacao": False,
            "email": False,
            "relatorio_mes": False,
            "relatorio_fat": False
        }

        # Configuração do Grid Principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Cabeçalho da Seção
        self._criar_header()

        # 2. Container Rolável de Cards (Layout 2x2)
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
        """Cria a área rolável de cards operacionais do faturamento em grade 2x2."""
        self.cards_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        self.cards_container.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.cards_container.grid_columnconfigure((0, 1), weight=1)

        # Card 1: Execução da Automação de Faturamento (Row 0, Col 0)
        self._criar_card_automacao(row=0, col=0)

        # Card 2: Enviar E-mails para Vendedores (Row 0, Col 1)
        self._criar_card_email_vendedores(row=0, col=1)

        # Card 3: Relatório Diário / Mês (Row 1, Col 0)
        self._criar_card_relatorio_diario_mes(row=1, col=0)

        # Card 4: Relatório Faturamento Diário (Row 1, Col 1)
        self._criar_card_relatorio_faturamento_diario(row=1, col=1)

        # Card 5: Calculadora de ICMS (Row 2, Col 0)
        self._criar_card_calculadora_icms(row=2, col=0)

    # -------------------------------------------------------------------------
    # Card 1: Automação de Faturamento
    # -------------------------------------------------------------------------
    def _criar_card_automacao(self, row, col):
        card = ctk.CTkFrame(
            self.cards_container,
            fg_color=self.COR_CARD_BG,
            border_color=self.COR_CARD_BORDER,
            border_width=1,
            corner_radius=12
        )
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        card.grid_columnconfigure(0, weight=1)

        # Header do Card
        card_header = ctk.CTkFrame(card, fg_color="transparent")
        card_header.pack(fill="x", padx=20, pady=(18, 10))

        lbl_card_title = ctk.CTkLabel(
            card_header,
            text="⚡  Automação de Faturamento",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        lbl_card_title.pack(side="left")

        divisor = ctk.CTkFrame(card, height=1, fg_color=self.COR_CARD_BORDER)
        divisor.pack(fill="x", padx=20, pady=(0, 12))

        # Conteúdo Explicativo
        card_body = ctk.CTkFrame(card, fg_color="transparent")
        card_body.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        lbl_desc = ctk.CTkLabel(
            card_body,
            text=(
                "Executa a sequência automatizada de faturamento do sistema (rotinas MTM194, MTM724 e MTM237).\n"
                "Para prosseguir cada etapa após iniciar, utilize o botão lateral do mouse (x2) ou cancele com (x)."
            ),
            font=ctk.CTkFont(size=12),
            text_color=("#475569", "#94A3B8"),
            justify="left",
            wraplength=340
        )
        lbl_desc.pack(anchor="w", pady=(0, 10))

        # Painel de Ações
        card_actions = ctk.CTkFrame(card, fg_color="transparent")
        card_actions.pack(fill="x", padx=20, pady=(0, 18))

        self.btn_iniciar_automacao = ctk.CTkButton(
            card_actions,
            text="🚀  INICIAR FATURAMENTO",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#EA580C",
            hover_color="#C2410C",
            text_color="#FFFFFF",
            height=42,
            corner_radius=8,
            command=self._iniciar_processo_faturamento
        )
        self.btn_iniciar_automacao.pack(fill="x", pady=(0, 8))

        self.lbl_status_automacao = ctk.CTkLabel(
            card_actions,
            text="🟢  Status: Pronto para iniciar",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#16A34A", "#4ADE80")
        )
        self.lbl_status_automacao.pack(anchor="w")

    # -------------------------------------------------------------------------
    # Card 2: Enviar E-mails para Vendedores
    # -------------------------------------------------------------------------
    def _criar_card_email_vendedores(self, row, col):
        card = ctk.CTkFrame(
            self.cards_container,
            fg_color=self.COR_CARD_BG,
            border_color=self.COR_CARD_BORDER,
            border_width=1,
            corner_radius=12
        )
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        card.grid_columnconfigure(0, weight=1)

        # Header do Card
        card_header = ctk.CTkFrame(card, fg_color="transparent")
        card_header.pack(fill="x", padx=20, pady=(18, 10))

        lbl_card_title = ctk.CTkLabel(
            card_header,
            text="📧  Enviar E-mails para Vendedores",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        lbl_card_title.pack(side="left")

        divisor = ctk.CTkFrame(card, height=1, fg_color=self.COR_CARD_BORDER)
        divisor.pack(fill="x", padx=20, pady=(0, 12))

        # Conteúdo Explicativo
        card_body = ctk.CTkFrame(card, fg_color="transparent")
        card_body.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        lbl_desc = ctk.CTkLabel(
            card_body,
            text="Envio de pedidos faturados por e-mail com vendedor em CC.",
            font=ctk.CTkFont(size=12),
            text_color=("#475569", "#94A3B8"),
            justify="left",
            wraplength=340
        )
        lbl_desc.pack(anchor="w", pady=(0, 10))

        # Painel de Ações
        card_actions = ctk.CTkFrame(card, fg_color="transparent")
        card_actions.pack(fill="x", padx=20, pady=(0, 18))

        self.btn_enviar_emails = ctk.CTkButton(
            card_actions,
            text="📧  ENVIAR E-MAILS PARA VENDEDORES",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            height=42,
            corner_radius=8,
            command=self._iniciar_envio_emails
        )
        self.btn_enviar_emails.pack(fill="x", pady=(0, 8))

        self.lbl_status_email = ctk.CTkLabel(
            card_actions,
            text="🟢  Status: Pronto para enviar",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#16A34A", "#4ADE80")
        )
        self.lbl_status_email.pack(anchor="w")

    # -------------------------------------------------------------------------
    # Card 3: Relatório Diário / Mês
    # -------------------------------------------------------------------------
    def _criar_card_relatorio_diario_mes(self, row, col):
        card = ctk.CTkFrame(
            self.cards_container,
            fg_color=self.COR_CARD_BG,
            border_color=self.COR_CARD_BORDER,
            border_width=1,
            corner_radius=12
        )
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        card.grid_columnconfigure(0, weight=1)

        # Header do Card
        card_header = ctk.CTkFrame(card, fg_color="transparent")
        card_header.pack(fill="x", padx=20, pady=(18, 10))

        lbl_card_title = ctk.CTkLabel(
            card_header,
            text="📅  Relatório Diário / Mês",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        lbl_card_title.pack(side="left")

        divisor = ctk.CTkFrame(card, height=1, fg_color=self.COR_CARD_BORDER)
        divisor.pack(fill="x", padx=20, pady=(0, 12))

        # Conteúdo Explicativo
        card_body = ctk.CTkFrame(card, fg_color="transparent")
        card_body.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        lbl_desc = ctk.CTkLabel(
            card_body,
            text=(
                "Gera e compila o relatório consolidado de movimentação diária e resumo mensal de faturamento.\n"
                "Exporta os dados para acompanhamento gerencial."
            ),
            font=ctk.CTkFont(size=12),
            text_color=("#475569", "#94A3B8"),
            justify="left",
            wraplength=340
        )
        lbl_desc.pack(anchor="w", pady=(0, 10))

        # Painel de Ações
        card_actions = ctk.CTkFrame(card, fg_color="transparent")
        card_actions.pack(fill="x", padx=20, pady=(0, 18))

        self.btn_relatorio_mes = ctk.CTkButton(
            card_actions,
            text="📊  GERAR RELATÓRIO DIÁRIO/MÊS",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#059669",
            hover_color="#047857",
            text_color="#FFFFFF",
            height=42,
            corner_radius=8,
            command=self._iniciar_relatorio_diario_mes
        )
        self.btn_relatorio_mes.pack(fill="x", pady=(0, 8))

        self.lbl_status_relatorio_mes = ctk.CTkLabel(
            card_actions,
            text="🟢  Status: Pronto para gerar",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#16A34A", "#4ADE80")
        )
        self.lbl_status_relatorio_mes.pack(anchor="w")

    # -------------------------------------------------------------------------
    # Card 4: Relatório Faturamento Diário
    # -------------------------------------------------------------------------
    def _criar_card_relatorio_faturamento_diario(self, row, col):
        card = ctk.CTkFrame(
            self.cards_container,
            fg_color=self.COR_CARD_BG,
            border_color=self.COR_CARD_BORDER,
            border_width=1,
            corner_radius=12
        )
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        card.grid_columnconfigure(0, weight=1)

        # Header do Card
        card_header = ctk.CTkFrame(card, fg_color="transparent")
        card_header.pack(fill="x", padx=20, pady=(18, 10))

        lbl_card_title = ctk.CTkLabel(
            card_header,
            text="📈  Relatório Faturamento Diário",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        lbl_card_title.pack(side="left")

        divisor = ctk.CTkFrame(card, height=1, fg_color=self.COR_CARD_BORDER)
        divisor.pack(fill="x", padx=20, pady=(0, 12))

        # Conteúdo Explicativo
        card_body = ctk.CTkFrame(card, fg_color="transparent")
        card_body.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        lbl_desc = ctk.CTkLabel(
            card_body,
            text=(
                "Compilação detalhada do faturamento efetuado no dia corrente, incluindo notas emitidas e totais faturados.\n"
                "Ideal para controle e fechamento diário."
            ),
            font=ctk.CTkFont(size=12),
            text_color=("#475569", "#94A3B8"),
            justify="left",
            wraplength=340
        )
        lbl_desc.pack(anchor="w", pady=(0, 10))

        # Painel de Ações
        card_actions = ctk.CTkFrame(card, fg_color="transparent")
        card_actions.pack(fill="x", padx=20, pady=(0, 18))

        self.btn_relatorio_fat = ctk.CTkButton(
            card_actions,
            text="💵  GERAR RELATÓRIO FATURAMENTO",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#7C3AED",
            hover_color="#6D28D9",
            text_color="#FFFFFF",
            height=42,
            corner_radius=8,
            command=self._iniciar_relatorio_faturamento_diario
        )
        self.btn_relatorio_fat.pack(fill="x", pady=(0, 8))

        self.lbl_status_relatorio_fat = ctk.CTkLabel(
            card_actions,
            text="🟢  Status: Pronto para gerar",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#16A34A", "#4ADE80")
        )
        self.lbl_status_relatorio_fat.pack(anchor="w")

    # =========================================================================
    # Lógica de Execução dos Processos Assíncronos
    # =========================================================================

    # 1. Automação de Faturamento
    def _iniciar_processo_faturamento(self):
        if self.executando["automacao"]:
            messagebox.showwarning("Aviso", "A automação de faturamento já está em execução!")
            return

        confirmar = messagebox.askyesno(
            "Confirmar Automação",
            "Deseja iniciar o processo automatizado de faturamento?"
        )
        if not confirmar:
            return

        self.executando["automacao"] = True
        self.btn_iniciar_automacao.configure(state="disabled", fg_color="#64748B", text="⏳  EM EXECUÇÃO...")
        self.lbl_status_automacao.configure(
            text="🟡  Status: Automação em execução...",
            text_color=("#D97706", "#FBBF24")
        )

        threading.Thread(target=self._executar_thread_faturamento, daemon=True).start()

    def _executar_thread_faturamento(self):
        try:
            iniciar_faturamento()
            self.after(0, self._finalizar_execucao_automacao, True, "Automação finalizada com sucesso!")
        except Exception as e:
            self.after(0, self._finalizar_execucao_automacao, False, str(e))

    def _finalizar_execucao_automacao(self, sucesso, mensagem):
        self.executando["automacao"] = False
        self.btn_iniciar_automacao.configure(state="normal", fg_color="#EA580C", text="🚀  INICIAR FATURAMENTO")

        if sucesso:
            self.lbl_status_automacao.configure(
                text="🟢  Status: Concluído com sucesso",
                text_color=("#16A34A", "#4ADE80")
            )
            messagebox.showinfo("Sucesso", mensagem)
        else:
            self.lbl_status_automacao.configure(
                text="🔴  Status: Erro ou cancelado",
                text_color=("#DC2626", "#F87171")
            )
            messagebox.showerror("Erro no Faturamento", f"Ocorreu um erro durante a automação:\n{mensagem}")

    # 2. Enviar E-mails para Vendedores
    def _iniciar_envio_emails(self):
        if self.executando["email"]:
            messagebox.showwarning("Aviso", "O envio de e-mails já está em andamento!")
            return

        confirmar = messagebox.askyesno(
            "Confirmar Envio",
            "Deseja iniciar o envio de e-mails para os vendedores?"
        )
        if not confirmar:
            return

        self.executando["email"] = True
        self.btn_enviar_emails.configure(state="disabled", fg_color="#64748B", text="⏳  ENVIANDO E-MAILS...")
        self.lbl_status_email.configure(
            text="🟡  Status: Enviando e-mails...",
            text_color=("#D97706", "#FBBF24")
        )

        threading.Thread(target=self._executar_thread_emails, daemon=True).start()

    def _executar_thread_emails(self):
        try:
            sucesso, msg = enviar_emails_vendedores()
            self.after(0, self._finalizar_execucao_emails, sucesso, msg)
        except Exception as e:
            self.after(0, self._finalizar_execucao_emails, False, str(e))

    def _finalizar_execucao_emails(self, sucesso, mensagem):
        self.executando["email"] = False
        self.btn_enviar_emails.configure(state="normal", fg_color="#1D4ED8", text="📧  ENVIAR E-MAILS PARA VENDEDORES")

        if sucesso:
            self.lbl_status_email.configure(
                text="🟢  Status: Envio concluído",
                text_color=("#16A34A", "#4ADE80")
            )
            messagebox.showinfo("Sucesso", mensagem)
        else:
            self.lbl_status_email.configure(
                text="🔴  Status: Erro no envio",
                text_color=("#DC2626", "#F87171")
            )
            messagebox.showerror("Erro no Envio", f"Ocorreu um erro ao enviar e-mails:\n{mensagem}")

    # 3. Relatório Diário / Mês
    def _iniciar_relatorio_diario_mes(self):
        if self.executando["relatorio_mes"]:
            messagebox.showwarning("Aviso", "A geração do relatório já está em andamento!")
            return

        confirmar = messagebox.askyesno(
            "Confirmar Relatório",
            "Deseja gerar o Relatório Diário / Mês?"
        )
        if not confirmar:
            return

        self.executando["relatorio_mes"] = True
        self.btn_relatorio_mes.configure(state="disabled", fg_color="#64748B", text="⏳  GERANDO RELATÓRIO...")
        self.lbl_status_relatorio_mes.configure(
            text="🟡  Status: Gerando relatório...",
            text_color=("#D97706", "#FBBF24")
        )

        threading.Thread(target=self._executar_thread_relatorio_mes, daemon=True).start()

    def _executar_thread_relatorio_mes(self):
        try:
            sucesso, msg = gerar_relatorio_diario_mes()
            self.after(0, self._finalizar_execucao_relatorio_mes, sucesso, msg)
        except Exception as e:
            self.after(0, self._finalizar_execucao_relatorio_mes, False, str(e))

    def _finalizar_execucao_relatorio_mes(self, sucesso, mensagem):
        self.executando["relatorio_mes"] = False
        self.btn_relatorio_mes.configure(state="normal", fg_color="#059669", text="📊  GERAR RELATÓRIO DIÁRIO/MÊS")

        if sucesso:
            self.lbl_status_relatorio_mes.configure(
                text="🟢  Status: Relatório gerado",
                text_color=("#16A34A", "#4ADE80")
            )
            messagebox.showinfo("Sucesso", mensagem)
        else:
            self.lbl_status_relatorio_mes.configure(
                text="🔴  Status: Erro na geração",
                text_color=("#DC2626", "#F87171")
            )
            messagebox.showerror("Erro no Relatório", f"Ocorreu um erro ao gerar relatório:\n{mensagem}")

    # 4. Relatório Faturamento Diário
    def _iniciar_relatorio_faturamento_diario(self):
        if self.executando["relatorio_fat"]:
            messagebox.showwarning("Aviso", "A geração do relatório de faturamento diário já está em andamento!")
            return

        confirmar = messagebox.askyesno(
            "Confirmar Relatório",
            "Deseja gerar o Relatório de Faturamento Diário?"
        )
        if not confirmar:
            return

        self.executando["relatorio_fat"] = True
        self.btn_relatorio_fat.configure(state="disabled", fg_color="#64748B", text="⏳  GERANDO RELATÓRIO...")
        self.lbl_status_relatorio_fat.configure(
            text="🟡  Status: Gerando relatório...",
            text_color=("#D97706", "#FBBF24")
        )

        threading.Thread(target=self._executar_thread_relatorio_fat, daemon=True).start()

    def _executar_thread_relatorio_fat(self):
        try:
            sucesso, msg = gerar_relatorio_faturamento_diario()
            self.after(0, self._finalizar_execucao_relatorio_fat, sucesso, msg)
        except Exception as e:
            self.after(0, self._finalizar_execucao_relatorio_fat, False, str(e))

    def _finalizar_execucao_relatorio_fat(self, sucesso, mensagem):
        self.executando["relatorio_fat"] = False
        self.btn_relatorio_fat.configure(state="normal", fg_color="#7C3AED", text="💵  GERAR RELATÓRIO FATURAMENTO")

        if sucesso:
            self.lbl_status_relatorio_fat.configure(
                text="🟢  Status: Relatório gerado",
                text_color=("#16A34A", "#4ADE80")
            )
            messagebox.showinfo("Sucesso", mensagem)
        else:
            self.lbl_status_relatorio_fat.configure(
                text="🔴  Status: Erro na geração",
                text_color=("#DC2626", "#F87171")
            )
            messagebox.showerror("Erro no Relatório", f"Ocorreu um erro ao gerar relatório:\n{mensagem}")

    # -------------------------------------------------------------------------
    # Card 5: Calculadora de valor aprox dos tributos
    # -------------------------------------------------------------------------
    def _criar_card_calculadora_icms(self, row, col):
        card = ctk.CTkFrame(
            self.cards_container,
            fg_color=self.COR_CARD_BG,
            border_color=self.COR_CARD_BORDER,
            border_width=1,
            corner_radius=12
        )
        card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        card.grid_columnconfigure(0, weight=1)

        # Header do Card
        card_header = ctk.CTkFrame(card, fg_color="transparent")
        card_header.pack(fill="x", padx=20, pady=(18, 10))

        lbl_card_title = ctk.CTkLabel(
            card_header,
            text="🧮  Calculadora de valor aprox dos tributos",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        lbl_card_title.pack(side="left")

        divisor = ctk.CTkFrame(card, height=1, fg_color=self.COR_CARD_BORDER)
        divisor.pack(fill="x", padx=20, pady=(0, 12))

        # Conteúdo Explicativo
        card_body = ctk.CTkFrame(card, fg_color="transparent")
        card_body.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        lbl_desc = ctk.CTkLabel(
            card_body,
            text=(
                "Calculadora auxiliar para simulação de alíquotas de ICMS Perfil (12% e 7%) e "
                "ICMS Chapa (12% e 7%) com base em um valor informado."
            ),
            font=ctk.CTkFont(size=12),
            text_color=("#475569", "#94A3B8"),
            justify="left",
            wraplength=340
        )
        lbl_desc.pack(anchor="w", pady=(0, 10))

        # Painel de Ações
        card_actions = ctk.CTkFrame(card, fg_color="transparent")
        card_actions.pack(fill="x", padx=20, pady=(0, 18))

        self.btn_abrir_calculadora = ctk.CTkButton(
            card_actions,
            text="🧮  ABRIR CALCULADORA DE TRIBUTOS",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#0EA5E9",
            hover_color="#0284C7",
            text_color="#FFFFFF",
            height=42,
            corner_radius=8,
            command=self._abrir_calculadora_icms
        )
        self.btn_abrir_calculadora.pack(fill="x", pady=(0, 8))

        self.lbl_status_calc = ctk.CTkLabel(
            card_actions,
            text="🟢  Status: Pronta para uso",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#16A34A", "#4ADE80")
        )
        self.lbl_status_calc.pack(anchor="w")

    def _abrir_calculadora_icms(self):
        # Evita abrir múltiplas instâncias da calculadora ao mesmo tempo
        if hasattr(self, "janela_calculadora") and self.janela_calculadora.winfo_exists():
            self.janela_calculadora.focus_force()
        else:
            self.janela_calculadora = CalculadoraICMSModal(self)

