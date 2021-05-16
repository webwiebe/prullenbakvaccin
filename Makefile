POSTCODE?=1012AB
venv:
	python -m venv venv

install: venv
	source venv/bin/activate; \
		pip install -r requirements.txt

start:
	source venv/bin/activate; python main.py ${POSTCODE}