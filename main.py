import tkinter as tk
import requests
from collections import deque
from PIL import Image, ImageTk

API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

btc_path = "/home/orangepi/Crypto-Price/files/btc.png"
eth_path = "/home/orangepi/Crypto-Price/files/eth.png"

prev_prices_btc = deque(maxlen=20)
prev_prices_eth = deque(maxlen=20)

def get_crypto_prices():
    global prev_prices_btc, prev_prices_eth
    try:
        response = requests.get(API_URL)
        data = response.json()

        btc_price = data['bitcoin']['usd']
        eth_price = data['ethereum']['usd']
        
        btc_price_str = f"{btc_price:,.2f}"
        eth_price_str = f"{eth_price:,.2f}"
        btc_symbol = " "
        btc_symbol_color = "white"

        eth_symbol = " "
        eth_symbol_color = "white"

        if prev_prices_btc:
            oldest_btc_price = prev_prices_btc[0]  
            if btc_price > oldest_btc_price:
                btc_symbol = "▲" 
                btc_symbol_color = "green"
            else:
                btc_symbol = "▼"  
                btc_symbol_color = "red"
        
        if prev_prices_eth:
            oldest_eth_price = prev_prices_eth[0]  
            if eth_price > oldest_eth_price:
                eth_symbol = "▲"  
                eth_symbol_color = "green"
            else:
                eth_symbol = "▼" 
                eth_symbol_color = "red"

        btc_label.config(text=f"BTC: ${btc_price_str}")
        btc_symbol_label.config(text=btc_symbol, fg=btc_symbol_color)

        eth_label.config(text=f"ETH: ${eth_price_str}")
        eth_symbol_label.config(text=eth_symbol, fg=eth_symbol_color)

        prev_prices_btc.append(btc_price)
        prev_prices_eth.append(eth_price)
        
    except Exception as e:
        btc_label.config(text="[ERROR]", fg="red")
        eth_label.config(text="[ERROR]", fg="red")

    root.after(300000, get_crypto_prices)  # 5 min

def exit_fullscreen(event):
    root.attributes("-fullscreen", False)  

root = tk.Tk()
root.attributes("-fullscreen", True)  
root.configure(bg="black")
root.geometry("320x240")


btc_image = Image.open(btc_path) 
btc_image = btc_image.resize((40, 40), Image.LANCZOS)
btc_photo = ImageTk.PhotoImage(btc_image)

eth_image = Image.open(eth_path) 
eth_image = eth_image.resize((40, 40), Image.LANCZOS)
eth_photo = ImageTk.PhotoImage(eth_image)

frame = tk.Frame(root, bg="black")
frame.place(relx=0.5, rely=0.5, anchor="center")

btc_frame = tk.Frame(frame, bg="black")
btc_frame.grid(row=0, column=0, pady=10)

btc_icon = tk.Label(btc_frame, image=btc_photo, bg="black")
btc_icon.grid(row=0, column=0, padx=10)

btc_label = tk.Label(btc_frame, text="Loading...", font=("Arial", 20, "bold"), fg="white", bg="black")
btc_label.grid(row=0, column=1)

eth_frame = tk.Frame(frame, bg="black")
eth_frame.grid(row=1, column=0, pady=10)

eth_icon = tk.Label(eth_frame, image=eth_photo, bg="black")
eth_icon.grid(row=0, column=0, padx=10)

eth_label = tk.Label(eth_frame, text="Loading...", font=("Arial", 20, "bold"), fg="white", bg="black")
eth_label.grid(row=0, column=1)

btc_symbol_label = tk.Label(btc_frame, text="", font=("Arial", 20, "bold"), bg="black")
btc_symbol_label.grid(row=0, column=2)

eth_symbol_label = tk.Label(eth_frame, text="", font=("Arial", 20, "bold"), bg="black")
eth_symbol_label.grid(row=0, column=2)

root.bind("<Escape>", exit_fullscreen)  

get_crypto_prices()
root.mainloop()
