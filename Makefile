start:
	poetry run python -m services.main

black:
	poetry run black .

pep-isort:
	poetry run isort . 

tests-coverage:
	poetry run pytest --cov=etl_data_from_vk --cov-report xml

check:
	poetry run  pytest -vv


lint:
	poetry run flake8 etl_data_from_vk
