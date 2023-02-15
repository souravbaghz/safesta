import argparse
import os
import re
from termcolor import colored
#banner
print("")
print("  ─────█─▄▀█──█▀▄─█─────\n  ────▐▌──────────▐▌────\n  ────█▌▀▄──▄▄──▄▀▐█────\n  ───▐██──▀▀──▀▀──██▌───\n  ──▄████▄──▐▌──▄████▄──")
print("")
print(" █▀ ▄▀█ █▀▀ █▀▀ █▀ ▀█▀ ▄▀█")
print(" ▄█ █▀█ █▀░ ██▄ ▄█ ░█░ █▀█")
print("  github.com/souravbaghz  ")
print("")
# Parse command-line arguments
parser = argparse.ArgumentParser(description='Scan code files for dangerous function calls')
parser.add_argument('directory', help='the directory to scan')
args = parser.parse_args()

# Define the configuration file paths and load the function names for each programming language
dangerous_functions = {
    'python': [],
    'c': [],
    'c++': [],
    'c#': []
}
with open('src/dangerous_functions_python.txt', 'r') as f:
    dangerous_functions['python'] = [line.strip() for line in f.readlines()]
with open('src/dangerous_functions_c.txt', 'r') as f:
    dangerous_functions['c'] = [line.strip() for line in f.readlines()]
with open('src/dangerous_functions_c++.txt', 'r') as f:
    dangerous_functions['c++'] = [line.strip() for line in f.readlines()]
with open('src/dangerous_functions_c#.txt', 'r') as f:
    dangerous_functions['c#'] = [line.strip() for line in f.readlines()]

# Define the file extensions to search for each programming language
file_extensions = {
    'python': ['.py'],
    'c': ['.c'],
    'c++': ['.cpp', '.cxx', '.cc'],
    'c#': ['.cs']
}

# Loop through each programming language
for lang, functions in dangerous_functions.items():
    print(colored(f'[INF] Searching for dangerous functions in {lang} code...', 'magenta'))
   # print("------------------------------------------------------------------")

    # Loop through each file extension for the programming language
    for file_ext in file_extensions[lang]:
        # Loop through each file in the directory with a matching extension
        for filename in [f for f in os.listdir(args.directory) if os.path.splitext(f)[-1] == file_ext]:
            file_path = os.path.join(args.directory, filename)

            # Open the file and read its contents
            with open(file_path, 'r') as f:
                file_contents = f.read()

            # Loop through each dangerous function in the list and search for its presence
            for function_name in functions:
                pattern = re.compile(f'{function_name}\\(')
                matches = list(pattern.finditer(file_contents))

                # If the function is found, print a message with the filename, line number, programming language, and function name
                if len(matches) > 0:
                    line_numbers = [file_contents[:m.start()].count('\n') + 1 for m in matches]
                    print(colored(f'[-] Potentially dangerous function {function_name} found in {filename} ({lang}) on lines: {", ".join(str(n) for n in line_numbers)}', 'red'))
