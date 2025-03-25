.PHONY:	env db web test extract

env:
	rm -rf .venv/
	rm -f poetry.lock
	poetry config virtualenvs.in-project true
	poetry install
	poetry run python -m spacy download zh_core_web_sm

db:
	rm -rf wenshu.db
	db/setup.sh wenshu.db

web:
	poetry run flask --app web run --debug

test:
	poetry run python -m wenshu.read db/data_raw/2018年裁判文书数据_马克数据网/2018年01月裁判文书数据.csv

extract:
	poetry run python -m wenshu.extract db/data_raw/2018年裁判文书数据_马克数据网/2018年01月裁判文书数据.csv
