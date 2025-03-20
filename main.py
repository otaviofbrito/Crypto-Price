import requests
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()
API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

def get_bitcoin_price():
    try:
        response = requests.get(API_URL)
        data = response.json()
        return data["bitcoin"]["usd"]
    except Exception as e:
        return f"Erro: {e}"

while True:
    price = get_bitcoin_price()
    
    text = Text()
    text.append("📈 Bitcoin Price\n", style="bold yellow")
    text.append(f"\n💰 ${price}", style="bold green")
    
    console.clear()
    console.print(Panel(text, title="📊 Cotação do Bitcoin", border_style="blue"))
    
    time.sleep(30)
