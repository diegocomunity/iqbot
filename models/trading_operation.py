class TradingOperation:
    def __init__(self, operation_id, timestamp, entry_price, exit_price):
        self.operation_id = operation_id
        self.timestamp = timestamp
        self.entry_price = entry_price
        self.exit_price = exit_price

    def to_dict(self):
        return {
            "id": self.operation_id,
            "timestamp": self.timestamp,
            "entry_price": self.entry_price,
            "exit_price": self.exit_price
        }

    def __str__(self):
        return f"ID: {self.operation_id}, Timestamp: {self.timestamp}, Entry Price: {self.entry_price}, Exit Price: {self.exit_price}"
