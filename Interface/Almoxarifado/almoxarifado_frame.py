import customtkinter as ctk
from tkinter.ttk import Treeview, Style
from tkinter import messagebox as msg

from Database.estoque import database
from Interface.Almoxarifado.adicionar_frame import AdicionarFrame
from Interface.Almoxarifado.editar_frame import EditarFrame
from Interface.Almoxarifado.entrada_frame import EntradaFrame
from Interface.Almoxarifado.saida_frame import SaidaFrame

class AlmoxarifadoFrame(ctk.CTkFrame):
    """
    Frame principal do módulo de Almoxarifado.
    Substitui a antiga janela de Estoque. Trabalha 100% via CTkFrame sem janelas secundárias.
    """
    def __init__(self, parent, usuario_logado="Operador Sistema", dados_usuario=None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.usuario_logado = usuario_logado
        self.dados_usuario = dados_usuario or {}
        
        # Permissões do usuário (Admin vs Operador)
        self.perfil = self.dados_usuario.get("perfil", "operador").lower()
        self.is_admin = (self.perfil == "admin" or usuario_logado == "tk" or "*" in self.dados_usuario.get("modulos", []))

        # Configuração do Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Referência para o container de formulários integrados
        self.frame_formulario_ativo = None

        # Construção da Interface
        self._criar_header()
        self._criar_painel_pesquisa()
        self._criar_container_tabela()
        self._criar_painel_botoes()
        self._criar_container_overlay_formulario()

        # Indicador de carregamento preguiçoso (Lazy loading)
        self.tabela_carregada = False

    def carregar_se_necessario(self):
        """Carrega os dados do banco apenas quando o usuário realmente abre a aba do Almoxarifado."""
        if not self.tabela_carregada:
            self.tabela_carregada = True
            self.atualizar_tabela()

    def _criar_header(self):
        """Cabeçalho superior da aba Almoxarifado."""
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
            text="Gestão de Almoxarifado",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_titulo.pack(anchor="w", pady=(2, 0))

    def _criar_painel_pesquisa(self):
        """Barra de pesquisa e recarregamento da tabela."""
        self.panel_top = ctk.CTkFrame(
            self,
            fg_color=("#F0F4F8", "#1E2228"),
            border_color=("#94A3B8", "#2D323E"),
            border_width=1,
            corner_radius=12
        )
        self.panel_top.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 15))
        self.panel_top.grid_columnconfigure(0, weight=1)

        box_search = ctk.CTkFrame(self.panel_top, fg_color="transparent")
        box_search.pack(fill="x", padx=20, pady=12)

        self.entry_pesquisa = ctk.CTkEntry(
            box_search,
            placeholder_text="🔍  Pesquisar produto por nome ou código...",
            font=ctk.CTkFont(size=13),
            fg_color=("#E2E8F0", "#14171C"),
            border_color=("#94A3B8", "#2D323E"),
            text_color=("#0F172A", "#FFFFFF"),
            placeholder_text_color=("#475569", "#6B7280"),
            height=40,
            corner_radius=8
        )
        self.entry_pesquisa.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_pesquisa.bind("<Return>", lambda e: self.pesquisar())

        btn_buscar = ctk.CTkButton(
            box_search,
            text="Buscar",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#1D4ED8",
            hover_color="#1E40AF",
            text_color="#FFFFFF",
            width=90,
            height=40,
            corner_radius=8,
            command=self.pesquisar
        )
        btn_buscar.pack(side="left", padx=(0, 8))

        btn_atualizar = ctk.CTkButton(
            box_search,
            text="🔃 Recarregar",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#475569",
            hover_color="#334155",
            text_color="#FFFFFF",
            width=110,
            height=40,
            corner_radius=8,
            command=self.atualizar_tabela
        )
        btn_atualizar.pack(side="left")

    def _criar_container_tabela(self):
        """Container central contendo a Treeview do Almoxarifado."""
        self.container_tabela = ctk.CTkFrame(
            self,
            fg_color=("#F0F4F8", "#1E2228"),
            border_color=("#94A3B8", "#2D323E"),
            border_width=1,
            corner_radius=12
        )
        self.container_tabela.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 15))
        self.container_tabela.grid_columnconfigure(0, weight=1)
        self.container_tabela.grid_rowconfigure(0, weight=1)

        # Treeview de Produtos
        self.tabela = TabelaAlmoxarifado(self.container_tabela)
        self.tabela.pack(fill="both", expand=True, padx=15, pady=15)

        # Evento de duplo clique na linha
        if self.is_admin:
            self.tabela.bind("<Double-Button-1>", lambda e: self.abrir_entrada())
        else:
            self.tabela.bind("<Double-Button-1>", lambda e: self.abrir_saida())

    def _criar_painel_botoes(self):
        """Barra inferior de ações (Adicionar, Editar, Remover, Entrada, Saída)."""
        self.panel_botoes = ctk.CTkFrame(
            self,
            fg_color=("#F0F4F8", "#1E2228"),
            border_color=("#94A3B8", "#2D323E"),
            border_width=1,
            corner_radius=12
        )
        self.panel_botoes.grid(row=3, column=0, sticky="ew", padx=30, pady=(0, 20))
        self.panel_botoes.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        box_btns = ctk.CTkFrame(self.panel_botoes, fg_color="transparent")
        box_btns.pack(fill="x", padx=15, pady=12)
        box_btns.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        if self.is_admin:
            # Botão 1: Adicionar
            btn_add = ctk.CTkButton(
                box_btns,
                text="➕  Adicionar Produto",
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color="#16A34A",
                hover_color="#15803D",
                text_color="#FFFFFF",
                height=40,
                corner_radius=8,
                command=self.abrir_adicionar
            )
            btn_add.grid(row=0, column=0, padx=5, sticky="ew")

            # Botão 2: Editar
            btn_edit = ctk.CTkButton(
                box_btns,
                text="✏️  Editar",
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color="#2563EB",
                hover_color="#1D4ED8",
                text_color="#FFFFFF",
                height=40,
                corner_radius=8,
                command=self.abrir_editar
            )
            btn_edit.grid(row=0, column=1, padx=5, sticky="ew")

            # Botão 3: Remover
            btn_del = ctk.CTkButton(
                box_btns,
                text="🗑️  Remover",
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color="#DC2626",
                hover_color="#B91C1C",
                text_color="#FFFFFF",
                height=40,
                corner_radius=8,
                command=self.remover_produto
            )
            btn_del.grid(row=0, column=2, padx=5, sticky="ew")

            # Botão 4: Entrada
            btn_ent = ctk.CTkButton(
                box_btns,
                text="📥  Entrada",
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color="#0891B2",
                hover_color="#0E7490",
                text_color="#FFFFFF",
                height=40,
                corner_radius=8,
                command=self.abrir_entrada
            )
            btn_ent.grid(row=0, column=3, padx=5, sticky="ew")

        # Botão Saída (Visível para todos)
        btn_sai = ctk.CTkButton(
            box_btns,
            text="📤  Saída",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#EA580C",
            hover_color="#C2410C",
            text_color="#FFFFFF",
            height=40,
            corner_radius=8,
            command=self.abrir_saida
        )
        col_saida = 4 if self.is_admin else 0
        btn_sai.grid(row=0, column=col_saida, padx=5, sticky="ew")

    def _criar_container_overlay_formulario(self):
        """Container para exibição inline dos formulários de ação (sem CTkToplevel)."""
        self.overlay_formulario = ctk.CTkFrame(self, fg_color="transparent")
        # Por padrão não está posicionado (aparece sob demanda)

    def exibir_formulario_inline(self, frame_classe, *args, **kwargs):
        """Exibe o formulário de ação inline sobre o conteúdo (sem janela secundária)."""
        if self.frame_formulario_ativo:
            self.frame_formulario_ativo.destroy()

        self.overlay_formulario.grid(row=1, column=0, rowspan=3, sticky="nsew", padx=30, pady=(0, 20))
        self.overlay_formulario.grid_columnconfigure(0, weight=1)
        self.overlay_formulario.grid_rowconfigure(0, weight=1)

        self.frame_formulario_ativo = frame_classe(
            self.overlay_formulario,
            *args,
            callback_sucesso=self.fechar_formulario_e_atualizar,
            callback_cancelar=self.fechar_formulario,
            **kwargs
        )
        self.frame_formulario_ativo.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.75)
        self.frame_formulario_ativo.lift()

    def fechar_formulario(self):
        """Oculta o formulário inline."""
        if self.frame_formulario_ativo:
            self.frame_formulario_ativo.destroy()
            self.frame_formulario_ativo = None
        self.overlay_formulario.grid_forget()

    def fechar_formulario_e_atualizar(self):
        """Oculta o formulário inline e atualiza a tabela."""
        self.fechar_formulario()
        self.atualizar_tabela()

    # --- Ações Operacionais ---
    def abrir_adicionar(self):
        self.exibir_formulario_inline(AdicionarFrame)

    def abrir_editar(self):
        item = self.tabela.selection()
        if not item:
            msg.showwarning("Seleção Requerida", "Por favor, selecione um produto na tabela para editar.")
            return
        values = self.tabela.item(item)["values"]
        self.exibir_formulario_inline(EditarFrame, values=values)

    def abrir_entrada(self):
        item = self.tabela.selection()
        if not item:
            msg.showwarning("Seleção Requerida", "Por favor, selecione um produto na tabela para dar entrada.")
            return
        values = self.tabela.item(item)["values"]
        self.exibir_formulario_inline(EntradaFrame, values=values)

    def abrir_saida(self):
        item = self.tabela.selection()
        if not item:
            msg.showwarning("Seleção Requerida", "Por favor, selecione um produto na tabela para dar saída.")
            return
        values = self.tabela.item(item)["values"]
        self.exibir_formulario_inline(SaidaFrame, values=values)

    def remover_produto(self):
        item = self.tabela.selection()
        if not item:
            msg.showwarning("Seleção Requerida", "Por favor, selecione um produto na tabela para remover.")
            return
        elif len(item) > 1:
            msg.showwarning("Seleção Múltipla", "Selecione apenas um produto por vez para remoção.")
            return

        values = self.tabela.item(item)["values"]
        codigo = values[0]
        produto = values[1]

        confirmar = msg.askyesno("Confirmar Remoção", f"Tem certeza que deseja remover permanentemente o produto:\n\n• Cód: {codigo}\n• Item: {produto}?")
        if not confirmar:
            return

        res = database.remover_produto(codigo, master=self)
        if res and "não" in str(res).lower():
            msg.showerror("Falha na Remoção", res)
        else:
            msg.showinfo("Removido", f"Produto '{produto}' removido com sucesso!")
            self.atualizar_tabela()

    def pesquisar(self):
        termo = self.entry_pesquisa.get().strip()
        if not termo:
            self.atualizar_tabela()
            return
        produtos = database.pesquisar_produtos(termo, master=self)
        self.tabela.carregar_registros(produtos)

    def atualizar_tabela(self):
        self.entry_pesquisa.delete(0, "end")
        produtos = database.listar_produtos(master=self)
        self.tabela.carregar_registros(produtos)


