# ===============================
# Anime-Rec Makefile
# ===============================
# Common commands for development

# Default target
.DEFAULT_GOAL := help

# Colors for output
GREEN  := \033[0;32m
CYAN   := \033[0;36m
RESET  := \033[0m

# -------------------------------------
# 🌱 Environment setup
# -------------------------------------

install: ## Install dependencies from pyproject.toml
	@echo "$(CYAN)Installing dependencies using uv...$(RESET)"
	uv sync
	@echo "$(GREEN)✅ Dependencies installed.$(RESET)"

venv: ## Create or update the virtual environment
	@echo "$(CYAN)Setting up virtual environment...$(RESET)"
	uv venv
	@echo "$(GREEN)✅ Virtual environment ready.$(RESET)"

# -------------------------------------
# 🧠 Database and seeding
# -------------------------------------

initdb: ## Initialize the database (create tables)
	@echo "$(CYAN)Initializing database schema...$(RESET)"
	uv run python -c "from app.db import init_db; init_db()"
	@echo "$(GREEN)✅ Database tables created.$(RESET)"

# -------------------------------------
# 🚀 Run server
# -------------------------------------

run: ## Run FastAPI development server
	@echo "$(CYAN)Starting FastAPI with Uvicorn...$(RESET)"
	uv run uvicorn app.main:app --reload

# -------------------------------------
# 🧹 Utilities
# -------------------------------------

clean: ## Remove __pycache__, .pyc, etc.
	@echo "$(CYAN)Cleaning build artifacts...$(RESET)"
	del /s /q *.pyc 2>nul || true
	del /s /q __pycache__ 2>nul || true
	@echo "$(GREEN)✅ Cleanup complete.$(RESET)"

help: ## Show this help
	@echo ""
	@echo "$(CYAN)Anime-Rec Project Commands$(RESET)"
	@echo "----------------------------------"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(RESET) %s\n", $$1, $$2}'
	@echo ""

up: ## Start backend + Postgres + Redis with Docker Compose
	@echo "$(CYAN)Starting full stack with Docker Compose...$(RESET)"
	cd .. && docker compose up --build

seed: ## Seed anime data from Jikan
	cd .. && docker compose exec backend uv run python -m app.seed_jikan

up-no-build:
	cd .. && docker compose up

down:
	cd .. && docker compose down