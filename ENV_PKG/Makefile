maint:
	pip install -r requirements/dev.txt
	pre-commit autoupdate && pre-commit run --all-files
	pip-compile -U requirements/dev.in

upload:
	make clean
	python setup.py sdist bdist_wheel && twine upload dist/*
clean:
	python setup.py clean --all
	pyclean .
	rm -rf *.pyc __pycache__ build dist gym_bracket_gen.egg-info gym_bracket_gen/__pycache__ gym_bracket_gen/units/__pycache__ tests/__pycache__ tests/reports docs/build