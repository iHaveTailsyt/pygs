import os
import json
import sys

PYG_PACKAGES_DIR = 'pyg_packages'

class PyGameInterpreter:
    def __init__(self):
        self.scope = {}

    def visit(self, node):
        if node['type'] == 'Program':
            for statement in node['body']:
                self.visit(statement)
        elif node['type'] == 'VariableDeclaration':
            for declaration in node['declarations']:
                self.scope[declaration['id']['name']] = self.visit(declaration['init'])
        elif node['type'] == 'Literal':
            return node['value']
        elif node['type'] == 'Identifier':
            return self.scope.get(node['name'], None)
        elif node['type'] == 'BinaryExpression':
            left = self.visit(node['left'])
            right = self.visit(node['right'])
            if node['operator'] == '+':
                return left + right
            elif node['operator'] == '-':
                return left - right
            elif node['operator'] == '*':
                return left * right
            elif node['operator'] == '/':
                return left / right
        else:
            print(f"Unsupported node type: {node['type']}")
            sys.exit(1)

    def run_pygame_script(self, code):
        ast = json.loads(code)
        for statement in ast['body']:
            self.visit(statement)

def read_package_json(package_name):
    package_dir = os.path.join(PYG_PACKAGES_DIR, package_name)
    package_json_path = os.path.join(package_dir, 'pyg.json')

    if not os.path.exists(package_json_path):
        print(f'Error: Package "{package_name}" not found.')
        sys.exit(1)

    with open(package_json_path, 'r') as json_file:
        return json.load(json_file)

def install_package(package_name, global_install=False):
    package_json = read_package_json(package_name)
    print(f'Installing package: {package_name}@{package_json["version"]}')

    # Install dependencies
    if "dependencies" in package_json:
        for dep_name in package_json["dependencies"]:
            install_package(dep_name, global_install)

    print(f'Package {package_name} successfully installed.')

def main():
    if len(sys.argv) < 2:
        print('Usage: python pyg.py <command> [arguments]')
        sys.exit(1)

    command = sys.argv[1]

    if command == 'install':
        if len(sys.argv) < 3:
            print('Usage: python pyg.py install package_name')
            sys.exit(1)
        package_name = sys.argv[2]
        install_package(package_name)
    elif command == 'run':
        if len(sys.argv) < 3:
            print('Usage: python pyg.py run script.pygs')
            sys.exit(1)
        script_filename = sys.argv[2]
        with open(script_filename, 'r') as file:
            code = file.read()
        interpreter = PyGameInterpreter()
        interpreter.run_pygame_script(code)
    else:
        print(f'Error: Unknown command "{command}"')
        sys.exit(1)

if __name__ == "__main__":
    main()
