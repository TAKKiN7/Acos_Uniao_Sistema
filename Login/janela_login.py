import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
from Login.gerenciador_usuarios import carregar_usuarios

# Carrega dicionário de usuários dinamicamente a partir de Configurações/usuarios.json
USUARIOS_SISTEMA = carregar_usuarios()
USUARIOS_PADRAO = USUARIOS_SISTEMA

class JanelaLogin(ctk.CTk):
    """
    Interface de Login moderna e compacta para o Sistema AÇOS UNIÃO.
    Estilizada de acordo com a paleta de cores oficial da empresa (Laranja, Azul e Grafite Metálico).
    Controla acessos por perfis e módulos individuais.
    """
    # Paleta de Cores Oficial AÇOS UNIÃO
    COR_FUNDO = "#0B0D11"          # Fundo Grafite/Aço Escuro
    COR_CARD = "#14171E"           # Card Aço Escuro
    COR_BORDA_CARD = "#232834"     # Borda sutil do Card
    COR_INPUT_BG = "#090B0E"       # Fundo dos campos de texto
    COR_INPUT_BORDA = "#202530"    # Borda dos campos
    COR_LARANJA = "#EA580C"        # Laranja Institucional Aços União
    COR_LARANJA_HOVER = "#C2410C"  # Laranja Hover
    COR_AZUL = "#0052FF"           # Azul Metálico Institucional Aços União
    COR_AZUL_HOVER = "#003EB8"     # Azul Hover
    COR_TEXTO_MUTED = "#8E99A8"    # Texto Secundário / Slogan
    COR_TEXTO_ROTULO = "#A0AEC0"   # Rótulo de campos

    def __init__(self, usuarios_dict=None, callback_sucesso=None):
        super().__init__()

        # Define dicionário de usuários e suas permissões
        self.usuarios_dict = usuarios_dict if usuarios_dict is not None else carregar_usuarios()
        self.callback_sucesso = callback_sucesso

        # Configurações da Janela Compacta (390x510)
        self.title("Acesso ao Sistema - AÇOS UNIÃO")
        self.geometry("390x510")
        self.resizable(False, False)
        
        # Centralizar a janela na tela
        self.centralizar_janela(390, 510)

        # Configurar Ícone do Sistema
        self.definir_icone()

        # Modo de aparência escuro por padrão
        ctk.set_appearance_mode("Dark")

        # Container Principal de fundo escuro
        self.bg_frame = ctk.CTkFrame(self, fg_color=self.COR_FUNDO, corner_radius=0)
        self.bg_frame.pack(fill="both", expand=True)

        # Card de Login centralizado e compacto
        self.card_frame = ctk.CTkFrame(
            self.bg_frame,
            fg_color=self.COR_CARD,
            border_color=self.COR_BORDA_CARD,
            border_width=1,
            corner_radius=14,
            width=340,
            height=450
        )
        self.card_frame.pack_propagate(False)
        self.card_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Construir elementos visuais da interface de login
        self._criar_marca_empresa()
        self._criar_cabecalho()
        self._criar_campo_usuario()
        self._criar_campo_senha()
        self._criar_opcoes_adicionais()
        self._criar_mensagem_status()
        self._criar_botao_entrar()

        # Tecla ENTER para submeter login
        self.bind("<Return>", lambda event: self.autenticar_usuario())

    def centralizar_janela(self, largura, altura):
        """Centraliza a janela na tela do usuário."""
        self.update_idletasks()
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        pos_x = (largura_tela // 2) - (largura // 2)
        pos_y = (altura_tela // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    def _criar_marca_empresa(self):
        """Logotipo e Slogan da empresa AÇOS UNIÃO nas cores institucionais."""
        box_brand = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        box_brand.pack(anchor="w", padx=24, pady=(20, 0))

        # Título "AÇOS UNIÃO" (AÇOS em azul e UNIÃO em laranja)
        lbl_brand_acos = ctk.CTkLabel(
            box_brand,
            text="AÇOS ",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=self.COR_AZUL
        )
        lbl_brand_acos.pack(side="left")

        lbl_brand_uniao = ctk.CTkLabel(
            box_brand,
            text="UNIÃO",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
            text_color=self.COR_LARANJA
        )
        lbl_brand_uniao.pack(side="left")

        # Slogan "PRODUZIR E DISTRIBUIR"
        lbl_slogan = ctk.CTkLabel(
            self.card_frame,
            text="PRODUZIR E DISTRIBUIR",
            font=ctk.CTkFont(family="Segoe UI", size=8, weight="bold"),
            text_color=self.COR_TEXTO_MUTED
        )
        lbl_slogan.pack(anchor="w", padx=24, pady=(0, 10))

        # Linha divisória sutil em Laranja
        divisor = ctk.CTkFrame(self.card_frame, height=2, fg_color=self.COR_LARANJA, corner_radius=1)
        divisor.pack(fill="x", padx=24, pady=(0, 12))

    def _criar_cabecalho(self):
        """Título e subtítulo do formulário de acesso."""
        lbl_titulo = ctk.CTkLabel(
            self.card_frame,
            text="Acesso ao Sistema",
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            text_color="#FFFFFF"
        )
        lbl_titulo.pack(anchor="w", padx=24, pady=(0, 1))

        lbl_subtitulo = ctk.CTkLabel(
            self.card_frame,
            text="Insira suas credenciais para acessar o sistema.",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=self.COR_TEXTO_MUTED,
            wraplength=290,
            justify="left"
        )
        lbl_subtitulo.pack(anchor="w", padx=24, pady=(0, 14))

    def _criar_campo_usuario(self):
        """Campo de entrada para o nome de usuário."""
        lbl_user = ctk.CTkLabel(
            self.card_frame,
            text="USUÁRIO",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=self.COR_TEXTO_ROTULO
        )
        lbl_user.pack(anchor="w", padx=24, pady=(0, 3))

        # Container do input de usuário
        self.user_box = ctk.CTkFrame(
            self.card_frame,
            fg_color=self.COR_INPUT_BG,
            border_color=self.COR_INPUT_BORDA,
            border_width=1,
            corner_radius=7,
            height=38
        )
        self.user_box.pack(fill="x", padx=24, pady=(0, 10))
        self.user_box.pack_propagate(False)

        # Ícone do usuário
        lbl_icon = ctk.CTkLabel(
            self.user_box,
            text="👤",
            font=ctk.CTkFont(size=12),
            text_color=self.COR_AZUL,
            width=30
        )
        lbl_icon.pack(side="left", padx=(6, 0))

        # Input text
        self.entry_usuario = ctk.CTkEntry(
            self.user_box,
            placeholder_text="ex: operador",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color="transparent",
            border_width=0,
            text_color="#FFFFFF",
            placeholder_text_color="#4B5563"
        )
        self.entry_usuario.pack(side="left", fill="both", expand=True, padx=(0, 8))

    def _criar_campo_senha(self):
        """Campo de entrada para a senha com opção de alternar visibilidade."""
        lbl_pass = ctk.CTkLabel(
            self.card_frame,
            text="SENHA",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color=self.COR_TEXTO_ROTULO
        )
        lbl_pass.pack(anchor="w", padx=24, pady=(0, 3))

        # Container do input de senha
        self.pass_box = ctk.CTkFrame(
            self.card_frame,
            fg_color=self.COR_INPUT_BG,
            border_color=self.COR_INPUT_BORDA,
            border_width=1,
            corner_radius=7,
            height=38
        )
        self.pass_box.pack(fill="x", padx=24, pady=(0, 4))
        self.pass_box.pack_propagate(False)

        # Ícone de cadeado
        lbl_icon = ctk.CTkLabel(
            self.pass_box,
            text="🔒",
            font=ctk.CTkFont(size=12),
            text_color=self.COR_LARANJA,
            width=30
        )
        lbl_icon.pack(side="left", padx=(6, 0))

        # Entry da Senha (show="*")
        self.entry_senha = ctk.CTkEntry(
            self.pass_box,
            placeholder_text="••••••••",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            show="*",
            fg_color="transparent",
            border_width=0,
            text_color="#FFFFFF",
            placeholder_text_color="#4B5563"
        )
        self.entry_senha.pack(side="left", fill="both", expand=True, padx=(0, 4))

        # Botão olho para exibir/ocultar senha
        self.senha_visivel = False
        self.btn_olho = ctk.CTkButton(
            self.pass_box,
            text="👁",
            width=26,
            height=26,
            fg_color="transparent",
            hover_color="#1E232D",
            text_color=self.COR_TEXTO_MUTED,
            font=ctk.CTkFont(size=12),
            command=self.alternar_visibilidade_senha
        )
        self.btn_olho.pack(side="right", padx=4)

    def alternar_visibilidade_senha(self):
        """Alterna a exibição dos caracteres da senha entre oculta (*) e visível."""
        if self.senha_visivel:
            self.entry_senha.configure(show="*")
            self.btn_olho.configure(text="👁", text_color=self.COR_TEXTO_MUTED)
            self.senha_visivel = False
        else:
            self.entry_senha.configure(show="")
            self.btn_olho.configure(text="🙈", text_color=self.COR_AZUL)
            self.senha_visivel = True

    def _criar_opcoes_adicionais(self):
        """Link 'Esqueci minha senha' alinhado à direita."""
        btn_esqueci = ctk.CTkButton(
            self.card_frame,
            text="Esqueci minha senha",
            font=ctk.CTkFont(family="Segoe UI", size=10, underline=True),
            fg_color="transparent",
            hover_color=self.COR_CARD,
            text_color=self.COR_TEXTO_MUTED,
            anchor="e",
            height=18,
            command=self.esqueci_senha_action
        )
        btn_esqueci.pack(anchor="e", padx=24, pady=(2, 6))

    def _criar_mensagem_status(self):
        """Label para mensagens de erro ou feedback."""
        self.lbl_status = ctk.CTkLabel(
            self.card_frame,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            text_color="#EF4444"
        )
        self.lbl_status.pack(anchor="center", padx=24, pady=(0, 4))

    def _criar_botao_entrar(self):
        """Botão principal 'ENTRAR ➔'."""
        self.btn_entrar = ctk.CTkButton(
            self.card_frame,
            text="ENTRAR  ➔",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=self.COR_LARANJA,
            hover_color=self.COR_LARANJA_HOVER,
            text_color="#FFFFFF",
            height=38,
            corner_radius=7,
            command=self.autenticar_usuario
        )
        self.btn_entrar.pack(fill="x", padx=24, pady=(0, 16))

    def esqueci_senha_action(self):
        """Ação ao clicar em 'Esqueci minha senha'."""
        messagebox.showinfo(
            "Recuperação de Senha",
            "Entre em contato com o administrador do sistema para redefinir sua senha.\n\nE-mail: ti.mg@acosuniao.com.br"
        )

    def autenticar_usuario(self):
        """Valida as credenciais digitadas contra o dicionário de usuários."""
        self.usuarios_dict = carregar_usuarios()
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        if not usuario or not senha:
            self.lbl_status.configure(text="⚠️ Preencha os campos de usuário e senha.", text_color="#F59E0B")
            return

        if usuario in self.usuarios_dict:
            item = self.usuarios_dict[usuario]
            
            # Suporta dicionário simples {"user": "pass"} ou estruturado {"senha": "pass", "perfil": "admin", ...}
            if isinstance(item, dict):
                senha_correta = item.get("senha")
                dados_user = item
            else:
                senha_correta = item
                dados_user = {
                    "nome": usuario,
                    "perfil": "admin" if usuario == "tk" else "operador",
                    "modulos": ["*"] if usuario == "tk" else ["materia_prima"]
                }

            if senha == senha_correta:
                self.lbl_status.configure(text="✅ Login efetuado com sucesso!", text_color="#10B981")
                self.user_box.configure(border_color="#10B981")
                self.pass_box.configure(border_color="#10B981")

                # Aguarda breve instante visual e executa o callback / transição
                self.after(400, lambda: self._sucesso_login(usuario, dados_user))
                return

        # Caso credenciais inválidas
        self.lbl_status.configure(text="❌ Usuário ou senha incorretos.", text_color="#EF4444")
        self.user_box.configure(border_color="#EF4444")
        self.pass_box.configure(border_color="#EF4444")

    def _sucesso_login(self, usuario, dados_user):
        """Função disparada quando o login é válido."""
        if self.callback_sucesso:
            self.callback_sucesso(usuario, dados_user)
        else:
            self.destroy()

    def definir_icone(self):
        """Define o ícone oficial do sistema (01.ico)."""
        import sys
        caminhos_tentativas = []
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            caminhos_tentativas.append(Path(sys._MEIPASS) / "Configurações" / "imagens" / "01.ico")
            caminhos_tentativas.append(Path(sys.executable).resolve().parent / "Configurações" / "imagens" / "01.ico")
        caminhos_tentativas.append(Path(__file__).resolve().parent.parent / "Configurações" / "imagens" / "01.ico")

        for caminho_icone in caminhos_tentativas:
            if caminho_icone.exists():
                try:
                    self.iconbitmap(str(caminho_icone))
                    break
                except Exception as e:
                    print(f"Aviso: Não foi possível definir o ícone na JanelaLogin: {e}")

if __name__ == "__main__":
    app = JanelaLogin()
    app.mainloop()
