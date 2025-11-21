"""
YAGAMI UNIVERZE - GitHub Repository Scanner
"""

import re
import logging
from typing import Dict, List, Optional, Set
from pathlib import Path
import tempfile
import shutil
import git
from bot.config import Config

logger = logging.getLogger(__name__)


class RepoScanner:
    """Scan GitHub repositories to extract bot structure and env vars"""
    
    def __init__(self):
        self.github_token = Config.GITHUB_TOKEN
    
    async def scan_repository(self, repo_url: str) -> Dict:
        """
        Scan a GitHub repository and extract information
        
        Returns:
            Dict with:
            {
                'env_vars': ['VAR1', 'VAR2', ...],
                'language': 'python',
                'framework': 'pyrogram',
                'structure': {...},
                'readme_content': '...',
                'dependencies': [...]
            }
        """
        logger.info(f"Scanning repository: {repo_url}")
        
        try:
            # Clone repository to temp directory
            temp_dir = tempfile.mkdtemp()
            
            try:
                # Clone with authentication if token available
                if self.github_token:
                    auth_url = repo_url.replace('https://', f'https://{self.github_token}@')
                    repo = git.Repo.clone_from(auth_url, temp_dir, depth=1)
                else:
                    repo = git.Repo.clone_from(repo_url, temp_dir, depth=1)
                
                repo_path = Path(temp_dir)
                
                # Detect language and framework
                language, framework = self._detect_language_and_framework(repo_path)
                
                # Extract environment variables
                env_vars = self._extract_env_variables(repo_path, language)
                
                # Get project structure
                structure = self._get_project_structure(repo_path)
                
                # Read README if exists
                readme_content = self._read_readme(repo_path)
                
                # Extract dependencies
                dependencies = self._extract_dependencies(repo_path, language)
                
                # Extract configuration patterns
                config_patterns = self._extract_config_patterns(repo_path, language)
                
                return {
                    'env_vars': sorted(list(env_vars)),
                    'language': language,
                    'framework': framework,
                    'structure': structure,
                    'readme_content': readme_content,
                    'dependencies': dependencies,
                    'config_patterns': config_patterns,
                    'repo_url': repo_url
                }
                
            finally:
                # Cleanup temp directory
                shutil.rmtree(temp_dir, ignore_errors=True)
        
        except Exception as e:
            logger.error(f"Error scanning repository: {e}")
            raise
    
    def _detect_language_and_framework(self, repo_path: Path) -> tuple:
        """Detect programming language and framework"""
        
        language = "unknown"
        framework = "unknown"
        
        # Check for Python
        if (repo_path / "requirements.txt").exists() or \
           (repo_path / "setup.py").exists() or \
           (repo_path / "pyproject.toml").exists():
            language = "python"
            
            # Detect Python framework
            requirements = self._read_file_safe(repo_path / "requirements.txt")
            if requirements:
                if "pyrogram" in requirements.lower():
                    framework = "pyrogram"
                elif "aiogram" in requirements.lower():
                    framework = "aiogram"
                elif "telebot" in requirements.lower() or "pytelegrambotapi" in requirements.lower():
                    framework = "telebot"
                elif "python-telegram-bot" in requirements.lower():
                    framework = "python-telegram-bot"
        
        # Check for Node.js
        elif (repo_path / "package.json").exists():
            language = "nodejs"
            
            package_json = self._read_file_safe(repo_path / "package.json")
            if package_json:
                if "telegraf" in package_json.lower():
                    framework = "telegraf"
                elif "node-telegram-bot-api" in package_json.lower():
                    framework = "node-telegram-bot-api"
                elif "grammy" in package_json.lower():
                    framework = "grammy"
        
        # Check for Go
        elif (repo_path / "go.mod").exists():
            language = "go"
            go_mod = self._read_file_safe(repo_path / "go.mod")
            if go_mod and "telegram" in go_mod.lower():
                framework = "telegram-bot-api"
        
        # Check for PHP
        elif (repo_path / "composer.json").exists():
            language = "php"
            framework = "telegram-bot-sdk"
        
        return language, framework
    
    def _extract_env_variables(self, repo_path: Path, language: str) -> Set[str]:
        """Extract environment variables from code"""
        
        env_vars = set()
        
        # Check .env.example files
        for env_file in ['.env.example', '.env.sample', 'env.example', '.env.template']:
            env_path = repo_path / env_file
            if env_path.exists():
                content = self._read_file_safe(env_path)
                if content:
                    # Extract variable names
                    for line in content.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            var_name = line.split('=')[0].strip()
                            if var_name:
                                env_vars.add(var_name)
        
        # Scan code files for environment variables
        patterns = {
            'python': [
                r'os\.getenv\([\'"]([A-Z_]+)[\'"]\)',
                r'os\.environ\[[\'"]([A-Z_]+)[\'"]\]',
                r'config\.[A-Z_]+ = os\.getenv\([\'"]([A-Z_]+)[\'"]\)',
            ],
            'nodejs': [
                r'process\.env\.([A-Z_]+)',
                r'process\.env\[[\'"]([A-Z_]+)[\'"]\]',
            ],
            'go': [
                r'os\.Getenv\([\'"]([A-Z_]+)[\'"]\)',
            ],
            'php': [
                r'getenv\([\'"]([A-Z_]+)[\'"]\)',
                r'\$_ENV\[[\'"]([A-Z_]+)[\'"]\]',
            ]
        }
        
        if language in patterns:
            for file_path in repo_path.rglob('*'):
                if file_path.is_file() and self._is_code_file(file_path, language):
                    content = self._read_file_safe(file_path)
                    if content:
                        for pattern in patterns[language]:
                            matches = re.findall(pattern, content)
                            env_vars.update(matches)
        
        return env_vars
    
    def _get_project_structure(self, repo_path: Path) -> Dict:
        """Get simplified project structure"""
        
        structure = {
            'files': [],
            'directories': []
        }
        
        # Get top-level items only
        for item in repo_path.iterdir():
            if item.name.startswith('.'):
                continue
            
            if item.is_file():
                structure['files'].append(item.name)
            elif item.is_dir():
                structure['directories'].append(item.name)
        
        return structure
    
    def _read_readme(self, repo_path: Path) -> Optional[str]:
        """Read README file"""
        
        for readme_name in ['README.md', 'README.rst', 'README.txt', 'README']:
            readme_path = repo_path / readme_name
            if readme_path.exists():
                return self._read_file_safe(readme_path)
        
        return None
    
    def _extract_dependencies(self, repo_path: Path, language: str) -> List[str]:
        """Extract project dependencies"""
        
        dependencies = []
        
        if language == "python":
            req_path = repo_path / "requirements.txt"
            if req_path.exists():
                content = self._read_file_safe(req_path)
                if content:
                    for line in content.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Extract package name without version
                            pkg = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                            if pkg:
                                dependencies.append(pkg)
        
        elif language == "nodejs":
            pkg_path = repo_path / "package.json"
            if pkg_path.exists():
                import json
                content = self._read_file_safe(pkg_path)
                if content:
                    try:
                        pkg_data = json.loads(content)
                        deps = pkg_data.get('dependencies', {})
                        dependencies.extend(deps.keys())
                    except json.JSONDecodeError:
                        pass
        
        return dependencies
    
    def _extract_config_patterns(self, repo_path: Path, language: str) -> Dict:
        """Extract configuration patterns from the code"""
        
        patterns = {
            'has_database': False,
            'has_redis': False,
            'has_webhooks': False,
            'has_api_calls': False,
            'has_file_handling': False
        }
        
        # Search for common patterns in code
        for file_path in repo_path.rglob('*'):
            if file_path.is_file() and self._is_code_file(file_path, language):
                content = self._read_file_safe(file_path)
                if content:
                    content_lower = content.lower()
                    
                    if any(db in content_lower for db in ['sqlalchemy', 'mongodb', 'psycopg', 'mysql']):
                        patterns['has_database'] = True
                    
                    if 'redis' in content_lower:
                        patterns['has_redis'] = True
                    
                    if any(wh in content_lower for wh in ['webhook', 'set_webhook']):
                        patterns['has_webhooks'] = True
                    
                    if any(api in content_lower for api in ['requests.', 'aiohttp', 'httpx', 'fetch(']):
                        patterns['has_api_calls'] = True
                    
                    if any(fh in content_lower for fh in ['open(', 'file.write', 'fs.write']):
                        patterns['has_file_handling'] = True
        
        return patterns
    
    def _is_code_file(self, file_path: Path, language: str) -> bool:
        """Check if file is a code file for the given language"""
        
        extensions = {
            'python': ['.py'],
            'nodejs': ['.js', '.ts'],
            'go': ['.go'],
            'php': ['.php']
        }
        
        if language in extensions:
            return file_path.suffix in extensions[language]
        
        return False
    
    def _read_file_safe(self, file_path: Path) -> Optional[str]:
        """Safely read a file"""
        
        try:
            return file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            logger.warning(f"Could not read {file_path}: {e}")
            return None
    
    def generate_env_template(self, env_vars: List[str], readme_content: Optional[str] = None) -> str:
        """Generate .env template from extracted variables"""
        
        template = "# Environment Variables\n"
        template += "# Fill in the values below\n\n"
        
        # Group variables by category
        telegram_vars = []
        database_vars = []
        api_vars = []
        other_vars = []
        
        for var in env_vars:
            var_lower = var.lower()
            if any(t in var_lower for t in ['bot', 'telegram', 'api_id', 'api_hash']):
                telegram_vars.append(var)
            elif any(d in var_lower for d in ['database', 'db_', 'sql', 'mongo']):
                database_vars.append(var)
            elif 'api' in var_lower or 'key' in var_lower or 'token' in var_lower:
                api_vars.append(var)
            else:
                other_vars.append(var)
        
        # Add Telegram section
        if telegram_vars:
            template += "# Telegram Configuration\n"
            for var in telegram_vars:
                template += f"{var}=\n"
            template += "\n"
        
        # Add API section
        if api_vars:
            template += "# API Keys\n"
            for var in api_vars:
                template += f"{var}=\n"
            template += "\n"
        
        # Add Database section
        if database_vars:
            template += "# Database Configuration\n"
            for var in database_vars:
                template += f"{var}=\n"
            template += "\n"
        
        # Add other variables
        if other_vars:
            template += "# Other Configuration\n"
            for var in other_vars:
                template += f"{var}=\n"
        
        return template
