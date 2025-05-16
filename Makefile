.PHONY: uv install run ui start stop status

### === Config ===
APP_NAME := RagNotesAI
PID_FILE := backend.pid

### === Tasks ===

uv:  # install uv if it's not present
	@command -v uv > /dev/null 2>&1 || { \
		echo "🔧 Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	}

dev: uv
	uv sync --dev

install: uv  # install dependencies
	uv sync --frozen

run: install
	@if [ ! -f .env ]; then \
		echo "📝 .env not found. Creating from .env.example..."; \
		cp .env.example .env; \
	fi
	@echo "🔧 Starting $(APP_NAME) backend..."
	@nohup uv run main.py > /dev/null 2>&1 & echo $$! > $(PID_FILE)

ui: install
	@echo "🖥️  Starting $(APP_NAME) UI..."
	@sleep 1
	@uv run streamlit run ui.py

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
