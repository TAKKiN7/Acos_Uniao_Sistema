import customtkinter as ctk
import datetime
from tkinter import messagebox
from pathlib import Path

# Importação dos frames das abas dos arquivos separados
from Interface.Status.status_frame import StatusFrame
from Interface.Materia_Prima.materia_prima_frame import MateriaPrimaFrame
from Interface.CTE.notas_cte_frame import NotasCTEFrame
from Interface.Uso_Consumo.uso_consumo_frame import UsoConsumoFrame
from Interface.Almoxarifado.almoxarifado_frame import AlmoxarifadoFrame
from Interface.Usuarios.usuarios_frame import UsuariosFrame

# Configurações iniciais do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class JanelaPrincipal(ctk.CTk):
    """
    Janela Principal do Sistema AÇOS UNIÃO MANAGER.
    Gerencia a navegação lateral, o cabeçalho superior, o rodapé e a troca de abas.
    Aplica controle de acesso e exibe a tela inicial de Status ao iniciar.
    """
    def __init__(self, usuario_logado="Operador Sistema", dados_usuario=None, callback_trocar_usuario=None):
        super().__init__()
        self.usuario_logado = usuario_logado
        self.callback_trocar_usuario = callback_trocar_usuario
        
        # Dados de perfil e permissões do usuário
        self.dados_usuario = dados_usuario or {
            "nome": usuario_logado,
            "perfil": "admin" if usuario_logado == "tk" else "operador",
            "modulos": ["*"] if usuario_logado == "tk" else ["materia_prima"]
        }

        # Configurações da Janela
        self.title("AÇOS UNIÃO SISTEMA")
        self.geometry("1240x780")
        self.minsize(1024, 680)

        # Configurar Ícone do Sistema
        self.definir_icone()

        # Layout Principal (Grid: Sidebar na col 0, Conteúdo Principal na col 1)
        self.grid_columnconfigure(0, weight=0) # Sidebar largura fixa
        self.grid_columnconfigure(1, weight=1) # Área central flexível
        self.grid_rowconfigure(0, weight=0)    # Topbar
        self.grid_rowconfigure(1, weight=1)    # Conteúdo (Abas)
        self.grid_rowconfigure(2, weight=0)    # Rodapé

        # Dicionário para armazenar abas instanciadas
        self.frames = {}

        # Construção da Interface
        self.criar_sidebar()
        self.criar_topbar()

        # Container Principal onde os frames das abas serão exibidos
        self.container_principal = ctk.CTkFrame(
            self, 
            fg_color=("#CBD5E1", "#121418"), 
            corner_radius=0
        )
        self.container_principal.grid(row=1, column=1, sticky="nsew")
        self.container_principal.grid_columnconfigure(0, weight=1)
        self.container_principal.grid_rowconfigure(0, weight=1)

        # Inicializa os frames das abas separadas
        self.inicializar_abas()

        # Exibir a tela inicial de Status por padrão
        self.selecionar_aba_inicial()

        # Iniciar relógio digital no cabeçalho
        self.atualizar_relogio()

        # Ativar fullscreen por padrão e vincular tecla F11 para alternar
        self.attributes("-fullscreen", True)
        self.bind("<F11>", self.alternar_fullscreen)

    def tem_acesso_modulo(self, chave_modulo):
        """Verifica se o usuário logado possui permissão para acessar determinado módulo."""
        modulos = self.dados_usuario.get("modulos", [])
        perfil = self.dados_usuario.get("perfil", "operador")
        if perfil == "admin" or "*" in modulos or chave_modulo in modulos:
            return True
        if chave_modulo == "almoxarifado" and ("almoxarifado_operador" in modulos or "almoxarifado_admin" in modulos):
            return True
        return False

    def criar_sidebar(self):
        """Cria o menu lateral (Sidebar) com botões ativos ou bloqueados conforme as permissões."""
        self.sidebar = ctk.CTkFrame(
            self, 
            width=240, 
            fg_color=("#E2E8F0", "#181B20"), 
            border_color=("#94A3B8", "#262B34"), 
            border_width=1, 
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, rowspan=3, sticky="nsew")
        
        # Espaçador que empurra o usuário e botão de fechar para o fundo na row=9
        self.sidebar.grid_rowconfigure(9, weight=1)

        # Logo / Nome da Empresa
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.logo_frame.grid(row=0, column=0, padx=20, pady=(25, 20), sticky="ew")

        self.lbl_brand = ctk.CTkLabel(
            self.logo_frame,
            text="AÇOS UNIÃO",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_brand.pack(anchor="w")

        # Divisor
        self.divisor1 = ctk.CTkFrame(self.sidebar, height=1, fg_color=("#94A3B8", "#262B34"))
        self.divisor1.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))

        # Botões de Navegação (Menu Lateral)
        self.botoes_menu = {}

        # Listagem de todos os itens do menu
        self.menu_items = [
            ("materia_prima", "  NOTAS DE MATÉRIA-PRIMA", self.abrir_materia_prima),
            ("notas_cte", "  NOTAS CTE", self.abrir_notas_cte),
            ("uso_consumo", "  NOTAS DE USO E CONSUMO", self.abrir_uso_consumo),
            ("almoxarifado", "  ALMOXARIFADO", self.abrir_almoxarifado),
            ("faturamento", "  FATURAMENTO", lambda: self.menu_em_desenvolvimento("Faturamento")),
            ("ti", "  TI", lambda: self.menu_em_desenvolvimento("Módulo TI")),
            ("usuarios", "  GESTÃO DE USUÁRIOS", self.abrir_usuarios)
        ]

        for index, (chave, texto, comando) in enumerate(self.menu_items, start=2):
            tem_permissao = self.tem_acesso_modulo(chave)

            if tem_permissao:
                btn = ctk.CTkButton(
                    self.sidebar,
                    text=texto,
                    anchor="w",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    fg_color="transparent",
                    text_color=("#0F172A", "#A0AEC0"),
                    hover_color=("#CBD5E1", "#252A32"),
                    height=42,
                    corner_radius=8,
                    command=comando
                )
            else:
                # Módulo sem permissão -> Botão com cadeado e aviso de bloqueio
                btn = ctk.CTkButton(
                    self.sidebar,
                    text=f"🔒 {texto.strip()}",
                    anchor="w",
                    font=ctk.CTkFont(size=11, weight="bold"),
                    fg_color="transparent",
                    text_color=("#94A3B8", "#475569"),
                    hover_color=("#E2E8F0", "#1E232B"),
                    height=42,
                    corner_radius=8,
                    command=lambda m=texto.strip(): self.acesso_negado(m)
                )

            btn.grid(row=index, column=0, padx=12, pady=3, sticky="ew")
            self.botoes_menu[chave] = btn

        # Rodapé do Sidebar (Usuário, Botão Trocar Usuário e Encerrar Turno)
        self.user_info_frame = ctk.CTkFrame(
            self.sidebar, 
            fg_color=("#CBD5E1", "#121418"), 
            corner_radius=8
        )
        self.user_info_frame.grid(row=10, column=0, padx=15, pady=(0, 10), sticky="ew")

        nome_exibir = self.dados_usuario.get("nome", self.usuario_logado)
        self.lbl_user = ctk.CTkLabel(
            self.user_info_frame,
            text=f"👤 {nome_exibir}",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#0F172A", "#E2E8F0")
        )
        self.lbl_user.pack(anchor="w", padx=12, pady=10)

        # Botão Trocar de Usuário (Azul)
        self.btn_trocar_user = ctk.CTkButton(
            self.sidebar,
            text="🔄  TROCAR USUÁRIO",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#0052FF",
            hover_color="#003EB8",
            text_color="#FFFFFF",
            height=38,
            corner_radius=8,
            command=self.trocar_usuario
        )
        self.btn_trocar_user.grid(row=11, column=0, padx=15, pady=(2, 4), sticky="ew")

        # Botão Encerrar Turno (Vermelho)
        self.btn_encerrar = ctk.CTkButton(
            self.sidebar,
            text="↪  ENCERRAR TURNO",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#DC2626",
            hover_color="#B91C1C",
            text_color="#FFFFFF",
            height=38,
            corner_radius=8,
            command=self.encerrar_turno
        )
        self.btn_encerrar.grid(row=12, column=0, padx=15, pady=(2, 15), sticky="ew")

    def criar_topbar(self):
        """Cria a barra superior do aplicativo."""
        self.topbar = ctk.CTkFrame(
            self, 
            height=60, 
            fg_color=("#F0F4F8", "#181B20"), 
            border_color=("#94A3B8", "#262B34"), 
            border_width=1, 
            corner_radius=0
        )
        self.topbar.grid(row=0, column=1, sticky="ew")
        self.topbar.grid_columnconfigure(0, weight=1)

        # Título do aplicativo no cabeçalho
        self.lbl_app_title = ctk.CTkLabel(
            self.topbar,
            text="AÇOS UNIÃO SISTEMA",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.lbl_app_title.grid(row=0, column=0, padx=25, pady=15, sticky="w")

        # Lado direito do cabeçalho (Relógio Digital + Modo do Usuário)
        self.header_right = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.header_right.grid(row=0, column=1, padx=25, pady=10, sticky="e")

        # Label do Relógio Digital
        self.lbl_relogio = ctk.CTkLabel(
            self.header_right,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#94A3B8"
        )
        self.lbl_relogio.pack(side="left", padx=(0, 15))

        # Indicador de perfil (ADMIN / OPERADOR) logo após a data
        perfil = self.dados_usuario.get("perfil", "operador")
        if perfil == "admin":
            texto_perfil = "🟢 MODO ADMINISTRADOR"
            cor_perfil = ("#047857", "#10B981")
        else:
            texto_perfil = "🔵 MODO OPERADOR"
            cor_perfil = ("#1D4ED8", "#3B82F6")

        self.lbl_modo_usuario = ctk.CTkLabel(
            self.header_right,
            text=texto_perfil,
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=cor_perfil
        )
        self.lbl_modo_usuario.pack(side="left", padx=(5, 0))

    def inicializar_abas(self):
        """Instancia os frames contidos nos arquivos externos e guarda no dicionário."""
        # Frame 0: Status / Home inicial (status_frame.py na pasta Interface/Status)
        frame_status = StatusFrame(
            self.container_principal,
            usuario_logado=self.usuario_logado,
            dados_usuario=self.dados_usuario
        )
        frame_status.grid(row=0, column=0, sticky="nsew")
        self.frames["status"] = frame_status

        # Frame 1: Matéria-Prima (materia_prima_frame.py)
        frame_mp = MateriaPrimaFrame(self.container_principal)
        frame_mp.grid(row=0, column=0, sticky="nsew")
        self.frames["materia_prima"] = frame_mp

        # Frame 2: Notas CTE (notas_cte_frame.py)
        frame_cte = NotasCTEFrame(
            self.container_principal,
            usuario_logado=self.usuario_logado,
            dados_usuario=self.dados_usuario
        )
        frame_cte.grid(row=0, column=0, sticky="nsew")
        self.frames["notas_cte"] = frame_cte

        # Frame 3: Notas de Uso e Consumo (uso_consumo_frame.py na pasta Interface/Uso_Consumo)
        frame_uc = UsoConsumoFrame(self.container_principal)
        frame_uc.grid(row=0, column=0, sticky="nsew")
        self.frames["uso_consumo"] = frame_uc

        # Frame 4: Almoxarifado (almoxarifado_frame.py na pasta Interface/Almoxarifado)
        frame_almox = AlmoxarifadoFrame(
            self.container_principal,
            usuario_logado=self.usuario_logado,
            dados_usuario=self.dados_usuario
        )
        frame_almox.grid(row=0, column=0, sticky="nsew")
        self.frames["almoxarifado"] = frame_almox

        # Frame 5: Gestão de Usuários (usuarios_frame.py na pasta Interface/Usuarios)
        frame_usr = UsuariosFrame(
            self.container_principal,
            usuario_logado=self.usuario_logado,
            dados_usuario=self.dados_usuario
        )
        frame_usr.grid(row=0, column=0, sticky="nsew")
        self.frames["usuarios"] = frame_usr

    def selecionar_aba_inicial(self):
        """Abre a tela inicial de Status por padrão (sem aba no menu lateral)."""
        self.selecionar_aba("status")

    def selecionar_aba(self, chave_aba):
        """Eleva a aba selecionada se o usuário possuir permissão."""
        if chave_aba != "status" and not self.tem_acesso_modulo(chave_aba):
            self.acesso_negado(chave_aba)
            return

        for chave, frame in self.frames.items():
            if chave == chave_aba:
                frame.tkraise()
            
        for chave, btn in self.botoes_menu.items():
            if chave == chave_aba:
                btn.configure(
                    fg_color="#EA580C", 
                    text_color="#FFFFFF", 
                    hover_color="#C2410C"
                )
            elif self.tem_acesso_modulo(chave):
                btn.configure(
                    fg_color="transparent", 
                    text_color=("#0F172A", "#A0AEC0"), 
                    hover_color=("#CBD5E1", "#252A32")
                )

    def abrir_materia_prima(self):
        self.selecionar_aba("materia_prima")

    def abrir_notas_cte(self):
        self.selecionar_aba("notas_cte")

    def abrir_uso_consumo(self):
        self.selecionar_aba("uso_consumo")

    def abrir_almoxarifado(self):
        self.selecionar_aba("almoxarifado")
        if "almoxarifado" in self.frames:
            self.frames["almoxarifado"].carregar_se_necessario()

    def abrir_usuarios(self):
        self.selecionar_aba("usuarios")

    def menu_em_desenvolvimento(self, nome_modulo):
        messagebox.showinfo("Módulo em Desenvolvimento", f"O módulo '{nome_modulo}' estará disponível em breve.")

    def acesso_negado(self, nome_modulo):
        """Alerta exibido ao tentar acessar um módulo restrito."""
        messagebox.showwarning(
            "Acesso Restrito",
            f"O usuário '{self.usuario_logado}' não possui permissão para acessar o módulo '{nome_modulo}'.\n\nEntre em contato com o administrador do sistema para solicitar acesso."
        )

    def atualizar_relogio(self):
        """Atualiza o relógio no topo em tempo real."""
        agora = datetime.datetime.now()
        meses = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
        data_formatada = f"{agora.strftime('%H:%M:%S')}  {agora.day:02d} de {meses[agora.month-1]} de {agora.year}"
        self.lbl_relogio.configure(text=data_formatada)
        self.after(1000, self.atualizar_relogio)

    def trocar_usuario(self):
        """Dispara a confirmação para trocar de usuário e retornar à tela de login."""
        resposta = messagebox.askyesno("Trocar Usuário", "Deseja realmente trocar de usuário e retornar à tela de login?")
        if resposta:
            if self.callback_trocar_usuario:
                self.callback_trocar_usuario()
            else:
                self.destroy()

    def encerrar_turno(self):
        resposta = messagebox.askyesno("Encerrar Turno", "Deseja realmente encerrar seu turno e sair do sistema?")
        if resposta:
            self.destroy()

    def alternar_fullscreen(self, event=None):
        """Alterna entre modo tela cheia (fullscreen) e janela ao pressionar a tecla F11."""
        estado_atual = self.attributes("-fullscreen")
        self.attributes("-fullscreen", not estado_atual)

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
                    print(f"Aviso: Não foi possível definir o ícone na JanelaPrincipal: {e}")
