class Action:
    def __init__(self, action_type, figure=None):
        self.action_type = action_type
        self.figure = figure

        if self.figure is not None:
            self.description = f"{self.action_type} {self.figure.type.upper()}"
        else:
            self.description = self.action_type
