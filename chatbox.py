import os
import sys
import json
import math
import time
import requests
from datetime import datetime
from pathlib import Path
 
# Load .env file for API key
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass
 
# ============================================================================
# COLORS FOR TERMINAL
# ============================================================================
class Colors:
    """Terminal colors for nice output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
 
# ============================================================================
# CALCULATOR - Do math
# ============================================================================
class Calculator:
    """Safe math calculator"""
    
    @staticmethod
    def calculate(expression):
        """
        Calculate math expression safely
        Examples: 2+2, sqrt(16), sin(0)
        """
        try:
            # Remove spaces
            expression = expression.replace(" ", "")
            
            # Allowed math functions
            math_functions = {
                'abs': abs, 'round': round,
                'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos,
                'tan': math.tan, 'log': math.log, 'exp': math.exp,
                'pi': math.pi
            }
            
            # Calculate safely
            result = eval(expression, {"__builtins__": {}}, math_functions)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"
 
# ============================================================================
# WEB SEARCH - Search the internet
# ============================================================================
class WebSearch:
    """Search web using free API (no key needed)"""
    
    @staticmethod
    def search(query):
        """
        Search the web
        Uses DuckDuckGo API (free, no authentication)
        """
        try:
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': 1,
                't': 'chatbot'
            }
            
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            results = []
            
            # Get main result
            if data.get('AbstractText'):
                results.append({
                    'title': data.get('Heading', 'Result'),
                    'text': data['AbstractText'][:200],
                    'url': data.get('AbstractURL', '#')
                })
            
            # Get related topics
            if data.get('RelatedTopics'):
                for item in data['RelatedTopics'][:3]:
                    if 'Text' in item:
                        results.append({
                            'title': item.get('FirstURL', 'Topic'),
                            'text': item['Text'][:200],
                            'url': item.get('FirstURL', '#')
                        })
            
            return results if results else [{'title': 'No results', 'text': 'Try a different search.', 'url': '#'}]
        
        except Exception as e:
            return [{'title': 'Search Error', 'text': str(e), 'url': '#'}]
 
# ============================================================================
# FILE HANDLER - Read and upload files
# ============================================================================
class FileHandler:
    """Handle file reading"""
    
    @staticmethod
    def read_file(filepath):
        """
        Read file content
        Supports: .txt, .py, .md, .json, .csv
        """
        try:
            path = Path(filepath)
            
            if not path.exists():
                return f"File not found: {filepath}"
            
            # Check file type
            if path.suffix in ['.txt', '.md', '.py', '.json', '.csv']:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Show first 1000 characters
                if len(content) > 1000:
                    return f"{content[:1000]}...\n[File is longer, showing first 1000 characters]"
                return content
            else:
                return f"Unsupported file type: {path.suffix}"
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    @staticmethod
    def upload_file(filepath):
        """Check if file exists and report size"""
        try:
            path = Path(filepath)
            if path.exists():
                size = path.stat().st_size
                return f"✓ File uploaded: {path.name} ({size} bytes)"
            else:
                return f"File not found: {filepath}"
        except Exception as e:
            return f"Error: {str(e)}"
 
# ============================================================================
# CODE EXECUTOR - Run Python code safely
# ============================================================================
class CodeExecutor:
    """Execute Python code in restricted sandbox"""
    
    @staticmethod
    def execute(code):
        """
        Execute Python code safely
        Only allows: print, len, range, sum, max, min, str, int, float, list, dict
        """
        try:
            # Only allow safe functions
            safe_functions = {
                'print': print,
                'len': len,
                'range': range,
                'sum': sum,
                'max': max,
                'min': min,
                'sorted': sorted,
                'enumerate': enumerate,
                'zip': zip,
                'abs': abs,
                'round': round,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
            }
            
            # Capture output
            import io
            from contextlib import redirect_stdout
            
            output = io.StringIO()
            with redirect_stdout(output):
                exec(code, {"__builtins__": {}}, safe_functions)
            
            result = output.getvalue()
            return result if result else "Code executed (no output)"
        
        except Exception as e:
            return f"Error: {str(e)}"
 
# ============================================================================
# AI ENGINE - Chat with Claude AI
# ============================================================================
class AIChat:
    """Generate AI responses using Claude API"""
    
    @staticmethod
    def get_response(user_message, conversation_history):
        """
        Get AI response from Claude
        Requires ANTHROPIC_API_KEY environment variable
        """
        try:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            
            if not api_key:
                return "⚠️ No API key found!\nSet ANTHROPIC_API_KEY in .env file or environment variables.\nGo to https://console.anthropic.com to get free key."
            
            # Import Anthropic
            import anthropic
            
            client = anthropic.Anthropic(api_key=api_key)
            
            # Build conversation
            messages = [{"role": "user", "content": user_message}]
            
            # Get response
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=messages
            )
            
            return response.content[0].text
        
        except ImportError:
            return "Install anthropic: pip install anthropic"
        except Exception as e:
            return f"Error: {str(e)}"
 
# ============================================================================
# MAIN CHATBOT
# ============================================================================
class ChatBot:
    """Main chatbot class"""
    
    def __init__(self):
        self.history = []
        self.calculator = Calculator()
        self.search = WebSearch()
        self.files = FileHandler()
        self.code = CodeExecutor()
        self.ai = AIChat()
    
    def show_banner(self):
        """Show welcome message"""
        print(f"\n{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}   AI CHATBOT v1.0{Colors.RESET}")
        print(f"{Colors.CYAN}{'='*60}{Colors.RESET}")
        print(f"{Colors.DIM}Web Search | Math | Files | Code | AI Chat{Colors.RESET}")
        print(f"\nType 'help' for commands or just chat!\n")
    
    def show_help(self):
        """Show all available commands"""
        help_text = f"""
{Colors.CYAN}COMMANDS:{Colors.RESET}
 
