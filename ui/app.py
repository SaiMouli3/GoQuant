import streamlit as st
import time
import numpy as np
import pandas as pd
from data.websocket_client import OrderBookClient
from models.slippage import estimate_slippage
from models.fees import calculate_fees
from models.market_impact import estimate_market_impact
from models.maker_taker import predict_maker_taker
from utils.latency import measure_latency
from utils.logger import get_logger

logger = get_logger()

# Global orderbook client
orderbook_client = None


def run_app():
    global orderbook_client
    st.set_page_config(page_title="GoQuant Trade Simulator", layout="wide")
    st.title("GoQuant Trade Simulator")

    # Sidebar/Input panel
    st.sidebar.header("Input Parameters")
    exchange = st.sidebar.selectbox("Exchange", ["OKX"])
    asset = st.sidebar.text_input("Spot Asset", "BTC-USDT-SWAP")
    order_type = st.sidebar.selectbox("Order Type", ["market"])
    quantity_usd = st.sidebar.number_input("Quantity (USD)", min_value=1.0, value=100.0)
    volatility = st.sidebar.slider("Volatility", min_value=0.0, max_value=1.0, value=0.1)
    fee_tier = st.sidebar.selectbox("Fee Tier", ["Regular", "VIP1", "VIP2"])  # Example tiers

    # Start WebSocket client if not running
    if orderbook_client is None or not orderbook_client.is_running():
        orderbook_client = OrderBookClient(asset)
        orderbook_client.start()

    # Output panel
    st.header("Simulation Output")
    col1, col2 = st.columns([2, 1])
    # For historical trend
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    # For alert threshold
    slippage_threshold = st.sidebar.number_input("Slippage Alert Threshold", min_value=0.0, value=0.01, step=0.001)
    impact_threshold = st.sidebar.number_input("Impact Alert Threshold", min_value=0.0, value=0.01, step=0.001)

    with col1:
        orderbook_chart = st.empty()
        trend_chart = st.empty()
    with col2:
        slippage_box = st.empty()
        fees_box = st.empty()
        impact_box = st.empty()
        netcost_box = st.empty()
        makertaker_box = st.empty()
        latency_box = st.empty()
        alert_box = st.empty()

    last_tick = None
    while True:
        start_time = time.time()
        orderbook = orderbook_client.get_orderbook()
        if orderbook is not None and orderbook != last_tick:
            last_tick = orderbook
            # Model calculations
            slippage = estimate_slippage(orderbook, quantity_usd)
            fees = calculate_fees(quantity_usd, fee_tier)
            market_impact = estimate_market_impact(orderbook, quantity_usd, volatility)
            net_cost = slippage + fees + market_impact
            maker_taker = predict_maker_taker(orderbook, order_type)
            latency = measure_latency(start_time)

            # Save to history
            st.session_state['history'].append({
                'slippage': slippage,
                'fees': fees,
                'impact': market_impact,
                'net_cost': net_cost,
                'latency': latency,
                'timestamp': time.time()
            })
            # Keep only last 100
            st.session_state['history'] = st.session_state['history'][-100:]

            # Orderbook visualization
            asks = np.array(orderbook.get('asks', []), dtype=float)
            bids = np.array(orderbook.get('bids', []), dtype=float)
            import matplotlib.pyplot as plt
            import io
            fig, ax = plt.subplots(figsize=(5,3))
            if len(bids) > 0:
                ax.step(bids[:,0], np.cumsum(bids[:,1]), label='Bids', color='green')
            if len(asks) > 0:
                ax.step(asks[:,0], np.cumsum(asks[:,1]), label='Asks', color='red')
            ax.set_xlabel('Price')
            ax.set_ylabel('Cumulative Size')
            ax.legend()
            ax.set_title('Orderbook Depth')
            orderbook_chart.pyplot(fig)
            plt.close(fig)

            # Trend chart
            df = pd.DataFrame(st.session_state['history'])
            if not df.empty:
                trend_chart.line_chart(df[['slippage','impact','net_cost']])

            # Output metrics
            slippage_box.metric("Expected Slippage", f"{slippage:.6f}")
            fees_box.metric("Expected Fees", f"{fees:.4f}")
            impact_box.metric("Expected Market Impact", f"{market_impact:.6f}")
            netcost_box.metric("Net Cost", f"{net_cost:.4f}")
            makertaker_box.metric("Maker/Taker Proportion", f"{maker_taker['maker']*100:.1f}% / {maker_taker['taker']*100:.1f}%")
            latency_box.metric("Internal Latency (ms)", f"{latency}")

            # Alerts
            alert_msgs = []
            if abs(slippage) > slippage_threshold:
                alert_msgs.append(f"⚠️ Slippage {slippage:.4f} exceeds threshold!")
            if abs(market_impact) > impact_threshold:
                alert_msgs.append(f"⚠️ Impact {market_impact:.4f} exceeds threshold!")
            if alert_msgs:
                alert_box.warning("\n".join(alert_msgs))
            else:
                alert_box.info("All metrics within thresholds.")
        time.sleep(0.5)
