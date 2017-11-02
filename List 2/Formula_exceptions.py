class VariableNotAttributed(Exception):
    def __init__(self, variable_name, **kwargs):
        super().__init__(kwargs)
        self.name = variable_name

