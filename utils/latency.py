import time

def measure_latency(start_time):
    """
    Measure internal latency in milliseconds.
    """
    return round((time.time() - start_time) * 1000, 2)
