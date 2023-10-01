import argparse
import os
import re

# convert $...$ to \( ... \)
def single_dollar_to_parentheses(latex_string):
    return re.sub(r'\$(.*?)\$', r'\\(\1\\)', latex_string)

# convert \( ... \) to $...$
def parentheses_to_single_dollar(latex_string):
    return re.sub(r'\\(.*?\\)', r'$\1$', latex_string)

# convert $$...$$ to \[ ... \]
def double_dollar_to_braces(latex_string):
    return re.sub(r'\$\$(.*?)\$\$', r'\\[\1\\]', latex_string)

# convert \[ ... \] to $$...$$
def braces_to_double_dollar(latex_string):
    return re.sub(r'\\[\s\S]*?\\]', r'$$\1$$', latex_string)

# Function to process a single file
def process_file(input_file, mode):
    with open(input_file, 'r') as file:
        latex_content = file.read()
    
    if mode == 'dedollarify':
        converted_latex = single_dollar_to_parentheses(latex_content)
        converted_latex = double_dollar_to_braces(converted_latex)
    elif mode == '':
        converted_latex = parentheses_to_single_dollar(latex_content)
        converted_latex = braces_to_double_dollar(converted_latex)
    else:
        raise ValueError("Invalid mode. Use 'dedollarify' or 'dollarify'.")
    
    with open(input_file, 'w') as file:
        file.write(converted_latex)

# Function to process all files in a directory
def process_directory(directory, mode):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".tex"):
                filepath = os.path.join(root, filename)
                process_file(filepath, mode)

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Convert LaTeX equations between formats.")
parser.add_argument("mode", choices=["dedollarify", "dollarify"], help="Conversion mode (dedollarify &  dollarify LaTeX format)")
parser.add_argument("path", help="File or directory path to process")

args = parser.parse_args()

if os.path.isfile(args.path):
    process_file(args.path, args.mode)
elif os.path.isdir(args.path):
    process_directory(args.path, args.mode)
else:
    print(f"Invalid path: {args.path}")

