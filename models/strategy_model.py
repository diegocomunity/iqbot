class StrategyModel:
    def __init__(self, strategy_name, description, parameters, signal_strength):
        self.strategy_name = strategy_name
        self.description = description
        self.parameters = parameters
        self.signal_strength = signal_strength

    def __str__(self):
        return f"Strategy Name: {self.strategy_name}\nDescription: {self.description}\nParameters: {self.parameters}\nSignal Strength: {self.signal_strength}"
