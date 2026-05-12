# Instructions pour Antigravity

## Stack Technique
- **Langage :** Python 3.1x (Utiliser `venv` systématiquement).
- **Scripts :** Shell (Bash/Zsh) pour l'automatisation.
- **Gestion de Projet :** Taiga (Lien entre Git et Taiga actif).

## Conventions de Code
- **Python :** Respecter strictement la PEP 8. Utiliser des docstrings pour chaque fonction.
- **Git :** Format de message obligatoire : `TG-<ID> #<status> : <description>` (ex: TG-42 #closed : Ajout de la validation email).
- **Sécurité :** NE JAMAIS inclure de secrets dans le code. Utiliser `.env`.

## Comportement Attendu
1. Si une commande shell est risquée (`rm`, `chmod`), demande confirmation.
2. Toujours mettre à jour `task_plan.md` après une étape majeure terminée.
3. Toujours mettre à jour taiga
