import sys
import json
from pathlib import Path

def obter_pasta_raiz() -> Path:
    """Retorna a pasta raiz do projeto ou a pasta do executável .exe."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent

def obter_caminho_json() -> Path:
    """Retorna o caminho do arquivo JSON de usuários."""
    caminho = obter_pasta_raiz() / "Configurações" / "usuarios.json"
    caminho.parent.mkdir(parents=True, exist_ok=True)
    return caminho

USUARIOS_PADRAO_INICIAIS = {
    "tk": {
        "senha": "347",
        "nome": "Eustáquio (TK)",
        "perfil": "admin",
        "modulos": ["*"]
    },
    "admin_juliana": {
        "senha": "159753",
        "nome": "Juliana",
        "perfil": "operador",
        "modulos": ["almoxarifado"]
    },
    "user": {
        "senha": "user",
        "nome": "Operador Usuário",
        "perfil": "operador",
        "modulos": ["materia_prima"]
    },
    "producao": {
        "senha": "producao",
        "nome": "Operador Produção",
        "perfil": "operador",
        "modulos": ["materia_prima", "notas_cte"]
    }
}

def carregar_usuarios() -> dict:
    """
    Carrega o dicionário de usuários a partir do arquivo JSON.
    Caso o arquivo não exista ou esteja corrompido, recria com os usuários padrão.
    """
    caminho = obter_caminho_json()

    if not caminho.exists():
        salvar_usuarios(USUARIOS_PADRAO_INICIAIS)
        return dict(USUARIOS_PADRAO_INICIAIS)

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if isinstance(dados, dict) and dados:
                return dados
            else:
                salvar_usuarios(USUARIOS_PADRAO_INICIAIS)
                return dict(USUARIOS_PADRAO_INICIAIS)
    except Exception as e:
        print(f"Aviso: Erro ao ler {caminho} ({e}). Restaurando arquivo padrão...")
        salvar_usuarios(USUARIOS_PADRAO_INICIAIS)
        return dict(USUARIOS_PADRAO_INICIAIS)


def salvar_usuarios(usuarios_dict: dict) -> bool:
    """
    Salva o dicionário de usuários no arquivo JSON.
    """
    caminho = obter_caminho_json()
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(usuarios_dict, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar usuários em JSON: {e}")
        return False


def autenticar(login: str, senha_informada: str) -> tuple[bool, dict | None]:
    """
    Valida as credenciais de um usuário.
    Retorna (True, dados_do_usuario) se válido, ou (False, None) caso contrário.
    """
    usuarios = carregar_usuarios()
    login_limpo = login.strip()

    if login_limpo in usuarios:
        dados = usuarios[login_limpo]
        if str(dados.get("senha")) == str(senha_informada):
            dados_retorno = {
                "login": login_limpo,
                "nome": dados.get("nome", login_limpo),
                "perfil": dados.get("perfil", "operador"),
                "modulos": dados.get("modulos", [])
            }
            return True, dados_retorno

    return False, None


def salvar_ou_atualizar_usuario(login: str, senha: str, nome: str, perfil: str, modulos: list) -> bool:
    """
    Adiciona ou atualiza um usuário no JSON.
    """
    usuarios = carregar_usuarios()
    login = login.strip()

    usuarios[login] = {
        "senha": str(senha).strip(),
        "nome": str(nome).strip(),
        "perfil": str(perfil).strip().lower(),
        "modulos": modulos if isinstance(modulos, list) else []
    }

    return salvar_usuarios(usuarios)


def remover_usuario(login: str) -> bool:
    """
    Remove um usuário do arquivo JSON.
    """
    usuarios = carregar_usuarios()
    login = login.strip()

    if login in usuarios:
        del usuarios[login]
        return salvar_usuarios(usuarios)

    return False
