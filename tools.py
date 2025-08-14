import subprocess, shutil, platform, sys
from pathlib import Path

VERSION_CONFIG = {
    "APEX": {"logo": "logo_apex.png", "gif": "apex_bg.gif", "theme_color": "#ffc107", "description": "Linux Ver."},
    "FORGE": {"logo": "logo_forge.png", "gif": "forge_bg.gif", "theme_color": "#43a047", "description": "Windows Ver."},
    "BREW": {"logo": "logo_brew.png", "gif": "brew_bg.gif", "theme_color": "#d81b60", "description": "macOS Ver."},
    "DEFENDER": {"logo": "logo_defender.png", "gif": "defender_bg.gif", "theme_color": "#1e88e5", "description": "Blue Team Sec."}
    
}

TOOLS_APEX = {
    "cat_system_activation": [{'text_key': 'tool_create_restore_point', 'command': {'tipo': 'shell', 'comando': '...'}}, {'text_key': 'tool_update_system', 'command': {'tipo': 'pm', 'acao': 'update'}}],
    "cat_optimization_cleanup": [{'text_key': 'tool_disk_cleanup', 'command': {'tipo': 'pm', 'acao': 'clean'}}, {'text_key': 'tool_btop', 'command': {'tipo': 'pm', 'acao': 'install', 'pacote': 'btop'}}]
}
TOOLS_FORGE = { "cat_win_system": [{'text_key': 'tool_create_restore_point', 'command': {'tipo': 'shell', 'comando': '...'}}] }
TOOLS_DEFENDER = { "cat_sec_tools": [{'text_key': 'tool_create_restore_point', 'command': {'tipo': 'shell', 'comando': '...'}}] }
TOOLS_BREW = { "cat_macos_tools": [{'text_key': 'tool_create_restore_point', 'command': {'tipo': 'shell', 'comando': '...'}}] }

def get_tools(version="APEX"):
    if version == "FORGE": return TOOLS_FORGE
    if version == "DEFENDER": return TOOLS_DEFENDER
    if version == "BREW": return TOOLS_BREW
    return TOOLS_APEX

def get_version_config():
    return VERSION_CONFIG

def detectar_gerenciador_pacotes():
    if sys.platform == "win32":
        if shutil.which("choco"): return "Chocolatey"
        if shutil.which("winget"): return "Winget"
        return "N/A"
    elif sys.platform == "darwin":
        if shutil.which("brew"): return "Homebrew"
        return "N/A"
    elif sys.platform == "linux":
        for pm in ["apt", "dnf", "pacman", "zypper"]:
            if shutil.which(pm): return pm.upper()
    return "N/D"

def detectar_distro():
    if sys.platform == "win32": return f"Windows {platform.release()}"
    if sys.platform == "darwin": return f"macOS {platform.release()}"
    if sys.platform == "linux":
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="): return line.split("=")[1].strip().strip('"')
        except FileNotFoundError: return "Linux"
    return "Sistema Desconhecido"

def executar_comando(info_comando):
    comando_final = ""
    pm = detectar_gerenciador_pacotes().lower()
    tipo = info_comando.get('tipo')
    if tipo == 'shell':
        comando_final = info_comando.get('comando')
    elif tipo == 'pm':
        acao = info_comando.get('acao')
        pacote = info_comando.get('pacote', '')
        mapa_pm = {
            'update': {'apt': 'sudo apt update && sudo apt upgrade -y', 'dnf': 'sudo dnf upgrade -y', 'pacman': 'sudo pacman -Syu --noconfirm'},
            'clean': {'apt': 'sudo apt autoremove -y && sudo apt clean', 'dnf': 'sudo dnf autoremove -y && sudo dnf clean all', 'pacman': 'sudo pacman -Rns $(pacman -Qtdq) --noconfirm'},
            'install': {'apt': f'sudo apt install -y {pacote}', 'dnf': f'sudo dnf install -y {pacote}', 'pacman': f'sudo pacman -S --noconfirm {pacote}'}
        }
        if acao in mapa_pm and pm in mapa_pm[acao]:
            comando_final = mapa_pm[acao][pm]
        else:
            yield f"[ERRO] Ação '{acao}' não suportada para o gerenciador '{pm.upper()}'."
            return
    if not comando_final:
        yield "[ERRO] Não foi possível determinar o comando a ser executado."
        return
    if comando_final.startswith("xdg-open"):
        subprocess.run(comando_final, shell=True)
        yield "Comando de abertura executado.\n\n\n"
        return
    try:
        process = subprocess.Popen(
            comando_final, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1, encoding='utf-8', errors='replace'
        )
        for line in process.stdout: yield line
        for line in process.stderr: yield f"[ERRO] {line}"
        process.wait()
        yield f"\n--- Comando concluído ---\n\n\n"
    except Exception as e:
        yield f"\n[ERRO FATAL] Falha ao executar o comando: {e}\n\n\n"