import customtkinter as ctk
from tkinter import messagebox
from threading import Thread
from pathlib import Path
from datetime import datetime

from Interface.Uso_Consumo.Pedido.nf_uso_consumo_leitura import ler_nfe
from Interface.Uso_Consumo.Pedido.pedido_itens import iniciar


class JanelaPedidoItensModal(ctk.CTkToplevel):
    """
    Janela Modal (Toplevel) para exibição dos itens do Pedido de Uso e Consumo
    e acionamento da automação de geração de pedidos.
    """
    def __init__(self, parent, dados_nota, data_pedido: str):
        super().__init__(parent)
        self.dados_nota = dados_nota
        self.data_pedido = data_pedido
        self.itens = dados_nota.get("itens", [])
        self.nf = dados_nota.get("numero_nf", "N/D")

        # Configurações da Janela
        self.title(f"Itens do Pedido - NF nº {self.nf} | Data: {data_pedido}")
        self.geometry("900x650")
        self.minsize(750, 500)

        # Configurar Ícone do Sistema
        self.definir_icone()

        # Centralizar a janela na tela
        self.center_window()

        # Modal / Foco
        self.grab_set()
        self.focus_force()

        # Grid principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Textbox expande

        # 1. Header Frame
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color=("#F0F4F8", "#181B20"),
            corner_radius=0
        )
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.header_frame.grid_columnconfigure(0, weight=1)

        self.lbl_titulo = ctk.CTkLabel(
            self.header_frame,
            text="📋  ITENS DO PEDIDO DE USO E CONSUMO",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_titulo.grid(row=0, column=0, sticky="w", padx=25, pady=(15, 2))

        info_text = f"Emitente: {dados_nota.get('emitente', 'N/D')}  |  NF nº: {self.nf}  |  Data: {self.data_pedido}  |  Total: {len(self.itens)} item(ns)"
        self.lbl_info = ctk.CTkLabel(
            self.header_frame,
            text=info_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#1D4ED8", "#60A5FA")
        )
        self.lbl_info.grid(row=1, column=0, sticky="w", padx=25, pady=(0, 15))

        # 2. Textbox para exibição dos produtos
        self.textbox_itens = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color=("#E2E8F0", "#14171C"),
            border_color=("#94A3B8", "#2D323E"),
            border_width=1,
            text_color=("#0F172A", "#FFFFFF"),
            corner_radius=8,
            wrap="word"
        )
        self.textbox_itens.grid(row=1, column=0, sticky="nsew", padx=25, pady=15)

        # Preenchimento dos dados no Textbox
        self.preencher_textbox()

        # 3. Footer Bar com Botões de Ação
        self.footer_frame = ctk.CTkFrame(
            self,
            fg_color=("#F0F4F8", "#181B20"),
            corner_radius=0
        )
        self.footer_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        self.footer_frame.grid_columnconfigure(0, weight=1)

        # Botão Verde para Iniciar Pedido
        self.btn_iniciar_pedido = ctk.CTkButton(
            self.footer_frame,
            text="⚡  INICIAR PEDIDO NO SISTEMA",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#16A34A",
            hover_color="#15803D",
            text_color="#FFFFFF",
            height=45,
            corner_radius=8,
            command=self.iniciar_pedido_aut
        )
        self.btn_iniciar_pedido.grid(row=0, column=0, sticky="ew", padx=(25, 10), pady=15)

        # Botão Fechar
        self.btn_fechar = ctk.CTkButton(
            self.footer_frame,
            text="FECHAR",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#64748B", "#334155"),
            hover_color=("#475569", "#1E293B"),
            text_color="#FFFFFF",
            height=45,
            width=120,
            corner_radius=8,
            command=self.destroy
        )
        self.btn_fechar.grid(row=0, column=1, sticky="e", padx=(0, 25), pady=15)

    def center_window(self):
        self.update_idletasks()
        width = 900
        height = 650
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def preencher_textbox(self):
        self.textbox_itens.configure(state="normal")
        self.textbox_itens.delete("1.0", "end")

        divisor = "=" * 80 + "\n"
        sub_divisor = "-" * 80 + "\n"

        cabecalho = (
            f"{divisor}"
            f"EMITENTE   : {self.dados_nota.get('emitente', 'N/D')}\n"
            f"NÚMERO NF  : {self.nf}\n"
            f"DATA PEDIDO: {self.data_pedido}\n"
            f"TOTAL ITENS: {len(self.itens)}\n"
            f"{divisor}\n"
        )
        self.textbox_itens.insert("end", cabecalho)

        for idx, item in enumerate(self.itens, 1):
            texto_item = (
                f"[ITEM {idx} DE {len(self.itens)}]\n"
                f"  • Código        : {item.get('codigo', '')}\n"
                f"  • Descrição     : {item.get('descricao', '')}\n"
                f"  • NCM/SH        : {item.get('ncm_sh', '')}\n"
                f"  • Unidade       : {item.get('unidade', '')}\n"
                f"  • Quantidade    : {item.get('quantidade', 0)}\n"
                f"  • Valor Unitário: R$ {item.get('valor_unitario', 0.0):.2f}\n"
                f"{sub_divisor}\n"
            )
            self.textbox_itens.insert("end", texto_item)

        self.textbox_itens.configure(state="disabled")

    def iniciar_pedido_aut(self):
        if not self.itens:
            messagebox.showwarning("Nenhum Item", "Não há itens para gerar o pedido.", parent=self)
            return

        confirmar = messagebox.askyesno(
            "Iniciar Automação de Pedido",
            f"Deseja iniciar a automação do Pedido de {len(self.itens)} item(ns)?\n\n"
            f"• NF: {self.nf}\n"
            f"• Data: {self.data_pedido}\n\n"
            "Nota: A automação aguardará os botões do mouse (X2 para prosseguir / X para cancelar).",
            parent=self
        )

        if confirmar:
            self.btn_iniciar_pedido.configure(
                text="⏳ GERANDO PEDIDO EM ANDAMENTO...",
                fg_color="#D97706",
                hover_color="#B45309",
                state="disabled"
            )

            def runner():
                try:
                    iniciar(self.itens, self.nf, self.data_pedido)
                finally:
                    self.after(0, lambda: self.btn_iniciar_pedido.configure(
                        text="⚡  INICIAR PEDIDO NO SISTEMA",
                        fg_color="#16A34A",
                        hover_color="#15803D",
                        state="normal"
                    ))

            Thread(target=runner, daemon=True).start()

    def definir_icone(self):
        """Define o ícone oficial do sistema (01.ico)."""
        import sys
        caminhos_tentativas = []
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            caminhos_tentativas.append(Path(sys._MEIPASS) / "Configurações" / "imagens" / "01.ico")
            caminhos_tentativas.append(Path(sys.executable).resolve().parent / "Configurações" / "imagens" / "01.ico")
        caminhos_tentativas.append(Path(__file__).resolve().parent.parent.parent.parent / "Configurações" / "imagens" / "01.ico")

        for caminho_icone in caminhos_tentativas:
            if caminho_icone.exists():
                try:
                    self.after(200, lambda c=caminho_icone: self.iconbitmap(str(c)))
                    self.iconbitmap(str(caminho_icone))
                    break
                except Exception as e:
                    print(f"Aviso: Não foi possível definir o ícone na JanelaPedidoItensModal: {e}")


