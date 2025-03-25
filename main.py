import tkinter as tk
import requests
from PIL import Image, ImageTk

API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
btc_path = "files/btc.png"
eth_path = "files/eth.png"

prev_prices = {"bitcoin": None, "ethereum": None}

def get_crypto_prices():
    global prev_prices
    try:
        response = requests.get(API_URL)
        data = response.json()
        
        btc_price = data['bitcoin']['usd']
        eth_price = data['ethereum']['usd']
        
        btc_price_str = f"{btc_price:,.2f}"
        eth_price_str = f"{eth_price:,.2f}"
        
        btc_color = "white"
        eth_color = "white"
        
        if prev_prices["bitcoin"] is not None:
            btc_color = "green" if btc_price > prev_prices["bitcoin"] else "red"
        
        if prev_prices["ethereum"] is not None:
            eth_color = "green" if eth_price > prev_prices["ethereum"] else "red"
        
        btc_label.config(text=f"BTC: $ {btc_price_str}", fg=btc_color)
        eth_label.config(text=f"ETH: $ {eth_price_str}", fg=eth_color)
        
        prev_prices["bitcoin"] = btc_price
        prev_prices["ethereum"] = eth_price
    except Exception as e:
        btc_label.config(text="[ERROR]", fg="red")
        eth_label.config(text="[ERROR]", fg="red")
    root.after(300000, get_crypto_prices)

def exit_fullscreen(event):
    root.attributes("-fullscreen", False)  

root = tk.Tk()
root.attributes("-fullscreen", True)  
root.configure(bg="black")
root.geometry("320x240")
font = ("Arial", 24, "bold")


btc_image = Image.open(btc_path) 
btc_image = btc_image.resize((20, 20), Image.LANCZOS)
btc_photo = ImageTk.PhotoImage(btc_image)

eth_image = Image.open(eth_path) 
eth_image = eth_image.resize((20, 20), Image.LANCZOS)
eth_photo = ImageTk.PhotoImage(eth_image)

frame = tk.Frame(root, bg="black")
frame.place(relx=0.5, rely=0.5, anchor="center")

btc_frame = tk.Frame(frame, bg="black")
btc_frame.grid(row=0, column=0, pady=10)

btc_icon = tk.Label(btc_frame, image=btc_photo, bg="black")
btc_icon.grid(row=0, column=0, padx=10)

btc_label = tk.Label(btc_frame, text="Loading...", font=("Arial", 10, "bold"), fg="white", bg="black")
btc_label.grid(row=0, column=1)

eth_frame = tk.Frame(frame, bg="black")
eth_frame.grid(row=1, column=0, pady=10)

eth_icon = tk.Label(eth_frame, image=eth_photo, bg="black")
eth_icon.grid(row=0, column=0, padx=10)

eth_label = tk.Label(eth_frame, text="Loading...", font=("Arial", 10, "bold"), fg="white", bg="black")
eth_label.grid(row=0, column=1)

root.bind("<Escape>", exit_fullscreen)  

get_crypto_prices()
root.mainloop()
