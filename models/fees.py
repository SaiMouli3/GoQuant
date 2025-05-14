def calculate_fees(quantity_usd, fee_tier):
    """
    Calculate expected fees based on OKX spot fee tiers (example values).
    """
    # Example fee rates (should be replaced with actual OKX rates)
    fee_rates = {
        "Regular": 0.001,
        "VIP1": 0.0008,
        "VIP2": 0.0006
    }
    rate = fee_rates.get(fee_tier, 0.001)
    return round(quantity_usd * rate, 4)
