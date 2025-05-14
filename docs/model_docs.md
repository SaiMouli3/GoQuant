# Model and Algorithm Documentation

## Slippage Estimation
- Uses orderbook walk to estimate slippage for a given notional.
- Can be extended with linear/quantile regression on historical data.

## Fee Calculation
- Rule-based, per OKX spot fee tiers.
- Replace example rates with actual OKX documentation values.

## Market Impact (Almgren-Chriss)
- Implements a simplified Almgren-Chriss model:
  - Permanent impact: gamma * Q
  - Temporary impact: eta * Q^2
  - Volatility adjustment: volatility * 0.1 * Q
- Parameters should be calibrated with real data.

## Maker/Taker Proportion
- Uses order type (market = taker, limit = maker/taker split).
- Can be extended with logistic regression on historical fills.

## Latency Measurement
- Measures processing time per tick in milliseconds.

## Optimization

### WebSocket & Data Ingestion
- **Threaded WebSocket Client:** Runs in a dedicated thread to avoid blocking UI or model calculations.
- **Auto-Reconnect & Robustness:** Implements automatic reconnection with exponential backoff on disconnects or errors.
- **Efficient Orderbook Updates:** Only processes and updates UI when the orderbook state changes, reducing unnecessary computation.

### Data Structures & Memory
- **Numpy Arrays for Orderbook:** Uses numpy arrays for fast vectorized operations and memory efficiency in orderbook depth calculations and visualization.
- **History Buffer:** Maintains a capped buffer (e.g., last 100 ticks) for historical trend analysis, minimizing memory usage.

### UI & Visualization
- **Batch UI Updates:** Uses Streamlit's session state and efficient update patterns to minimize redraws and flicker.
- **Real-Time Charts:** Visualizes orderbook depth and historical metrics with minimal overhead.
- **Threshold Alerts:** Only triggers UI alerts when user-defined thresholds are crossed, reducing noise.

### Latency & Performance Profiling
- **Component Latency Measurement:** Measures and displays per-tick latency for data ingestion, model computation, and UI update.
- **Profiling Hooks:** Easily extensible to add more detailed performance profiling if needed.

### Code & Logging
- **Centralized Logging:** All errors and performance events are logged for easy debugging and monitoring.
- **Minimal Data Copying:** Avoids unnecessary data duplication by passing references and using efficient data structures.

### Extensibility
- **Modular Architecture:** Each model and utility is in its own module, making it easy to optimize or swap out components as needed.
