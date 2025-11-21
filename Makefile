.PHONY: help setup build up down restart logs clean test

help:
	@echo "🔥 YAGAMI UNIVERZE - Makefile Commands"
	@echo "======================================"
	@echo ""
	@echo "Setup & Deployment:"
	@echo "  make setup     - Run setup script"
	@echo "  make build     - Build Docker image"
	@echo "  make up        - Start bot"
	@echo "  make down      - Stop bot"
	@echo "  make restart   - Restart bot"
	@echo ""
	@echo "Monitoring:"
	@echo "  make logs      - View logs"
	@echo "  make status    - Check status"
	@echo "  make ps        - List containers"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean     - Clean generated bots and temp files"
	@echo "  make prune     - Prune Docker system"
	@echo "  make backup    - Backup generated bots"
	@echo ""
	@echo "Development:"
	@echo "  make test      - Run tests"
	@echo "  make shell     - Enter container shell"
	@echo "  make local     - Run locally (not in Docker)"
	@echo ""

setup:
	@bash setup.sh

build:
	@echo "🔨 Building Docker image..."
	@docker-compose build

up:
	@echo "🚀 Starting YAGAMI UNIVERZE..."
	@docker-compose up -d
	@echo "✅ Bot started!"
	@echo "📊 View logs: make logs"

down:
	@echo "🛑 Stopping YAGAMI UNIVERZE..."
	@docker-compose down
	@echo "✅ Bot stopped!"

restart:
	@echo "🔄 Restarting YAGAMI UNIVERZE..."
	@docker-compose restart
	@echo "✅ Bot restarted!"

logs:
	@docker-compose logs -f

status:
	@docker-compose ps
	@echo ""
	@echo "📊 Container Stats:"
	@docker stats --no-stream yagami_univerze 2>/dev/null || echo "Container not running"

ps:
	@docker-compose ps

clean:
	@echo "🧹 Cleaning up..."
	@rm -rf temp/*
	@echo "✅ Temp files cleaned"
	@read -p "Delete generated bots older than 7 days? (y/N) " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		find generated_bots/ -type d -mtime +7 -exec rm -rf {} + 2>/dev/null || true; \
		echo "✅ Old generated bots cleaned"; \
	fi

prune:
	@echo "🧹 Pruning Docker system..."
	@docker system prune -f
	@echo "✅ Docker system pruned"

backup:
	@echo "💾 Creating backup..."
	@tar -czf backup_$$(date +%Y%m%d_%H%M%S).tar.gz generated_bots/ .env
	@echo "✅ Backup created"

test:
	@echo "🧪 Running tests..."
	@docker-compose exec yagami_univerze pytest tests/ -v

shell:
	@docker-compose exec yagami_univerze /bin/bash

local:
	@echo "🚀 Running locally..."
	@python3 main.py
