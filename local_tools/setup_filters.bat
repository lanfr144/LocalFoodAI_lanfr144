::ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
@echo off
:: Configuration des filtres avec des chemins relatifs portables (Git s'execute toujours a la racine du depot)
@git config filter.ident-dynamic.clean "python local_tools/git-ident-filter.py clean"
@git config filter.ident-dynamic.smudge "python local_tools/git-ident-filter.py smudge %%f"
:: Configuration du format de date universel
@git config log.date "format:%%Y/%%m/%%d %%H:%%M:%%S"
:: Installation du hook commit-msg
@copy /Y local_tools\commit-msg .git\hooks\commit-msg >nul
@echo ✅ Filtres Git et commit-msg hook configures avec succes pour Windows Natif.