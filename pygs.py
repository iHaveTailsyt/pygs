import ast
import argparse

class PyGameInterpreter(ast.NodeVisitor):
    def __init__(self):
        self.scope = {}

    def visit_Module(self, node):
        for statement in node.body:
            self.visit(statement)

    def visit_Assign(self, node):
        name = node.targets[0].id
        value = self.visit(node.value)
        self.scope[name] = value

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            return left / right

    def visit_Num(self, node):
        return node.n

    def visit_Name(self, node):
        return self.scope.get(node.id, None)

    def visit_Print(self, node):
        values = [self.visit(value) for value in node.values]
        print(*values)
        return None

def run_pygamescript(code):
    tree = ast.parse(code)
    interpreter = PyGameInterpreter()
    interpreter.visit(tree)

def main():
    parser = argparse.ArgumentParser(description='PyGameScript Interpreter')
    parser.add_argument('script_file', type=str, help='Path to the PyGameScript file to run')

    args = parser.parse_args()

    with open(args.script_file, "r") as file:
        script_code = file.read()

    run_pygamescript(script_code)

if __name__ == "__main__":
    main()
