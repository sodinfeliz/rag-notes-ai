.PHONY: init run ui start stop status

### === Config ===
APP_NAME := RagNoteAI
PID_FILE := backend.pid
LOG_FILE := backend.log

### === Tasks ===

init:
	@if [ ! -d "venv" ]; then \
		echo "🔧 Setting up virtual environment..."; \
		python -m venv venv; \
		source venv/bin/activate; \
		pip install --upgrade pip; \
		pip install -r requirements.txt; \
	else \
		echo "✅ Virtual environment already exists."; \
	fi

run:
	@if [ ! -f .env ]; then \
		echo "📝 .env not found. Creating from .env.example..."; \
		cp .env.example .env; \
	fi
	@echo "🔧 Starting $(APP_NAME) backend..."
	@nohup python main.py > $(LOG_FILE) 2>&1 & echo $$! > $(PID_FILE)

ui:
	@echo "🖥️  Starting $(APP_NAME) UI..."
	@sleep 1
	@streamlit run ui.py

start: run ui
	@echo "🚀 $(APP_NAME) is running (backend + UI)"

stop:
	@echo "🛑 Stopping $(APP_NAME) backend..."
	@if [ -f $(PID_FILE) ]; then \
		kill `cat $(PID_FILE)` && rm $(PID_FILE); \
		echo "✅ $(APP_NAME) backend stopped."; \
	else \
		echo "⚠️  No $(APP_NAME) PID file found."; \
	fi

status:
	@echo "📊 Checking $(APP_NAME) backend status..."
	@if [ -f $(PID_FILE) ]; then \
		PID=`cat $(PID_FILE)`; \
		if ps -p $$PID > /dev/null; then \
			echo "✅ $(APP_NAME) backend is running (PID: $$PID)"; \
		else \
			echo "❌ PID file exists, but process is not running."; \
		fi \
	else \
		echo "⚠️  $(APP_NAME) backend is not running."; \
	fi
