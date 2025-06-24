.ONESHELL: # Runs all commands in single shell
.PHONY: setup # Make setup (or other commands run on default)
VENV = .venv # Virtual environment (relative) directory

setup: pyproject.toml
	@echo "=== Installing virtual environment (does not activate it!) and package manager ==="
	python -m venv $(VENV)
	( \
       . .venv/bin/activate; \
			 pip install --upgrade pip; \
			 pip install poetry; \
	)
	@echo "=== Install dependencies ==="
	( \
       . .venv/bin/activate; \
       poetry install; \
	)

run:
	( \
       . .venv/bin/activate; \
		streamlit run app.py \
	)

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
	docker system prune
