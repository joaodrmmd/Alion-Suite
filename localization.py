# localization.py

TRANSLATIONS = {
    "pt": {
        # Launcher
        "launcher_title": "Alion Suite - Selecione a Versão",
        "access_button": "ACESSAR",
        "language": "Idioma",
        # App Geral
        "app_title": "Alion {version}",
        "welcome_message": "Bem-vindo ao Alion {version}\n\nSelecione uma ferramenta na barra lateral",
        "back_to_launcher": "← Voltar ao Lançador",
        "search_tools": "Pesquisar ferramentas...",
        "evaluate_github": "⭐ Avalie no GitHub",
        "page_for": "Página para: {tool_name}",
        # ToolPage
        "executing": "Executando...",
        "execute": "Executar {tool_name}",
        "starting": "--- Iniciando: {tool_name} ---\n",
        "task_complete": "\n>>> Comando concluído.",
        # Rodapé
        "os_ver": "Versão do SO",
        "developed_by": "Desenvolvido por r3du0x",
        "pkg_manager": "Gerenciador de Pacotes",
        # Categorias
        "cat_system_activation": "Sistema e Ativação",
        "cat_optimization_cleanup": "Otimização e Limpeza",
        "cat_drivers_apps": "Drivers e Apps",
        "cat_other": "Outros",
        "cat_win_system": "Sistema (Windows)",
        "cat_sec_tools": "Ferramentas de Segurança",
        "cat_macos_tools": "Ferramentas macOS", # Nova
        # Ferramentas
        "tool_create_restore_point": "Criar Ponto de Restauração",
        "tool_update_system": "Atualizar o Sistema",
        "tool_spotify_ads": "Bloquear Anúncios do Spotify",
        "tool_bleachbit": "Otimização (BleachBit)",
        "tool_disk_cleanup": "Limpeza de Disco",
        "tool_btop": "Monitor de Sistema (btop)",
        "tool_nvidia_drivers": "Drivers NVIDIA (Ubuntu)",
        "tool_amd_drivers": "Drivers AMD (Mesa/Ubuntu)",
        "tool_steam": "Instalar Steam",
        "tool_vencord": "Instalar Vencord (Discord)",
        "tool_github": "Abrir GitHub",
    },
    "en": {
        # Launcher
        "launcher_title": "Alion Suite - Select Version",
        "access_button": "ACCESS",
        "language": "Language",
        # App Geral
        "app_title": "Alion {version}",
        "welcome_message": "Welcome to Alion {version}\n\nSelect a tool from the sidebar",
        "back_to_launcher": "← Back to Launcher",
        "search_tools": "Search tools...",
        "evaluate_github": "⭐ Rate on GitHub",
        "page_for": "Page for: {tool_name}",
        # ToolPage
        "executing": "Executing...",
        "execute": "Execute {tool_name}",
        "starting": "--- Starting: {tool_name} ---\n",
        "task_complete": "\n>>> Command complete.",
        # Footer
        "os_ver": "OS Ver",
        "developed_by": "Developed by r3du0x",
        "pkg_manager": "Package Manager",
        # Categories
        "cat_system_activation": "System & Activation",
        "cat_optimization_cleanup": "Optimization & Cleanup",
        "cat_drivers_apps": "Drivers & Apps",
        "cat_other": "Other",
        "cat_win_system": "System (Windows)",
        "cat_sec_tools": "Security Tools",
        "cat_macos_tools": "macOS Tools", # New
        # Tools
        "tool_create_restore_point": "Create Restore Point",
        "tool_update_system": "Update System",
        "tool_spotify_ads": "Block Spotify Ads",
        "tool_bleachbit": "Optimization (BleachBit)",
        "tool_disk_cleanup": "Disk Cleanup",
        "tool_btop": "System Monitor (btop)",
        "tool_nvidia_drivers": "NVIDIA Drivers (Ubuntu)",
        "tool_amd_drivers": "AMD Drivers (Mesa/Ubuntu)",
        "tool_steam": "Install Steam",
        "tool_vencord": "Install Vencord (Discord)",
        "tool_github": "Open GitHub",
    }
}

def get_string(key, lang="en", **kwargs):
    """Busca uma string de tradução pelo seu ID e a formata."""
    try:
        return TRANSLATIONS[lang][key].format(**kwargs)
    except KeyError:
        return key