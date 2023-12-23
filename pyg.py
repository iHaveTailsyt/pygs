import os
import json
import sys
import shutil
import requests
from zipfile import ZipFile

PYG_PACKAGES_DIR = 'pyg_modules'
GITHUB_API_URL = 'https://api.github.com/repos'

class PyGamePackage:
    def __init__(self, name, version, main):
        self.name = name
        self.version = version
        self.main = main

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

def download_and_extract_zip(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        with ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(destination)
    else:
        print(f'Error downloading and extracting ZIP file from {url}')
        sys.exit(1)

def install_community_package(package_name):
    package_metadata_url = f'{GITHUB_API_URL}/{package_name}/contents/pyg.json'
    response = requests.get(package_metadata_url)
    if response.status_code == 200:
        package_metadata = json.loads(response.text)
        print(f'Installing community package: {package_name}@{package_metadata["version"]}')

        # Download and extract the package
        package_zip_url = f'{GITHUB_API_URL}/{package_name}/zipball/{package_metadata["version"]}'
        package_dir = os.path.join(PYG_PACKAGES_DIR, f'{package_name}@{package_metadata["version"]}')
        os.makedirs(package_dir, exist_ok=True)

        download_and_extract_zip(package_zip_url, package_dir)

        # Move pyg.json to the root of the package directory
        package_json_path = os.path.join(package_dir, f'{package_name}@{package_metadata["version"]}', 'pyg.json')
        shutil.move(package_json_path, os.path.join(package_dir, 'pyg.json'))

        print(f'Community package {package_name} successfully installed.')
    else:
        print(f'Error fetching metadata for package "{package_name}"')
        sys.exit(1)

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
    elif command == 'install-community':
        if len(sys.argv) < 3:
            print('Usage: python pyg.py install-community package_name')
            sys.exit(1)
        package_name = sys.argv[2]
        install_community_package(package_name)
    else:
        print(f'Error: Unknown command "{command}"')
        sys.exit(1)

if __name__ == "__main__":
    main()
