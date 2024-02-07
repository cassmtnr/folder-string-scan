import os

def read_target_strings(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Target strings file '{file_path}' not found.")
        return []

def scan_source_code(directory, target_strings=None, additional_strings=None):
    if target_strings is None:
        target_strings = []

    if additional_strings:
        additional_target_strings = read_target_strings(additional_strings)
        # Concatenate the two lists and convert to a set to remove duplicates
        target_strings = list(set(target_strings + additional_target_strings))

    if not target_strings:
        print("No target strings provided.")
        return []

    found_lines = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                lines = f.readlines()
                for line_num, line in enumerate(lines, start=1):
                    for target_string in target_strings:
                        if target_string in line:
                            found_lines.append((filepath, line_num, line.strip(), target_string))
                            break  # Once a target string is found in a line, no need to check further
    return found_lines

if __name__ == "__main__":
    directory_to_scan = './build/'
    target_strings = []  # No need to specify any target strings here, as they will be read from additional_strings file
    additional_strings = './.env'

    found_lines = scan_source_code(directory_to_scan, target_strings=target_strings, additional_strings=additional_strings)

    if found_lines:
        print("Found the following target strings in the source files:")
        for file, line_num, line_content, target_string in found_lines:
            print(f"File: {file}, Line: {line_num}, Content: {line_content}")
    else:
        print("No target strings were found in any files.")
