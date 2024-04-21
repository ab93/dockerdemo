setup:
	poetry install
	cd extension; python setup.py install; cd -

export:
	poetry export --without dev -f requirements.txt --output requirements-exported.txt --without-hashes

