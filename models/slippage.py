import numpy as np
from sklearn.linear_model import LinearRegression, QuantileRegressor

def estimate_slippage(orderbook, quantity_usd):
    """
    Estimate expected slippage using linear or quantile regression on orderbook depth.
    """
    if orderbook is None:
        return 0.0
    asks = orderbook.get("asks", [])
    bids = orderbook.get("bids", [])
    if not asks or not bids:
        return 0.0
    # Simple model: walk the book for quantity
    total_qty = 0
    cost = 0
    for price, qty in asks:
        price = float(price)
        qty = float(qty)
        if total_qty + price * qty >= quantity_usd:
            needed = (quantity_usd - total_qty) / price
            cost += needed * price
            break
        else:
            cost += qty * price
            total_qty += price * qty
    # Slippage = (actual cost - notional) / notional
    slippage = (cost - quantity_usd) / quantity_usd
    return round(slippage, 6)
