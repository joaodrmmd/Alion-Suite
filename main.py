#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import shutil # <- NOVO: Módulo importado para usar o 'which'

# --- Constantes de Cores (ANSI escape codes) ---
COR = {
    "magenta": "\033[1;95m",
    "ciano": "\033[1;96m",
    "vermelho": "\033[1;91m",
    "reset": "\033[0m"
}

# --- LÓGICA DE DETECÇÃO DO GERENCIADOR DE PACOTES (NOVO) ---
def detectar_gerenciador_pacotes():
    """Verifica qual gerenciador de pacotes está disponível no sistema."""
    gerenciadores = ["apt", "dnf", "pacman", "zypper"] # Ordem de verificação
    for pm in gerenciadores:
        if shutil.which(pm):
            print(f"{COR['ciano']}Gerenciador de pacotes detectado: {pm}{COR['reset']}")
            return pm
    return None

# Variável global que armazenará o gerenciador de pacotes encontrado
GERENCIADOR_PACOTES = detectar_gerenciador_pacotes()

# Mapeamento de comandos para cada gerenciador (NOVO)
# Isso torna o script extremamente extensível
COMANDOS = {
    "apt": {
        "instalar": "sudo apt install -y",
        "atualizar": "sudo apt update && sudo apt upgrade -y",
        "limpeza": "sudo apt autoremove -y && sudo apt clean"
    },
    "dnf": {
        "instalar": "sudo dnf install -y",
        "atualizar": "sudo dnf upgrade -y",
        "limpeza": "sudo dnf autoremove -y && sudo dnf clean all"
    },
    "pacman": {
        "instalar": "sudo pacman -S --noconfirm",
        "atualizar": "sudo pacman -Syu --noconfirm",
        "limpeza": "sudo pacman -Rns $(pacman -Qtdq) --noconfirm"
    }
    # Adicione outros como 'zypper' se desejar
}

def limpar_tela():
    """Limpa o terminal. 'clear' para Linux/macOS, 'cls' para Windows."""
    os.system('clear' if os.name == 'posix' else 'cls')

def exibir_banner():
    """Exibe o banner ASCII art do AlionV1."""
    banner_art = f"""
{COR['magenta']}


                       .-'''-.                                                                                                  
          .---.       '   _    \                                                                                                
          |   |.--. /   /` '.   \    _..._                       _________   _...._            __.....__                        
          |   ||__|.   |     \  '  .'     '.                     \        |.'      '-.     .-''         '.                      
          |   |.--.|   '      |  '.   .-.   .                     \        .'```'.    '.  /     .-''"'-.  `.                    
    __    |   ||  |\    \     / / |  '   '  |              __      \      |       \     \/     /________\   \ ____     _____    
 .:--.'.  |   ||  | `.   ` ..' /  |  |   |  |           .:--.'.     |     |        |    ||                  |`.   \  .'    /    
/ |   \ | |   ||  |    '-...-'`   |  |   |  |          / |   \ |    |      \      /    . \    .-------------'  `.  `'    .'     
`" __ | | |   ||  |               |  |   |  |          `" __ | |    |     |\`'-.-'   .'   \    '-.____...---.    '.    .'       
 .'.''| | |   ||__|               |  |   |  |           .'.''| |    |     | '-....-'`      `.             .'     .'     `.      
/ /   | |_'---'                   |  |   |  |          / /   | |_  .'     '.                 `''-...... -'     .'  .'`.   `.    
\ \._,\ '/                        |  |   |  |          \ \._,\ '/'-----------'                               .'   /    `.   `.  
 `--'  `"                         '--'   '--'           `--'  `"                                            '----'       '----' 

{COR['reset']}
    """
    print(banner_art)

