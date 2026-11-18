#!/usr/bin/env bash
# env_install.sh : configure un environnement de dev (Ubuntu / macOS)

# printf plutôt qu'echo : comportement identique sur tous les systèmes
print_message() {
    printf "\n%s\n\n" "$1"
}

# OSTYPE est fourni par Bash : "linux-gnu" sur Ubuntu, "darwin..." sur macOS
detect_os() {
    case "$OSTYPE" in
        linux*)  echo "linux" ;;
        darwin*) echo "macos" ;;
        *)       echo "unknown" ;;
    esac
}

# Choisit le bon gestionnaire de paquets selon l'OS
install_pkg() {
    local linux_pkg="$1"
    local mac_pkg="${2:-$1}"
    if [ "$OS" = "linux" ]; then
        sudo apt install -y "$linux_pkg"
    else
        brew install "$mac_pkg"
    fi
}

OS=$(detect_os)
print_message "Système détecté : $OS"

if [ "$OS" = "unknown" ]; then
    print_message "Système non supporté"
    exit 1
fi

# L'index apt doit être à jour avant d'installer quoi que ce soit
if [ "$OS" = "linux" ]; then
    if ! sudo apt update; then
        print_message "ERREUR : apt update a échoué"
        exit 1
    fi
fi

# Python
if command -v python3 > /dev/null 2>&1; then
    print_message "Python déjà installé : $(python3 --version)"
else
    print_message "python3 absent, installation..."
    install_pkg python3
fi

# pip
if ! command -v pip3 > /dev/null 2>&1; then
    print_message "pip3 absent, installation..."
    install_pkg python3-pip python3
fi
print_message "pip : $(pip3 --version)"

# Jupyter
print_message "Installation de Jupyter Notebook"
install_pkg jupyter-notebook jupyterlab

# brew doctor : macOS uniquement
if [ "$OS" = "macos" ]; then
    print_message "Vérification de Homebrew"
    brew doctor
fi

print_message "Installation terminée !"
