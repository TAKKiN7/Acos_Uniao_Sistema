import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path

from Login.gerenciador_usuarios import (
    carregar_usuarios,
    salvar_ou_atualizar_usuario,
    remover_usuario
)

MODULE_LIST = [
    ("*", "⭐ Acesso Total (*)"),
    ("materia_prima", "📦 Notas de Matéria-Prima"),
    ("notas_cte", "🚚 Notas CTE"),
    ("uso_consumo", "🛒 Notas de Uso e Consumo"),
    ("almoxarifado", "🏭 Almoxarifado (Admin / Acesso Total no Estoque)"),
    ("almoxarifado_operador", "🏭 Almoxarifado (Operador / Somente Saída)"),
    ("faturamento", "📊 Faturamento"),
    ("ti", "💻 TI"),
    ("usuarios", "👤 Gestão de Usuários")
]


class JanelaConfirmarSenhaModal(ctk.CTkToplevel):
    """
    Modal de confirmação de senha para autorizar operações críticas
    (Criação, Alteração ou Exclusão de Usuários).
    """
    def __init__(self, parent, acao_nome="operação"):
        super().__init__(parent)
        self.acao_nome = acao_nome
        self.confirmado = False
        self.senha_digitada = None

        self.title("🔒 Autorização de Segurança")
        self.geometry("420x260")
        self.resizable(False, False)

        self.definir_icone()
        self.center_window()

        self.grab_set()
        self.focus_force()

        # Grid layout
        self.grid_columnconfigure(0, weight=1)

        # 1. Header
        self.lbl_titulo = ctk.CTkLabel(
            self,
            text="🔒 AUTORIZAÇÃO DE SEGURANÇA",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#EA580C", "#FF6B00")
        )
        self.lbl_titulo.pack(padx=20, pady=(20, 5))

        self.lbl_desc = ctk.CTkLabel(
            self,
            text=f"Digite sua senha para autorizar a {acao_nome}:",
            font=ctk.CTkFont(size=12),
            text_color=("#475569", "#9CA3AF"),
            wraplength=360
        )
        self.lbl_desc.pack(padx=20, pady=(0, 15))

        # 2. Entry de Senha
        self.entry_senha = ctk.CTkEntry(
            self,
            placeholder_text="🔑  Digite a senha de autorização...",
            show="*",
            font=ctk.CTkFont(size=13),
            fg_color=("#E2E8F0", "#14171C"),
            border_color=("#94A3B8", "#2D323E"),
            height=44
        )
        self.entry_senha.pack(fill="x", padx=30, pady=(0, 20))
        self.entry_senha.bind("<Return>", lambda event: self.confirmar())
        self.entry_senha.focus_set()

        # 3. Botões
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.pack(fill="x", padx=30, pady=(0, 15))
        self.frame_botoes.grid_columnconfigure((0, 1), weight=1)

        self.btn_confirmar = ctk.CTkButton(
            self.frame_botoes,
            text="CONFIRMAR",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#16A34A",
            hover_color="#15803D",
            height=40,
            command=self.confirmar
        )
        self.btn_confirmar.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.btn_cancelar = ctk.CTkButton(
            self.frame_botoes,
            text="CANCELAR",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#64748B", "#334155"),
            hover_color=("#475569", "#1E293B"),
            height=40,
            command=self.destroy
        )
        self.btn_cancelar.grid(row=0, column=1, padx=(5, 0), sticky="ew")

    def center_window(self):
        self.update_idletasks()
        width = 420
        height = 260
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def definir_icone(self):
        import sys
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

    def confirmar(self):
        senha = self.entry_senha.get().strip()
        if not senha:
            messagebox.showwarning("Senha Não Informada", "Por favor, digite a senha de autorização.", parent=self)
            return

        self.senha_digitada = senha
        self.confirmado = True
        self.destroy()