def exibir_menu():
    """Exibe o menu de opções adaptado para Linux."""
    # O menu permanece o mesmo visualmente
    menu_texto = f"""
{COR['magenta']}║{COR['reset']} {COR['ciano']}[1] Criar Ponto de Restauração (Timeshift){COR['reset']} {COR['magenta']}║{COR['reset']} {COR['ciano']}[5] Instalar Monitor de Sistema (btop){COR['reset']}      {COR['magenta']}║{COR['reset']} {COR['ciano']}[9] Instalar Drivers AMD (Mesa Drivers){COR['reset']}
{COR['magenta']}║{COR['reset']}                                          {COR['magenta']}║{COR['reset']}                                          {COR['magenta']}║{COR['reset']}
{COR['magenta']}╠══{COR['reset']} {COR['ciano']}[2] Bloquear Anúncios do Spotify{COR['reset']}         {COR['magenta']}╠══{COR['reset']} {COR['ciano']}[6] Limpeza de Disco e Pacotes{COR['reset']}      {COR['magenta']}╠══{COR['reset']} {COR['ciano']}[10] Instalar Vencord (Mod Discord){COR['reset']}
{COR['magenta']}║{COR['reset']}                                          {COR['magenta']}║{COR['reset']}                                          {COR['magenta']}║{COR['reset']}
{COR['magenta']}╠══{COR['reset']} {COR['ciano']}[3] Atualizar o Sistema Completamente{COR['reset']}    {COR['magenta']}╠══{COR['reset']} {COR['ciano']}[7] Instalar Steam{COR['reset']}                  {COR['magenta']}╚══{COR['reset']} {COR['ciano']}[11] Abrir GitHub do Projeto{COR['reset']}
{COR['magenta']}║{COR['reset']}                                          {COR['magenta']}║{COR['reset']}
{COR['magenta']}╚══{COR['reset']} {COR['ciano']}[4] Otimização e Limpeza (BleachBit){COR['reset']}      {COR['magenta']}╚══{COR['reset']} {COR['ciano']}[8] Instalar Drivers NVIDIA{COR['reset']}

{COR['magenta']}║{COR['reset']} {COR['ciano']}[0] Sair do Programa{COR['reset']}
    """
    print(menu_texto)
    print(f"\n{COR['magenta']}║ {COR['reset']}{COR['ciano']}Developed by r3du0x@ 2025 (Linux Ver.){COR['reset']} {COR['magenta']}║ {COR['ciano']}Detected Package Manager: {GERENCIADOR_PACOTES or 'Nenhum'}{COR['reset']} {COR['magenta']}║{COR['reset']}")


def executar_comando(comando):
    """Executa um comando no terminal e exibe a saída em tempo real."""
    try:
        print(f"{COR['ciano']}\n Executando: {comando}{COR['reset']}")
        subprocess.run(comando, shell=True, check=True)
        print(f"\n{COR['magenta']}Comando executado com sucesso!{COR['reset']}")
    except subprocess.CalledProcessError as e:
        print(f"\n{COR['vermelho']}Ocorreu um erro ao executar o comando: {e}{COR['reset']}")
    except FileNotFoundError:
        print(f"\n{COR['vermelho']}Comando não encontrado. Verifique se o programa está instalado.{COR['reset']}")
    input("\n Pressione Enter para continuar...")

# --- Funções para cada opção do menu (MODIFICADAS) ---

def opcao_ponto_restauracao():
    print("--- Criando Ponto de Restauração com Timeshift ---")
    print("Isso criará um snapshot do seu sistema. Requer o Timeshift instalado.")
    executar_comando("sudo timeshift --create --comments 'Alion Restore Point'")

def opcao_spotify_ads():
    print("--- Instalando bloqueador de anúncios para Spotify no Linux ---")
    executar_comando(f"{COMANDOS[GERENCIADOR_PACOTES]['instalar']} git make && git clone https://github.com/abba23/spotify-adblock.git && cd spotify-adblock && make | sudo make install")

def opcao_atualizar_sistema():
    print("--- Atualizando todos os pacotes do sistema ---")
    comando_atualizar = COMANDOS[GERENCIADOR_PACOTES]['atualizar']
    executar_comando(comando_atualizar)

def opcao_bleachbit():
    print("--- Instalando o BleachBit para limpeza ---")
    comando_instalar = f"{COMANDOS[GERENCIADOR_PACOTES]['instalar']} bleachbit"
    executar_comando(f"{comando_instalar} && echo 'Execute bleachbit (normal) ou sudo bleachbit (root) para limpar.'")

