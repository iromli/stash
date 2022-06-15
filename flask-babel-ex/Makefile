tr-init:
	pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
	pybabel init -i messages.pot -d translations -l id

tr-update:
	pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
	pybabel update -i messages.pot -d translations

tr-compile:
	pybabel compile -d translations
