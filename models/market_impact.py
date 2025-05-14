import numpy as np

def estimate_market_impact(orderbook, quantity_usd, volatility):
    """
    Almgren-Chriss market impact model (simplified for demo).
    """
    if orderbook is None:
        return 0.0
    # Model parameters (should be calibrated)
    gamma = 2e-6  # permanent impact
    eta = 1e-5    # temporary impact
    # Estimate average price and volatility
    asks = orderbook.get("asks", [])
    if not asks:
        return 0.0
    mid_price = (float(asks[0][0]) + float(orderbook["bids"][0][0])) / 2
    # Almgren-Chriss: MI = gamma * Q + eta * Q^2
    Q = quantity_usd / mid_price
    impact = gamma * Q + eta * Q**2 + volatility * 0.1 * Q
    return round(impact, 6)
