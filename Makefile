.PHONY: init run

init:
	@if [ ! -d "venv" ]; then \
		python -m venv venv; \
		source venv/bin/activate; \
		pip install --upgrade pip; \
		pip install -r requirements.txt; \
	else \
		echo "Virtual environment already exists. Skipping initialization."; \
	fi

run:
	uvicorn app.main:app --reload
