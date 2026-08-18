import sys
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox

class CalculadoraICMSModal(ctk.CTkToplevel):
    """
    Modal da Calculadora de Alíquotas de ICMS.
    Permite calcular de forma dinâmica e em tempo real os valores das alíquotas de ICMS
    sobre um valor base informado pelo usuário.
    """
    COR_CARD_BG = ("#F0F4F8", "#1E2228")
    COR_CARD_BORDER = ("#94A3B8", "#2D323E")

    def __init__(self, parent):
        super().__init__(parent)

        self.title("🧮 Calculadora de valor aprox dos tributos")
        self.geometry("520x600")
        self.resizable(False, False)

        # Configurações de Modalidade e Foco
        self.grab_set()
        self.focus_force()
        self.definir_icone()
        self.center_window()

        # Variáveis de Controle
        self.var_valor = ctk.StringVar(value="")
        self.var_perfil_12 = ctk.BooleanVar(value=True)
        self.var_perfil_7 = ctk.BooleanVar(value=False)
        self.var_chapa_12 = ctk.BooleanVar(value=False)
        self.var_icms_7 = ctk.BooleanVar(value=False)

        # Tracing para cálculo em tempo real
        self.var_valor.trace_add("write", self._atualizar_calculos)
        
        # Elementos de Interface
        self._configurar_grid()
        self._criar_header()
        self._criar_formulario()
        self._criar_resultados()
        self._criar_botoes_acao()

        # Executa cálculo inicial
        self._atualizar_calculos()

    def _configurar_grid(self):
        self.grid_columnconfigure(0, weight=1)

    def _criar_header(self):
        """Cria o cabeçalho superior da calculadora."""
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=30, pady=(15, 5))

        self.lbl_modulo = ctk.CTkLabel(
            self.header_frame,
            text="FERRAMENTA DE FATURAMENTO",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        self.lbl_modulo.pack(anchor="w")

        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame,
            text="Calculadora de Valor Aprox. dos Tributos",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_titulo.pack(anchor="w", pady=(2, 0))

        divisor = ctk.CTkFrame(self, height=1, fg_color=self.COR_CARD_BORDER)
        divisor.pack(fill="x", padx=30, pady=(0, 10))

    def _criar_formulario(self):
        """Cria a seção de entrada de valores e seleção de alíquotas."""
        # Container de Entrada
        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.form_frame.pack(fill="x", padx=30, pady=(0, 8))

        # Campo de Valor
        self.lbl_valor = ctk.CTkLabel(
            self.form_frame,
            text="Valor Base (R$):",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("#334155", "#E2E8F0")
        )
        self.lbl_valor.pack(anchor="w", pady=(0, 3))

        self.entry_valor = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Ex: 1.000,00 ou 1000",
            textvariable=self.var_valor,
            font=ctk.CTkFont(size=14),
            fg_color=("#FFFFFF", "#14171C"),
            border_color=self.COR_CARD_BORDER,
            height=40
        )
        self.entry_valor.pack(fill="x", pady=(0, 10))
        self.entry_valor.focus_set()

        # Checkboxes Container
        self.checkboxes_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.checkboxes_frame.pack(fill="x", pady=(0, 8))
        self.checkboxes_frame.grid_columnconfigure((0, 1), weight=1)

        # Checkbox 1: ICMS Perfil 12,00 (21,25%)
        self.chk_perfil_12 = ctk.CTkCheckBox(
            self.checkboxes_frame,
            text="ICMS Perfil 12,00 (21,25%)",
            variable=self.var_perfil_12,
            font=ctk.CTkFont(size=12),
            command=self._atualizar_calculos
        )
        self.chk_perfil_12.grid(row=0, column=0, padx=5, pady=4, sticky="w")

        # Checkbox 2: ICMS Perfil 7,00 (16,25%)
        self.chk_perfil_7 = ctk.CTkCheckBox(
            self.checkboxes_frame,
            text="ICMS Perfil 7,00 (16,25%)",
            variable=self.var_perfil_7,
            font=ctk.CTkFont(size=12),
            command=self._atualizar_calculos
        )
        self.chk_perfil_7.grid(row=0, column=1, padx=5, pady=4, sticky="w")

        # Checkbox 3: ICMS Chapa 12,00 (24,5%)
        self.chk_chapa_12 = ctk.CTkCheckBox(
            self.checkboxes_frame,
            text="ICMS Chapa 12,00 (24,50%)",
            variable=self.var_chapa_12,
            font=ctk.CTkFont(size=12),
            command=self._atualizar_calculos
        )
        self.chk_chapa_12.grid(row=1, column=0, padx=5, pady=4, sticky="w")

        # Checkbox 4: ICMS 7,00 (19,5%)
        self.chk_icms_7 = ctk.CTkCheckBox(
            self.checkboxes_frame,
            text="ICMS 7,00 (19,50%)",
            variable=self.var_icms_7,
            font=ctk.CTkFont(size=12),
            command=self._atualizar_calculos
        )
        self.chk_icms_7.grid(row=1, column=1, padx=5, pady=4, sticky="w")

    def _criar_resultados(self):
        """Cria o painel de resultados com os valores calculados."""
        self.results_title = ctk.CTkLabel(
            self,
            text="Valores Calculados:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("#334155", "#E2E8F0")
        )
        self.results_title.pack(anchor="w", padx=30, pady=(0, 3))

        # Container dos resultados
        self.results_frame = ctk.CTkFrame(
            self,
            fg_color=self.COR_CARD_BG,
            border_color=self.COR_CARD_BORDER,
            border_width=1,
            corner_radius=8
        )
        self.results_frame.pack(fill="x", padx=30, pady=(0, 12))
        self.results_frame.grid_columnconfigure(0, weight=2)
        self.results_frame.grid_columnconfigure(1, weight=1)
        self.results_frame.grid_columnconfigure(2, weight=1)

        # Estilo dos labels
        lbl_font = ctk.CTkFont(size=12)
        val_font = ctk.CTkFont(size=13, weight="bold")

        # Linha 1: Perfil 12,00 (21,25%)
        self.lbl_title_perfil_12 = ctk.CTkLabel(self.results_frame, text="ICMS Perfil 12,00 (21,25%):", font=lbl_font, anchor="w")
        self.lbl_title_perfil_12.grid(row=0, column=0, padx=15, pady=6, sticky="w")

        self.lbl_val_perfil_12 = ctk.CTkLabel(self.results_frame, text="R$ 0,00", font=val_font, anchor="e")
        self.lbl_val_perfil_12.grid(row=0, column=1, padx=10, pady=6, sticky="e")

        self.btn_copy_perfil_12 = ctk.CTkButton(
            self.results_frame, text="📋 Copiar", width=70, height=24, font=ctk.CTkFont(size=11),
            fg_color=("#E2E8F0", "#2D323E"), text_color=("#0F172A", "#FFFFFF"), hover_color=("#CBD5E1", "#3E4452"),
            command=lambda: self._copiar_valor("perfil_12", 0.2125, self.btn_copy_perfil_12)
        )
        self.btn_copy_perfil_12.grid(row=0, column=2, padx=15, pady=6, sticky="e")

        # Linha 2: Perfil 7,00 (16,25%)
        self.lbl_title_perfil_7 = ctk.CTkLabel(self.results_frame, text="ICMS Perfil 7,00 (16,25%):", font=lbl_font, anchor="w")
        self.lbl_title_perfil_7.grid(row=1, column=0, padx=15, pady=6, sticky="w")

        self.lbl_val_perfil_7 = ctk.CTkLabel(self.results_frame, text="R$ 0,00", font=val_font, anchor="e")
        self.lbl_val_perfil_7.grid(row=1, column=1, padx=10, pady=6, sticky="e")

        self.btn_copy_perfil_7 = ctk.CTkButton(
            self.results_frame, text="📋 Copiar", width=70, height=24, font=ctk.CTkFont(size=11),
            fg_color=("#E2E8F0", "#2D323E"), text_color=("#0F172A", "#FFFFFF"), hover_color=("#CBD5E1", "#3E4452"),
            command=lambda: self._copiar_valor("perfil_7", 0.1625, self.btn_copy_perfil_7)
        )
        self.btn_copy_perfil_7.grid(row=1, column=2, padx=15, pady=6, sticky="e")

        # Linha 3: Chapa 12,00 (24,50%)
        self.lbl_title_chapa_12 = ctk.CTkLabel(self.results_frame, text="ICMS Chapa 12,00 (24,50%):", font=lbl_font, anchor="w")
        self.lbl_title_chapa_12.grid(row=2, column=0, padx=15, pady=6, sticky="w")

        self.lbl_val_chapa_12 = ctk.CTkLabel(self.results_frame, text="R$ 0,00", font=val_font, anchor="e")
        self.lbl_val_chapa_12.grid(row=2, column=1, padx=10, pady=6, sticky="e")

        self.btn_copy_chapa_12 = ctk.CTkButton(
            self.results_frame, text="📋 Copiar", width=70, height=24, font=ctk.CTkFont(size=11),
            fg_color=("#E2E8F0", "#2D323E"), text_color=("#0F172A", "#FFFFFF"), hover_color=("#CBD5E1", "#3E4452"),
            command=lambda: self._copiar_valor("chapa_12", 0.2450, self.btn_copy_chapa_12)
        )
        self.btn_copy_chapa_12.grid(row=2, column=2, padx=15, pady=6, sticky="e")

        # Linha 4: ICMS 7,00 (19,50%)
        self.lbl_title_icms_7 = ctk.CTkLabel(self.results_frame, text="ICMS 7,00 (19,50%):", font=lbl_font, anchor="w")
        self.lbl_title_icms_7.grid(row=3, column=0, padx=15, pady=6, sticky="w")

        self.lbl_val_icms_7 = ctk.CTkLabel(self.results_frame, text="R$ 0,00", font=val_font, anchor="e")
        self.lbl_val_icms_7.grid(row=3, column=1, padx=10, pady=6, sticky="e")

        self.btn_copy_icms_7 = ctk.CTkButton(
            self.results_frame, text="📋 Copiar", width=70, height=24, font=ctk.CTkFont(size=11),
            fg_color=("#E2E8F0", "#2D323E"), text_color=("#0F172A", "#FFFFFF"), hover_color=("#CBD5E1", "#3E4452"),
            command=lambda: self._copiar_valor("icms_7", 0.1950, self.btn_copy_icms_7)
        )
        self.btn_copy_icms_7.grid(row=3, column=2, padx=15, pady=6, sticky="e")

    def _criar_botoes_acao(self):
        """Cria os botões de ação na parte inferior."""
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.pack(fill="x", padx=30, pady=(0, 15))
        self.actions_frame.grid_columnconfigure((0, 1), weight=1)

        self.btn_limpar = ctk.CTkButton(
            self.actions_frame,
            text="🧹 LIMPAR VALORES",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("#64748B", "#475569"),
            hover_color=("#475569", "#334155"),
            height=38,
            command=self._limpar
        )
        self.btn_limpar.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.btn_fechar = ctk.CTkButton(
            self.actions_frame,
            text="FECHAR",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("#94A3B8", "#1E293B"),
            hover_color=("#64748B", "#0F172A"),
            height=38,
            command=self.destroy
        )
        self.btn_fechar.grid(row=0, column=1, padx=(5, 0), sticky="ew")

    # =========================================================================
    # Lógica de Cálculos e Utilitários
    # =========================================================================

    def _obter_valor_base(self):
        """Extrai o valor float a partir do texto inserido (tratando separador brasileiro)."""
        raw_val = self.var_valor.get().strip()
        if not raw_val:
            return 0.0

        # Remove símbolo de moeda e espaços extras
        raw_val = raw_val.replace("R$", "").strip()

        try:
            # Identifica e trata formato brasileiro (pontos para milhares e vírgula para decimal)
            if "," in raw_val:
                # Remove os pontos de milhar e substitui a vírgula por ponto decimal
                raw_val = raw_val.replace(".", "").replace(",", ".")
            else:
                # Sem vírgula. Se tiver mais de um ponto ou ponto seguido de 3 dígitos, pode ser milhar
                # Ex: "1.000" -> 1000.0, mas "100.5" -> 100.5
                if "." in raw_val:
                    parts = raw_val.split(".")
                    if len(parts) > 2 or (len(parts) == 2 and len(parts[1]) == 3):
                        raw_val = raw_val.replace(".", "")
            
            return float(raw_val)
        except ValueError:
            return -1.0 # Sinaliza erro de formatação

    def _atualizar_calculos(self, *args):
        """Executa os cálculos com base no valor inserido e estado dos checkboxes."""
        valor = self._obter_valor_base()

        # Mapeamento das alíquotas e variáveis
        rate_configs = [
            (self.var_perfil_12, 0.2125, self.lbl_val_perfil_12, self.btn_copy_perfil_12),
            (self.var_perfil_7, 0.1625, self.lbl_val_perfil_7, self.btn_copy_perfil_7),
            (self.var_chapa_12, 0.2450, self.lbl_val_chapa_12, self.btn_copy_chapa_12),
            (self.var_icms_7, 0.1950, self.lbl_val_icms_7, self.btn_copy_icms_7),
        ]

        for var, pct, lbl_val, btn in rate_configs:
            if valor < 0:
                # Erro na formatação do valor de entrada
                lbl_val.configure(text="Valor inválido", text_color=("#DC2626", "#EF4444"))
                btn.configure(state="disabled")
            elif not var.get():
                # Checkbox desmarcado
                lbl_val.configure(text="---", text_color=("#94A3B8", "#64748B"))
                btn.configure(state="disabled")
            elif valor == 0:
                # Valor é zero ou vazio
                lbl_val.configure(text="R$ 0,00", text_color=("#94A3B8", "#64748B"))
                btn.configure(state="disabled")
            else:
                # Cálculo válido
                calc_val = valor * pct
                lbl_val.configure(text=self.format_moeda(calc_val), text_color=("#0F172A", "#FFFFFF"))
                btn.configure(state="normal")

    def format_moeda(self, valor):
        """Formata um float no formato monetário brasileiro: R$ X.XXX,XX"""
        formatted = f"R$ {valor:,.2f}"
        # Troca separadores: vírgula por X, ponto por vírgula, X por ponto
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")

    def _copiar_valor(self, key, pct, btn_widget):
        """Copia o valor calculado correspondente para a área de transferência."""
        valor_base = self._obter_valor_base()
        if valor_base <= 0:
            return

        calc_val = valor_base * pct
        # Formata o valor apenas com duas casas decimais e vírgula (formato brasileiro comum de número)
        # Ex: "212,50" ao invés de "R$ 212,50" para facilitar colar em sistemas ERP.
        str_para_copiar = f"{calc_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        self.clipboard_clear()
        self.clipboard_append(str_para_copiar)

        # Feedback visual temporário no botão
        btn_widget.configure(text="✅ Copiado!", fg_color="#16A34A", text_color="#FFFFFF")
        
        # Restaura o botão após 1.2 segundos
        self.after(1200, lambda: btn_widget.configure(
            text="📋 Copiar",
            fg_color=("#E2E8F0", "#2D323E"),
            text_color=("#0F172A", "#FFFFFF")
        ))

    def _limpar(self):
        """Limpa o campo de entrada e redefine os checkboxes para os valores padrão."""
        self.var_valor.set("")
        self.var_perfil_12.set(True)
        self.var_perfil_7.set(False)
        self.var_chapa_12.set(False)
        self.var_icms_7.set(False)
        self._atualizar_calculos()
        self.entry_valor.focus_set()

    # =========================================================================
    # Helpers de janela e ícone
    # =========================================================================

    def center_window(self):
        """Centraliza a janela na tela."""
        self.update_idletasks()
        width = 520
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def definir_icone(self):
        """Busca o ícone padrão do sistema e o associa à janela."""
        caminhos_tentativas = []
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            caminhos_tentativas.append(Path(sys._MEIPASS) / "Configurações" / "imagens" / "01.ico")
            caminhos_tentativas.append(Path(sys.executable).resolve().parent / "Configurações" / "imagens" / "01.ico")
        caminhos_tentativas.append(Path(__file__).resolve().parent.parent.parent / "Configurações" / "imagens" / "01.ico")

        for caminho_icone in caminhos_tentativas:
            if caminho_icone.exists():
                try:
                    self.iconbitmap(str(caminho_icone))
                    break
                except Exception:
                    pass