def opcao_btop():
    print("--- Instalando e executando o monitor de sistema btop ---")
    # Pacotes podem ter nomes diferentes, mas 'btop' é consistente na maioria
    comando_instalar = f"{COMANDOS[GERENCIADOR_PACOTES]['instalar']} btop"
    executar_comando(f"{comando_instalar} && btop")

def opcao_limpeza_disco():
    print("--- Removendo pacotes desnecessários e limpando o cache ---")
    comando_limpeza = COMANDOS[GERENCIADOR_PACOTES]['limpeza']
    executar_comando(comando_limpeza)

def opcao_instalar_steam():
    print("--- Instalando o cliente Steam ---")
    comando_instalar = f"{COMANDOS[GERENCIADOR_PACOTES]['instalar']} steam"
    executar_comando(comando_instalar)

def opcao_drivers_nvidia():
    print("--- Instalando drivers da NVIDIA ---")
    if GERENCIADOR_PACOTES == "apt":
        # Este comando é específico do Ubuntu
        print("Detectado sistema baseado em Debian/Ubuntu. Usando 'ubuntu-drivers'...")
        executar_comando("sudo ubuntu-drivers autoinstall")
    else:
        print(f"{COR['vermelho']}A instalação automática de drivers NVIDIA não é suportada para '{GERENCIADOR_PACOTES}'.{COR['reset']}")
        print("Por favor, consulte a documentação da sua distribuição.")
        input("\n Pressione Enter para continuar...")

def opcao_drivers_amd():
    print("--- Adicionando PPA para drivers Mesa atualizados (para jogos) ---")
    if GERENCIADOR_PACOTES == "apt":
        # PPA é específico do Ubuntu/Debian
        print("Detectado sistema baseado em Debian/Ubuntu. Adicionando PPA Kisak-Mesa...")
        executar_comando("sudo add-apt-repository ppa:kisak/kisak-mesa -y && sudo apt update && sudo apt upgrade -y")
    else:
        print(f"{COR['vermelho']}A adição de PPAs não é suportada para '{GERENCIADOR_PACOTES}'.{COR['reset']}")
        print("As distros mais recentes (Fedora, Arch) já costumam ter drivers Mesa atualizados.")
        input("\n Pressione Enter para continuar...")


def opcao_vencord():
    print("--- Instalando o Vencord para Discord ---")
    executar_comando("curl -sS https://raw.githubusercontent.com/Vendicated/VencordInstaller/main/install.sh | bash")

def opcao_github():
    print("--- Abrindo o repositório no GitHub ---")
    executar_comando("xdg-open https://github.com/joaodrmmd/AlionV1")

def main():
    """Função principal que executa o loop do programa."""
    if not GERENCIADOR_PACOTES:
        limpar_tela()
        exibir_banner()
        print(f"{COR['vermelho']}ERRO: Nenhum gerenciador de pacotes compatível (apt, dnf, pacman) foi encontrado.{COR['reset']}")
        print("Este script não pode continuar.")
        sys.exit(1) # Sai do script com um código de erro

    opcoes = {
        "1": opcao_ponto_restauracao,
        "2": opcao_spotify_ads,
        "3": opcao_atualizar_sistema,
        "4": opcao_bleachbit,
        "5": opcao_btop,
        "6": opcao_limpeza_disco,
        "7": opcao_instalar_steam,
        "8": opcao_drivers_nvidia,
        "9": opcao_drivers_amd,
        "10": opcao_vencord,
        "11": opcao_github,
    }

    while True:
        limpar_tela()
        exibir_banner()
        exibir_menu()


        escolha = input(f"{COR['magenta']}╚═ {COR['reset']}{COR['ciano']}Select Option -> {COR['reset']}").strip()

        if escolha == "0":
            print(f"\n{COR['magenta']}See u soon!{COR['reset']}")
            break
        
        funcao_a_executar = opcoes.get(escolha)

        if funcao_a_executar:
            limpar_tela()
            exibir_banner()
            funcao_a_executar()
        else:
            print(f"\n{COR['vermelho']}Opção inválida. Tente novamente.{COR['reset']}")
            input("\n Pressione Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{COR['magenta']}Programa interrompido pelo usuário. Saindo...{COR['reset']}")
        sys.exit(0)