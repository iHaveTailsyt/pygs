from lark import Lark, Transformer, v_args

# Define the PyGameScript grammar
grammar = """
    start: stmt+

    ?stmt: assign_stmt
         | expr_stmt
         | print_stmt

    assign_stmt: NAME "=" expr

    ?expr: atom
         | expr "+" expr -> add
         | expr "-" expr -> subtract
         | expr "*" expr -> multiply
         | expr "/" expr -> divide

    ?atom: NUMBER -> number
         | NAME -> variable

    print_stmt: "print" "(" expr ("," expr)* ")"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS

    %ignore WS
"""

# Transformer to convert the parse tree to a format suitable for interpretation
@v_args(inline=True)
class PyGameTransformer(Transformer):
    def add(self, left, right):
        return left + right

    def subtract(self, left, right):
        return left - right

    def multiply(self, left, right):
        return left * right

    def divide(self, left, right):
        return left / right

    def number(self, value):
        return float(value)

    def variable(self, name):
        return name

def run_pygamescript(code):
    parser = Lark(grammar, parser='lalr', transformer=PyGameTransformer())
    tree = parser.parse(code)
    interpreter = PyGameInterpreter()
    interpreter.visit(tree)

class PyGameInterpreter:
    def __init__(self):
        self.scope = {}

    def visit_assign_stmt(self, tree):
        name, value = tree.children
        self.scope[name] = value

    def visit_expr_stmt(self, tree):
        return self.visit(tree.children[0])

    def visit_print_stmt(self, tree):
        values = [self.visit(child) for child in tree.children]
        print(*values)

    def visit_add(self, tree):
        left, right = tree.children
        return left + right

    def visit_subtract(self, tree):
        left, right = tree.children
        return left - right

    def visit_multiply(self, tree):
        left, right = tree.children
        return left * right

    def visit_divide(self, tree):
        left, right = tree.children
        return left / right

    def visit_number(self, tree):
        return float(tree.children[0])

    def visit_variable(self, tree):
        return self.scope.get(tree.children[0], None)

if __name__ == "__main__":
    with open("your_script.pygs", "r") as file:
        script_code = file.read()

    run_pygamescript(script_code)
