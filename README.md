# goquant Trade Simulator

## Overview
A high-performance trade simulator for real-time estimation of transaction costs and market impact using L2 orderbook data from OKX.

### Features
- Real-time WebSocket L2 orderbook processing
- User interface for parameter input and output display
- Slippage, fee, and market impact estimation (Almgren-Chriss)
- Maker/taker proportion prediction
- Latency measurement and logging

## Project Structure

```
goquant/
│
├─ main.py                  # Entry point, launches UI
├─ requirements.txt         # Dependencies
├─ README.md                # Documentation
│
├─ ui/
│   └─ app.py               # UI logic (Streamlit)
│
├─ data/
│   └─ websocket_client.py  # WebSocket connection & orderbook processing
│
├─ models/
│   ├─ slippage.py          # Regression models for slippage
│   ├─ fees.py              # Fee calculation logic
│   ├─ market_impact.py     # Almgren-Chriss model
│   └─ maker_taker.py       # Maker/taker proportion model
│
├─ utils/
│   ├─ latency.py           # Latency measurement utilities
│   └─ logger.py            # Logging setup
│
└─ docs/
    └─ model_docs.md        # Model/algorithm documentation
```

## Setup

1. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
2. Run the application:
   ```powershell
   streamlit run main.py
   ```

## Documentation
See `docs/model_docs.md` for model and algorithm explanations.