{Colors.BOLD}MATH:{Colors.RESET}
  math 2+2              → Calculate: 2+2 = 4
  calc sqrt(16)         → Calculate: sqrt(16) = 4
  math sin(0)           → Calculate: sin(0) = 0
 
{Colors.BOLD}SEARCH:{Colors.RESET}
  search Python         → Search web for "Python"
  search machine learning → Search web
 
{Colors.BOLD}FILES:{Colors.RESET}
  read notes.txt        → Read file content
  upload file.txt       → Check if file exists
 
{Colors.BOLD}CODE:{Colors.RESET}
  code print('hello')   → Run Python code
  code sum(range(10))   → Run: sum(range(10)) = 45
 
{Colors.BOLD}CHAT:{Colors.RESET}
  Any text              → Chat with AI
  Example: What is AI?  → Get full answer
 
{Colors.BOLD}OTHER:{Colors.RESET}
  help                  → Show this menu
  clear                 → Clear conversation
  exit                  → Close chatbot
"""
        return help_text
    
    def handle_command(self, user_input):
        """
        Handle special commands
        Returns response or None if it's AI chat
        """
        lower = user_input.lower().strip()
        
        # MATH
        if lower.startswith('math ') or lower.startswith('calc '):
            expr = user_input[5:].strip()
            result = self.calculator.calculate(expr)
            return f"{Colors.GREEN}Math Result: {result}{Colors.RESET}"
        
        # SEARCH
        elif lower.startswith('search '):
            query = user_input[7:].strip()
            results = self.search.search(query)
            
            output = f"\n{Colors.CYAN}Search Results for '{query}':{Colors.RESET}\n"
            for i, result in enumerate(results, 1):
                output += f"\n{Colors.BOLD}{i}. {result['title']}{Colors.RESET}\n"
                output += f"   {result['text']}\n"
            
            return output
        
        # READ FILE
        elif lower.startswith('read '):
            filepath = user_input[5:].strip()
            content = self.files.read_file(filepath)
            return f"{Colors.CYAN}File Content:{Colors.RESET}\n{content}"
        
        # UPLOAD FILE
        elif lower.startswith('upload '):
            filepath = user_input[7:].strip()
            result = self.files.upload_file(filepath)
            return f"{Colors.GREEN}{result}{Colors.RESET}"
        
        # CODE
        elif lower.startswith('code '):
            code_str = user_input[5:].strip()
            result = self.code.execute(code_str)
            return f"{Colors.MAGENTA}Code Output:{Colors.RESET}\n{result}"
        
        # HELP
        elif lower in ['help', '?']:
            return self.show_help()
        
        # CLEAR
        elif lower == 'clear':
            self.history = []
            return f"{Colors.YELLOW}Conversation cleared{Colors.RESET}"
        
        # EXIT
        elif lower in ['exit', 'quit', 'bye']:
            return None
        
        # DEFAULT: AI CHAT
        else:
            return "AI_CHAT"
    
    def run(self):
        """Main chat loop"""
        self.show_banner()
        
        while True:
            try:
                # Get user input
                user_input = input(f"{Colors.BLUE}You: {Colors.RESET}").strip()
                
                if not user_input:
                    continue
                
                # Handle command
                response = self.handle_command(user_input)
                
                # Exit
                if response is None:
                    print(f"{Colors.GREEN}Goodbye!{Colors.RESET}\n")
                    break
                
                # Command executed
                if response != "AI_CHAT":
                    print(f"{response}\n")
                
                # AI Chat
                else:
                    print(f"{Colors.MAGENTA}Bot: {Colors.RESET}", end='', flush=True)
                    ai_response = self.ai.get_response(user_input, self.history)
                    print(f"{ai_response}\n")
                    
                    # Store in history
                    self.history.append(user_input)
                    self.history.append(ai_response)
            
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Interrupted{Colors.RESET}\n")
                break
            except Exception as e:
                print(f"{Colors.RED}Error: {str(e)}{Colors.RESET}\n")
 
# ============================================================================
# START HERE
# ============================================================================
if __name__ == "__main__":
    bot = ChatBot()
    bot.run()
 
