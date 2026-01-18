PY=python

.PHONY: help test test-cov clean run urun start ustart

help:
    @echo "make test      - run tests"
    @echo "make test-cov  - run tests with coverage"
    @echo "make clean     - remove __pycache__ and *.pyc"
    @echo "make run       - start fastapi dev"
	@echo "make urun      - start using uvicorn"
    @echo "make start     - production start (removes app.log then runs fastapi run)"
    @echo "make ustart    - production start using uvicorn (removes app.log then runs uvicorn)"


test:
    $(PY) -m pytest -q

test-cov:
    $(PY) -m pytest --cov=app

clean:
    $(PY) -c "import pathlib,shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc')]; p=pathlib.Path('app/app.log'); p.unlink() if p.exists() else None"

run:
    $(PY) -m fastapi dev app/src/main.py

urun:
    $(PY) -m uvicorn app.src.main:app --reload

start:
    @echo "Removing app log (if present) and starting production server"
    $(PY) -c "import pathlib; p=pathlib.Path('app/app.log'); p.unlink() if p.exists() else None"
    $(PY) -m fastapi run app/src/main.py

ustart:
    @echo "Removing app log (if present) and starting production server"
    $(PY) -c "import pathlib; p=pathlib.Path('app/app.log'); p.unlink() if p.exists() else None"
    $(PY) -m uvicorn app.src.main:app --host 0.0.0.0 --port 8000 --workers 1