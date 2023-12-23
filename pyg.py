import os
import json
import sys

PYG_PACKAGES_DIR = 'pyg_packages'

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

def run_pygame_script(filename):
    with open(filename, 'r') as file:
        code = file.read()
    # Implement your PyGameScript interpreter logic here
    print(f'Running PyGameScript: {filename}')

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
        run_pygame_script(script_filename)
    else:
        print(f'Error: Unknown command "{command}"')
        sys.exit(1)

if __name__ == "__main__":
    main()