class UsuariosFrame(ctk.CTkFrame):
    """
    Aba de Gestão e Criação de Usuários.
    Permite visualizar, adicionar, alterar permissões e excluir usuários com autenticação de segurança.
    """
    def __init__(self, parent, usuario_logado="admin", dados_usuario=None):
        super().__init__(parent, fg_color="transparent")
        self.usuario_logado = usuario_logado
        self.dados_usuario = dados_usuario or {}
        self.usuario_em_edicao = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Header Section
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(20, 10))

        self.lbl_title = ctk.CTkLabel(
            self.header_frame,
            text="👤 GESTÃO DE USUÁRIOS E PERMISSÕES",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_title.pack(anchor="w")

        self.lbl_subtitle = ctk.CTkLabel(
            self.header_frame,
            text="Cadastre novos usuários, modifique senhas ou gerencie os privilégios de acesso por módulo.",
            font=ctk.CTkFont(size=13),
            text_color=("#475569", "#9CA3AF")
        )
        self.lbl_subtitle.pack(anchor="w", pady=(2, 0))

        # 2. Main Content Split View (Formulário à Esquerda | Lista à Direita)
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0, 20))
        self.content_frame.grid_columnconfigure(0, weight=4)  # Formulário
        self.content_frame.grid_columnconfigure(1, weight=5)  # Lista
        self.content_frame.grid_rowconfigure(0, weight=1)

        # ==========================================
        # PANEL ESQUERDO: Formulário Cadastro/Edição
        # ==========================================
        self.form_card = ctk.CTkFrame(
            self.content_frame,
            fg_color=("#F0F4F8", "#181B20"),
            border_color=("#94A3B8", "#262B34"),
            border_width=1,
            corner_radius=12
        )
        self.form_card.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=0)
        self.form_card.grid_columnconfigure(0, weight=1)

        self.lbl_form_titulo = ctk.CTkLabel(
            self.form_card,
            text="➕  CADASTRAR / EDITAR USUÁRIO",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#C2410C", "#FF6B00")
        )
        self.lbl_form_titulo.pack(anchor="w", padx=20, pady=(20, 15))

        # Campos do Formulário
        self.scroll_form = ctk.CTkScrollableFrame(self.form_card, fg_color="transparent")
        self.scroll_form.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        self.scroll_form.grid_columnconfigure(0, weight=1)

        # Login
        self.lbl_login = ctk.CTkLabel(self.scroll_form, text="LOGIN / USUÁRIO:", font=ctk.CTkFont(size=11, weight="bold"), text_color=("#475569", "#9CA3AF"))
        self.lbl_login.pack(anchor="w", pady=(5, 2))
        self.entry_login = ctk.CTkEntry(self.scroll_form, placeholder_text="Ex: joao.silva", height=40)
        self.entry_login.pack(fill="x", pady=(0, 10))

        # Senha
        self.lbl_senha = ctk.CTkLabel(self.scroll_form, text="SENHA:", font=ctk.CTkFont(size=11, weight="bold"), text_color=("#475569", "#9CA3AF"))
        self.lbl_senha.pack(anchor="w", pady=(5, 2))
        self.entry_senha = ctk.CTkEntry(self.scroll_form, placeholder_text="Digite a senha de acesso...", show="*", height=40)
        self.entry_senha.pack(fill="x", pady=(0, 10))

        # Nome Completo
        self.lbl_nome = ctk.CTkLabel(self.scroll_form, text="NOME EXIBIÇÃO / NOME COMPLETO:", font=ctk.CTkFont(size=11, weight="bold"), text_color=("#475569", "#9CA3AF"))
        self.lbl_nome.pack(anchor="w", pady=(5, 2))
        self.entry_nome = ctk.CTkEntry(self.scroll_form, placeholder_text="Ex: João da Silva", height=40)
        self.entry_nome.pack(fill="x", pady=(0, 10))

        # Perfil
        self.lbl_perfil = ctk.CTkLabel(self.scroll_form, text="PERFIL DO USUÁRIO:", font=ctk.CTkFont(size=11, weight="bold"), text_color=("#475569", "#9CA3AF"))
        self.lbl_perfil.pack(anchor="w", pady=(5, 2))
        self.combo_perfil = ctk.CTkOptionMenu(
            self.scroll_form,
            values=["operador", "admin"],
            height=40,
            fg_color=("#0052FF", "#0052FF"),
            button_color=("#003EB8", "#003EB8")
        )
        self.combo_perfil.set("operador")
        self.combo_perfil.pack(fill="x", pady=(0, 15))

        # Módulos Permitidos
        self.lbl_modulos = ctk.CTkLabel(self.scroll_form, text="MÓDULOS PERMITIDOS:", font=ctk.CTkFont(size=11, weight="bold"), text_color=("#C2410C", "#FF6B00"))
        self.lbl_modulos.pack(anchor="w", pady=(5, 5))

        self.modulos_vars = {}
        for chave_mod, rotulo_mod in MODULE_LIST:
            var = ctk.BooleanVar(value=False)
            chk = ctk.CTkCheckBox(
                self.scroll_form,
                text=rotulo_mod,
                variable=var,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color="#0052FF",
                hover_color="#003EB8",
                checkbox_width=20,
                checkbox_height=20
            )
            chk.pack(anchor="w", pady=4, padx=5)
            self.modulos_vars[chave_mod] = var

        # Botões de Ação do Formulário
        self.frame_btn_form = ctk.CTkFrame(self.form_card, fg_color="transparent")
        self.frame_btn_form.pack(fill="x", padx=15, pady=15)
        self.frame_btn_form.grid_columnconfigure((0, 1), weight=1)

        self.btn_salvar = ctk.CTkButton(
            self.frame_btn_form,
            text="💾  SALVAR USUÁRIO",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#16A34A",
            hover_color="#15803D",
            height=44,
            command=self.salvar_usuario_acao
        )
        self.btn_salvar.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        self.btn_limpar = ctk.CTkButton(
            self.frame_btn_form,
            text="🔄  LIMPAR",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=("#64748B", "#334155"),
            hover_color=("#475569", "#1E293B"),
            height=44,
            command=self.limpar_formulario
        )
        self.btn_limpar.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        # ==========================================
        # PANEL DIREITO: Lista de Usuários Existentes
        # ==========================================
        self.list_card = ctk.CTkFrame(
            self.content_frame,
            fg_color=("#F0F4F8", "#181B20"),
            border_color=("#94A3B8", "#262B34"),
            border_width=1,
            corner_radius=12
        )
        self.list_card.grid(row=0, column=1, sticky="nsew", padx=(15, 0), pady=0)
        self.list_card.grid_columnconfigure(0, weight=1)
        self.list_card.grid_rowconfigure(1, weight=1)

        self.lbl_list_titulo = ctk.CTkLabel(
            self.list_card,
            text="📋  USUÁRIOS CADASTRADOS NO SISTEMA",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_list_titulo.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 15))

        self.scroll_usuarios = ctk.CTkScrollableFrame(self.list_card, fg_color="transparent")
        self.scroll_usuarios.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.scroll_usuarios.grid_columnconfigure(0, weight=1)

        # Carrega a lista inicial de usuários
        self.atualizar_lista_usuarios()

    def verificar_senha_autorizacao(self, acao_nome) -> bool:
        """Abre o modal pedindo a senha de autorização antes de salvar ou excluir."""
        modal = JanelaConfirmarSenhaModal(self, acao_nome=acao_nome)
        self.wait_window(modal)

        if not modal.confirmado or not modal.senha_digitada:
            return False

        senha_digitada = modal.senha_digitada
        usuarios = carregar_usuarios()

        # Verifica se a senha corresponde ao usuário logado ou a qualquer usuário administrador
        for usr_login, usr_data in usuarios.items():
            if str(usr_data.get("senha")) == senha_digitada:
                # Se for a senha do usuário logado ou de um admin, autoriza
                if usr_login == self.usuario_logado or usr_data.get("perfil") == "admin":
                    return True

        messagebox.showerror("Senha Incorreta", "Senha de autorização inválida! Ação cancelada.")
        return False

    def salvar_usuario_acao(self):
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()
        nome = self.entry_nome.get().strip()
        perfil = self.combo_perfil.get()

        if not login:
            messagebox.showwarning("Campo Obrigatório", "Por favor, informe o login do usuário.")
            return

        if not senha:
            messagebox.showwarning("Campo Obrigatório", "Por favor, informe a senha do usuário.")
            return

        if not nome:
            nome = login

        # Coleta módulos selecionados
        modulos_selecionados = []
        if self.modulos_vars["*"].get():
            modulos_selecionados = ["*"]
        else:
            for mod_k, var in self.modulos_vars.items():
                if mod_k != "*" and var.get():
                    modulos_selecionados.append(mod_k)

        # Pede confirmação por senha de segurança
        acao_desc = f"alteração do usuário '{login}'" if self.usuario_em_edicao else f"criação do usuário '{login}'"
        if not self.verificar_senha_autorizacao(acao_desc):
            return

        sucesso = salvar_ou_atualizar_usuario(login, senha, nome, perfil, modulos_selecionados)

        if sucesso:
            messagebox.showinfo("Sucesso", f"Usuário '{login}' salvo com sucesso!")
            self.limpar_formulario()
            self.atualizar_lista_usuarios()
        else:
            messagebox.showerror("Erro", "Não foi possível salvar o usuário no arquivo JSON.")

    def excluir_usuario_acao(self, login):
        confirmar = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir permanentemente o usuário '{login}'?"
        )
        if not confirmar:
            return

        # Pede confirmação por senha de segurança
        if not self.verificar_senha_autorizacao(f"exclusão do usuário '{login}'"):
            return

        sucesso = remover_usuario(login)
        if sucesso:
            messagebox.showinfo("Sucesso", f"Usuário '{login}' removido com sucesso!")
            if self.usuario_em_edicao == login:
                self.limpar_formulario()
            self.atualizar_lista_usuarios()
        else:
            messagebox.showerror("Erro", "Não foi possível remover o usuário.")

    def carregar_usuario_para_edicao(self, login, dados):
        self.usuario_em_edicao = login
        self.lbl_form_titulo.configure(text=f"✏️  EDITANDO USUÁRIO: {login}")

        self.entry_login.configure(state="normal")
        self.entry_login.delete(0, "end")
        self.entry_login.insert(0, login)

        self.entry_senha.delete(0, "end")
        self.entry_senha.insert(0, dados.get("senha", ""))

        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, dados.get("nome", login))

        self.combo_perfil.set(dados.get("perfil", "operador"))

        modulos_user = dados.get("modulos", [])
        for mod_k, var in self.modulos_vars.items():
            var.set("*" in modulos_user or mod_k in modulos_user)

    def limpar_formulario(self):
        self.usuario_em_edicao = None
        self.lbl_form_titulo.configure(text="➕  CADASTRAR / EDITAR USUÁRIO")

        self.entry_login.configure(state="normal")
        self.entry_login.delete(0, "end")
        self.entry_senha.delete(0, "end")
        self.entry_nome.delete(0, "end")
        self.combo_perfil.set("operador")

        for var in self.modulos_vars.values():
            var.set(False)

    def atualizar_lista_usuarios(self):
        # Limpa widgets existentes no scroll
        for widget in self.scroll_usuarios.winfo_children():
            widget.destroy()

        usuarios = carregar_usuarios()

        if not usuarios:
            lbl_vazio = ctk.CTkLabel(
                self.scroll_usuarios,
                text="Nenhum usuário cadastrado.",
                font=ctk.CTkFont(size=12),
                text_color=("#64748B", "#94A3B8")
            )
            lbl_vazio.pack(pady=20)
            return

        for login, dados in usuarios.items():
            card = ctk.CTkFrame(
                self.scroll_usuarios,
                fg_color=("#E2E8F0", "#14171C"),
                border_color=("#CBD5E1", "#2D323E"),
                border_width=1,
                corner_radius=8
            )
            card.pack(fill="x", pady=5)
            card.grid_columnconfigure(1, weight=1)

            perfil = dados.get("perfil", "operador")
            cor_badge = "#16A34A" if perfil == "admin" else "#0052FF"
            badge_text = "🟢 ADMIN" if perfil == "admin" else "🔵 OPERADOR"

            # Badge / Perfil
            lbl_badge = ctk.CTkLabel(
                card,
                text=badge_text,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=cor_badge
            )
            lbl_badge.grid(row=0, column=0, padx=12, pady=(10, 2), sticky="w")

            # Nome e Login
            nome_txt = f"{dados.get('nome', login)} ({login})"
            lbl_name = ctk.CTkLabel(
                card,
                text=nome_txt,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=("#0F172A", "#FFFFFF")
            )
            lbl_name.grid(row=1, column=0, columnspan=2, padx=12, pady=(0, 2), sticky="w")

            # Módulos autorizados
            mods = dados.get("modulos", [])
            mods_txt = "Acesso Total (*)" if "*" in mods else (", ".join(mods) if mods else "Nenhum módulo")
            lbl_mods = ctk.CTkLabel(
                card,
                text=f"Módulos: {mods_txt}",
                font=ctk.CTkFont(size=11),
                text_color=("#64748B", "#9CA3AF")
            )
            lbl_mods.grid(row=2, column=0, columnspan=2, padx=12, pady=(0, 10), sticky="w")

            # Botões Editar e Excluir
            frame_acoes = ctk.CTkFrame(card, fg_color="transparent")
            frame_acoes.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="e")

            btn_edit = ctk.CTkButton(
                frame_acoes,
                text="✏️",
                width=36,
                height=34,
                font=ctk.CTkFont(size=12),
                fg_color="#1D4ED8",
                hover_color="#1E40AF",
                command=lambda l=login, d=dados: self.carregar_usuario_para_edicao(l, d)
            )
            btn_edit.pack(side="left", padx=2)

            btn_del = ctk.CTkButton(
                frame_acoes,
                text="🗑️",
                width=36,
                height=34,
                font=ctk.CTkFont(size=12),
                fg_color="#DC2626",
                hover_color="#B91C1C",
                command=lambda l=login: self.excluir_usuario_acao(l)
            )
            btn_del.pack(side="left", padx=2)
