import os
import ast

def find_imported_modules(directory):
    imported_modules = set()

    # Walk through all files in the given directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)

                # Parse each Python file to extract imports
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        tree = ast.parse(f.read(), filename=file)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imported_modules.add(alias.name.split('.')[0])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    imported_modules.add(node.module.split('.')[0])
                    except SyntaxError as e:
                        print(f"Skipping {file_path} due to SyntaxError: {e}")

    return imported_modules

# Set your project's source directory
source_directory = '.'  # Change to your project's directory if needed
imported_modules = find_imported_modules(source_directory)

# Write the list to requirements_imports.txt
with open('../requirements_imports.txt', 'w') as req_file:
    for module in sorted(imported_modules):
        req_file.write(module + '\n')

print("The imported modules have been saved to requirements_imports.txt.")