import threading
import websocket
import json
import time
from utils.logger import get_logger

logger = get_logger()

class OrderBookClient:
    def __init__(self, symbol):
        self.symbol = symbol
        self.ws_url = f"wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/{symbol}"
        self.orderbook = None
        self._running = False
        self._thread = None

    def start(self):
        if self._thread is None or not self._thread.is_alive():
            self._running = True
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()

    def is_running(self):
        return self._running

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()

    def get_orderbook(self):
        return self.orderbook

    def _run(self):
        while self._running:
            try:
                ws = websocket.create_connection(self.ws_url, timeout=10)
                while self._running:
                    msg = ws.recv()
                    data = json.loads(msg)
                    self.orderbook = data
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                time.sleep(2)
