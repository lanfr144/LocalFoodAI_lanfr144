# Taiga Commit Workflow
Description: Garantit que chaque commit contient l'ID Taiga pour la mise à jour automatique.

### Étapes :
1. **Analyse** : Analyse les fichiers modifiés (`git status`).
2. **Demande d'ID** : Demande à l'utilisateur : "Quel est l'ID de la tâche Taiga (ex: 123) et le nouveau statut (ex: closed) ?"
3. **Génération** : Génère un message de commit qui inclut obligatoirement le tag `TG-<ID> #<STATUS>`.
4. **Exécution** : 
   - `git add .`
   - `git commit -m "TG-<ID> #<STATUS> - [Description concise des changements]"`
   - `git push`