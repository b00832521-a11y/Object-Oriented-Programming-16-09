# bash-exercise

Exercice Bash du cours OOP AIDAMS 2A : configurer un environnement de développement depuis zéro.

## Ce que fait le script env_install.sh
- détecte le système (Linux ou macOS) ;
- vérifie Python 3 et pip, et les installe si besoin ;
- installe Jupyter Notebook ;
- lance `brew doctor` sur macOS.

## Utilisation
    chmod +x env_install.sh
    ./env_install.sh

## Étapes manuelles
1. Installer Oh My Bash et choisir un thème.
2. Activer le plugin git dans ~/.bashrc, puis `source ~/.bashrc`.
3. Tester l'alias : `gst`.
4. Lancer Jupyter : `jupyter notebook`.
