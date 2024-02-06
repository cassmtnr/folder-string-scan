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

    found_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                lines = f.readlines()
                for line_num, line in enumerate(lines, start=1):
                    for target_string in target_strings:
                        if target_string in line:
                            found_files.append((filepath, line_num, line.strip(), target_string))
    return found_files

if __name__ == "__main__":
    directory_to_scan = './build/'
	# optionally can add strings to the array
    target_strings = []
    additional_strings = './.env'

    # Scan source code for target strings
    found_files = scan_source_code(directory_to_scan, target_strings=target_strings, additional_strings=additional_strings)

    if found_files:
        print("Found the following target strings in the source files:")
        for file, line_num, line_content, target_string in found_files:
            print(f"File: {file}, Line: {line_num}, Content: {line_content}, Target: {target_string}")
    else:
        print("No target strings were found in any files.")
