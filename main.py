from Login import JanelaLogin
from Interface.janela_principal import JanelaPrincipal

def iniciar_aplicacao():
    """
    Gerencia o ciclo de vida da aplicação.
    Permite alternar continuamente entre a tela de login e a janela principal sem fechar o sistema.
    """
    while True:
        sessao = {"usuario": None, "dados": None, "trocar_usuario": False}

        def login_sucesso(usuario, dados_usuario):
            sessao["usuario"] = usuario
            sessao["dados"] = dados_usuario
            login_app.destroy()

        # 1. Abre a tela de login
        login_app = JanelaLogin(callback_sucesso=login_sucesso)
        login_app.mainloop()

        # Se a janela de login foi fechada sem autenticação válida, encerra
        if not sessao["usuario"]:
            break

        def acao_trocar_usuario():
            sessao["trocar_usuario"] = True
            app_principal.destroy()

        # 2. Abre a Janela Principal com as permissões do usuário
        app_principal = JanelaPrincipal(
            usuario_logado=sessao["usuario"],
            dados_usuario=sessao["dados"],
            callback_trocar_usuario=acao_trocar_usuario
        )
        app_principal.mainloop()

        # Se o usuário encerrou o turno (sem solicitar troca de usuário), encerra o loop
        if not sessao["trocar_usuario"]:
            break

if __name__ == "__main__":
    iniciar_aplicacao()
