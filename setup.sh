#!/bin/bash
# setup.sh - YAGAMI UNIVERZE Setup Script

set -e

echo "🔥 YAGAMI UNIVERZE Setup Script"
echo "================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}⚠️  Please do not run this script as root${NC}"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Docker
echo "🔍 Checking Docker..."
if command_exists docker; then
    echo -e "${GREEN}✅ Docker is installed${NC}"
    docker --version
else
    echo -e "${YELLOW}⚠️  Docker is not installed${NC}"
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo -e "${GREEN}✅ Docker installed${NC}"
    echo -e "${YELLOW}⚠️  Please log out and log back in for group changes to take effect${NC}"
fi

# Check Docker Compose
echo ""
echo "🔍 Checking Docker Compose..."
if command_exists docker-compose; then
    echo -e "${GREEN}✅ Docker Compose is installed${NC}"
    docker-compose --version
else
    echo -e "${YELLOW}⚠️  Docker Compose is not installed${NC}"
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✅ Docker Compose installed${NC}"
fi

# Check Python
echo ""
echo "🔍 Checking Python..."
if command_exists python3; then
    echo -e "${GREEN}✅ Python is installed${NC}"
    python3 --version
else
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

# Check Git
echo ""
echo "🔍 Checking Git..."
if command_exists git; then
    echo -e "${GREEN}✅ Git is installed${NC}"
    git --version
else
    echo -e "${YELLOW}⚠️  Git is not installed${NC}"
    echo "Installing Git..."
    sudo apt-get update && sudo apt-get install -y git
    echo -e "${GREEN}✅ Git installed${NC}"
fi

# Create .env if not exists
echo ""
echo "📝 Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✅ Created .env file from template${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env and fill in your credentials${NC}"
    echo ""
    echo "Required variables:"
    echo "  - API_ID (from my.telegram.org)"
    echo "  - API_HASH (from my.telegram.org)"
    echo "  - BOT_TOKEN (from @BotFather)"
    echo "  - ANTHROPIC_API_KEY or OPENAI_API_KEY"
    echo "  - ADMIN_ID (your Telegram user ID)"
    echo ""
    read -p "Press Enter to edit .env now (or Ctrl+C to exit and edit manually)..."
    ${EDITOR:-nano} .env
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

# Create Docker network
echo ""
echo "🌐 Setting up Docker network..."
if docker network ls | grep -q yagami_network; then
    echo -e "${GREEN}✅ Docker network already exists${NC}"
else
    docker network create yagami_network
    echo -e "${GREEN}✅ Docker network created${NC}"
fi

# Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p logs generated_bots temp
chmod 755 logs generated_bots temp
echo -e "${GREEN}✅ Directories created${NC}"

# Install Python dependencies (optional, for local development)
echo ""
read -p "Do you want to install Python dependencies for local development? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📦 Installing Python dependencies..."
    if command_exists python3-venv; then
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        echo -e "${GREEN}✅ Python dependencies installed in virtual environment${NC}"
        echo -e "${YELLOW}💡 Activate with: source venv/bin/activate${NC}"
    else
        echo -e "${YELLOW}⚠️  python3-venv not found, skipping...${NC}"
    fi
fi

# Final checks
echo ""
echo "🔍 Validating .env configuration..."
if [ -f .env ]; then
    missing_vars=()
    required_vars=("API_ID" "API_HASH" "BOT_TOKEN" "ADMIN_ID")

    for var in "${required_vars[@]}"; do
        if ! grep -q "^${var}=..*" .env; then
            missing_vars+=("$var")
        fi
    done

    if [ ${#missing_vars[@]} -gt 0 ]; then
        echo -e "${RED}❌ Missing required environment variables:${NC}"
        for var in "${missing_vars[@]}"; do
            echo "   - $var"
        done
        echo ""
        echo -e "${YELLOW}Please edit .env and fill in all required variables${NC}"
    else
        echo -e "${GREEN}✅ All required variables are set${NC}"
    fi

    # Check AI provider
    if ! grep -q "^ANTHROPIC_API_KEY=..*" .env && ! grep -q "^OPENAI_API_KEY=..*" .env; then
        echo -e "${YELLOW}⚠️  No AI API key found. Please set either ANTHROPIC_API_KEY or OPENAI_API_KEY${NC}"
    fi
fi

# Summary
echo ""
echo "================================"
echo "🎉 Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Make sure .env is properly configured"
echo "2. Run: docker-compose up -d"
echo "3. Check logs: docker-compose logs -f"
echo ""
echo "Useful commands:"
echo "  - Start:   docker-compose up -d"
echo "  - Stop:    docker-compose down"
echo "  - Logs:    docker-compose logs -f"
echo "  - Rebuild: docker-compose up --build -d"
echo "  - Status:  docker-compose ps"
echo ""
echo "🔥 Happy bot generating!"
echo ""
