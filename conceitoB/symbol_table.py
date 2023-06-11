
class SymbolTable():
    table = {}

    def getter(self, key):
        if key not in SymbolTable.table:
            raise Exception(f"Variable/function not declared {key}")
        return SymbolTable.table[key]

    def setter(self, key, value):
        # Check if variable types match
        if key in SymbolTable.table.keys():
            if SymbolTable.table[key][0] != value[0]:
                raise Exception(
                    f"Overwriting variable with different type {SymbolTable.table[key][0]} != {value[0]}")
        SymbolTable.table[key] = value

    # def __str__():
    #     return str(SymbolTable.table)


class LocalSymbolTable():
    def __init__(self):
        self.table = {}

    def getter(self, key):
        if key not in self.table:
            raise Exception("Variable not declared")
        return self.table[key]

    def setter(self, key, value):
        # Check if variable types match
        if key in self.table.keys():
            if self.table[key][0] != value[0]:
                raise Exception(
                    f"Overwriting variable with different type {self.table[key][0]} != {value[0]}")
        self.table[key] = value

    # def __str__(self):
    #     return str(self.table)