class PedidoFrame(ctk.CTkFrame):
    """
    Frame individual para a operação de Pedidos no módulo de Uso e Consumo.
    Contém campos para Chave de Acesso e Data do Pedido, com modal para exibição dos itens e disparo do processo.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.dados_nota_atual = None
        self.data_atual = ""

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

        # 1. Título da Operação
        self.lbl_titulo = ctk.CTkLabel(
            self.card,
            text="📋  GERAÇÃO DE PEDIDOS DE USO E CONSUMO",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_titulo.grid(row=0, column=0, sticky="w", padx=25, pady=(20, 5))

        self.lbl_desc = ctk.CTkLabel(
            self.card,
            text="Digite a chave de acesso da nota e a data do pedido. Pressione Enter para carregar os itens e gerar o pedido.",
            font=ctk.CTkFont(size=12),
            text_color=("#475569", "#9CA3AF")
        )
        self.lbl_desc.grid(row=1, column=0, sticky="w", padx=25, pady=(0, 15))

        # Divisor
        self.div = ctk.CTkFrame(self.card, height=1, fg_color=("#CBD5E1", "#2D323E"))
        self.div.grid(row=2, column=0, sticky="ew", padx=25, pady=(0, 20))

        # 2. Formulário de Entrada (Chave + Data)
        self.frame_inputs = ctk.CTkFrame(self.card, fg_color="transparent")
        self.frame_inputs.grid(row=3, column=0, sticky="ew", padx=25, pady=(0, 20))
        self.frame_inputs.grid_columnconfigure(0, weight=3)
        self.frame_inputs.grid_columnconfigure(1, weight=2)

        # Label e Entry da Chave
        self.lbl_chave = ctk.CTkLabel(
            self.frame_inputs,
            text="CHAVE DE ACESSO DA NOTA FISCAL:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        self.lbl_chave.grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.entry_chave = ctk.CTkEntry(
            self.frame_inputs,
            placeholder_text="🔑  Digite ou bipe a chave de acesso...",
            font=ctk.CTkFont(size=13),
            fg_color=("#E2E8F0", "#14171C"),
            border_color=("#94A3B8", "#2D323E"),
            text_color=("#0F172A", "#FFFFFF"),
            placeholder_text_color=("#475569", "#6B7280"),
            height=48,
            corner_radius=8
        )
        self.entry_chave.grid(row=1, column=0, sticky="ew", padx=(0, 12))
        self.entry_chave.bind("<Return>", lambda event: self.carregar_nota())

        # Label e Entry da Data
        self.lbl_data = ctk.CTkLabel(
            self.frame_inputs,
            text="DATA DO PEDIDO:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        self.lbl_data.grid(row=0, column=1, sticky="w", pady=(0, 6))

        self.entry_data = ctk.CTkEntry(
            self.frame_inputs,
            placeholder_text="📅  DD/MM/AAAA",
            font=ctk.CTkFont(size=13),
            fg_color=("#E2E8F0", "#14171C"),
            border_color=("#94A3B8", "#2D323E"),
            text_color=("#0F172A", "#FFFFFF"),
            placeholder_text_color=("#475569", "#6B7280"),
            height=48,
            corner_radius=8
        )
        self.entry_data.grid(row=1, column=1, sticky="ew", padx=(0, 12))
        self.entry_data.bind("<Return>", lambda event: self.carregar_nota())

        # Preenche automaticamente com a data de hoje (DD/MM/AAAA)
        self.entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))

        # Botão Carregar Nota
        self.btn_buscar = ctk.CTkButton(
            self.frame_inputs,
            text="🔍  CARREGAR NOTA",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            height=48,
            width=170,
            corner_radius=8,
            command=self.carregar_nota
        )
        self.btn_buscar.grid(row=1, column=2, sticky="e")

        # 3. Card Informativo de Status da Nota Atual
        self.card_status = ctk.CTkFrame(
            self.card,
            fg_color=("#E2E8F0", "#14171C"),
            border_color=("#94A3B8", "#2D323E"),
            border_width=1,
            corner_radius=8
        )
        self.card_status.grid(row=4, column=0, sticky="ew", padx=25, pady=(0, 25))
        self.card_status.grid_columnconfigure(0, weight=1)

        self.lbl_status = ctk.CTkLabel(
            self.card_status,
            text="ℹ️ Nenhum pedido carregado no momento.",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#475569", "#9CA3AF")
        )
        self.lbl_status.grid(row=0, column=0, sticky="w", padx=20, pady=18)

        # Botão para reabrir modal do pedido carregado
        self.btn_abrir_modal = ctk.CTkButton(
            self.card_status,
            text="📋  VISUALIZAR ITENS DO PEDIDO",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            height=38,
            corner_radius=6,
            command=self.abrir_janela_itens
        )

    def carregar_nota(self):
        """Lê a chave e a data e abre a janela modal para confirmação do pedido."""
        chave = self.entry_chave.get().strip()
        data = self.entry_data.get().strip()

        if not chave:
            messagebox.showwarning("Chave Não Informada", "Por favor, digite ou bipe a chave de acesso da nota.")
            return

        if not data:
            messagebox.showwarning("Data Não Informada", "Por favor, informe a data do pedido.")
            return

        try:
            dados = ler_nfe(chave)
            itens = dados.get("itens", [])

            if not itens:
                messagebox.showinfo("Nenhum Item", "A nota fiscal foi encontrada, porém não contém itens.")
                return

            self.dados_nota_atual = dados
            self.data_atual = data

            # Atualiza o card de status na aba
            self.lbl_status.configure(
                text=f"✅ Nota nº {dados.get('numero_nf')} carregada | Data: {data} | Emitente: {dados.get('emitente')} ({len(itens)} itens)",
                text_color=("#047857", "#10B981")
            )
            self.btn_abrir_modal.grid(row=0, column=1, sticky="e", padx=20, pady=12)

            # Abre a janela modal do pedido
            self.abrir_janela_itens()

        except FileNotFoundError as fnf_err:
            self.dados_nota_atual = None
            self.btn_abrir_modal.grid_forget()
            self.lbl_status.configure(
                text="❌ Nenhuma nota carregada.",
                text_color=("#DC2626", "#EF4444")
            )
            messagebox.showerror("Arquivo Não Encontrado", str(fnf_err))

        except Exception as e:
            self.dados_nota_atual = None
            self.btn_abrir_modal.grid_forget()
            self.lbl_status.configure(
                text="❌ Erro ao ler nota fiscal.",
                text_color=("#DC2626", "#EF4444")
            )
            messagebox.showerror("Erro de Leitura", f"Ocorreu um erro ao ler a Nota Fiscal:\n{str(e)}")

    def abrir_janela_itens(self):
        """Abre a janela modal Toplevel com a lista de itens do pedido."""
        if self.dados_nota_atual and self.data_atual:
            JanelaPedidoItensModal(self, self.dados_nota_atual, self.data_atual)