class TabelaAlmoxarifado(Treeview):
    """Componente personalizado Treeview para o Almoxarifado."""
    def __init__(self, master):
        super().__init__(master, show="headings")
        self.style = Style()
        self.style.theme_use("clam")
        self.configurar_estilos()

    def configurar_estilos(self):
        self["columns"] = ("codigo", "item", "estoque")

        self.column("codigo", width=100, stretch=False, anchor="center")
        self.column("item", width=450, stretch=True, anchor="w")
        self.column("estoque", width=120, stretch=False, anchor="center")

        self.heading("codigo", text="Código")
        self.heading("item", text="Item / Produto")
        self.heading("estoque", text="Estoque Atual")

        self.tag_configure("linha_1", background="#1E293B", foreground="#FFFFFF")
        self.tag_configure("linha_2", background="#2A384E", foreground="#FFFFFF")
        self.tag_configure("estoque_baixo", background="#991B1B", foreground="#FFFFFF")

        self.style.configure(
            "Treeview",
            font=("Segoe UI", 11),
            rowheight=34,
            background="#1E293B",
            fieldbackground="#1E293B",
            foreground="#FFFFFF",
            borderwidth=0
        )

        self.style.map(
            "Treeview",
            background=[("selected", "#2563EB")],
            foreground=[("selected", "#FFFFFF")]
        )

        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 12, "bold"),
            background="#081233",
            foreground="#FFFFFF",
            relief="flat"
        )

        self.style.map(
            "Treeview.Heading",
            background=[("active", "#2563EB")]
        )

    def carregar_registros(self, registros):
        """Limpa e carrega os registros na Treeview."""
        for item in self.get_children():
            self.delete(item)

        if not registros:
            return

        for index, reg in enumerate(registros):
            cod = reg[0]
            nome = str(reg[1]).upper()
            estoque = int(reg[2]) if reg[2] is not None else 0

            valores = (cod, nome, estoque)

            if estoque < 10:
                tag = "estoque_baixo"
            elif index % 2 != 0:
                tag = "linha_1"
            else:
                tag = "linha_2"

            self.insert("", "end", values=valores, tags=(tag,))
