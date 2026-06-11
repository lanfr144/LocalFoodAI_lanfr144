#!/bin/sh
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
git config filter.ident-dynamic.clean "python3 local_tools/git-ident-filter.py clean"
git config filter.ident-dynamic.smudge "python3 local_tools/git-ident-filter.py smudge %f"
git config log.date "format:%Y/%m/%d %H:%M:%S"
cp local_tools/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
echo "✅ Filtres Git et commit-msg hook configurés avec succès pour Unix / WSL."