import time
import numpy as np
from threading import Thread

token = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOjEwLCJlbWFpbCI6ImUxMTU2MjM4QHUubnVzLmVkdSIsImlhdCI6MTcyMjk5NDg5M30.T-m5Mdvki4vSu8kRtdS-SNjVyMw5obmKfhbep_aRgzE
NSC = NUSwapConnector(token)

symbol = "BTCUSD" 
pos_held = False
trade_amount = 0.001  
transaction_cost = 0.001  
initial_window = 20 
initial_threshold = 0.05  
stop_loss_threshold = 0.98 
take_profit_threshold = 1.02 
api_rate_limit = 60 

def calculate_risk_adjusted_entry_price(price):
    return price * (1 + transaction_cost)

def calculate_risk_adjusted_exit_price(price):
    return price * (1 - transaction_cost)

def calculate_dynamic_momentum_threshold(close_list):
    returns = np.diff(close_list) / close_list[:-1]
    volatility = np.std(returns)
    dynamic_threshold = initial_threshold * (1 + volatility)
    return dynamic_threshold

def trading_loop():
    global pos_held
    purchase_price = None

    while True:
        print("\nChecking Price")

        market_data = NSC.getMarketHistory(symbol)

        close_list = [data['close'] for data in market_data]
        close_list = np.array(close_list, dtype=np.float64)

        dynamic_momentum_threshold = calculate_dynamic_momentum_threshold(close_list)

        returns = np.diff(close_list[-initial_window:]) / close_list[-initial_window:-1]
        momentum = np.mean(returns)
        last_price = close_list[-1]

        print(f"Momentum: {momentum:.4f}, Last Price: {last_price:.2f}, Dynamic Threshold: {dynamic_momentum_threshold:.4f}")

        # Trading Logic
        if momentum > dynamic_momentum_threshold and not pos_held:  # Buy signal
            entry_price = calculate_risk_adjusted_entry_price(last_price)
            print("Buy signal detected! Placing order...")
            NSC.placeOrder(symbol, 'Market', 'Buy', trade_amount)
            pos_held = True
            purchase_price = last_price
            print(f"Buy order placed at {last_price:.2f}")

        elif momentum < -dynamic_momentum_threshold and pos_held:  # Sell signal
            exit_price = calculate_risk_adjusted_exit_price(last_price)
            print("Sell signal detected! Placing order...")
            NSC.placeOrder(symbol, 'Market', 'Sell', trade_amount)
            pos_held = False
            print(f"Sell order placed at {last_price:.2f}")

        # Stop-Loss and Take-Profit Logic
        if pos_held:
            if last_price <= purchase_price * stop_loss_threshold:
                print("Stop-loss triggered! Placing sell order...")
                NSC.placeOrder(symbol, 'Market', 'Sell', trade_amount)
                pos_held = False
                print(f"Stop-loss sell order placed at {last_price:.2f}")
            elif last_price >= purchase_price * take_profit_threshold:
                print("Take-profit triggered! Placing sell order...")
                NSC.placeOrder(symbol, 'Market', 'Sell', trade_amount)
                pos_held = False
                print(f"Take-profit sell order placed at {last_price:.2f}")

        time.sleep(api_rate_limit)

trading_thread = Thread(target=trading_loop)
trading_thread.daemon = True
trading_thread.start()

while True:
    time.sleep(1)