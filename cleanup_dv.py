import os
import re

def remove_comments(text):
    """
    Removes Verilog/SystemVerilog style comments from the provided text.
    - // Single line comments
    - /* Multi-line 
         comments */
    """
    # Remove multi-line comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    # Remove single-line comments
    text = re.sub(r'//.*', '', text)
    return text

def cleanup_dv_files():
    """
    1. Deletes non-DV files (.sv, .v, .svh are kept).
    2. Removes all comments (// and /* */).
    3. Removes all blank lines.
    4. Strips trailing whitespace.
    """
    valid_extensions = {'.sv', '.v', '.svh'}
    remaining_files = []

    print("--- Phase 1: File Cleanup ---")
    for root, dirs, files in os.walk('.', topdown=False):
        # Avoid cleaning up the .git directory
        if '.git' in root.split(os.sep):
            continue
            
        for name in files:
            file_path = os.path.join(root, name)
            _, ext = os.path.splitext(name)
            
            if ext not in valid_extensions and name != 'cleanup_dv.py':
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
            elif ext in valid_extensions:
                remaining_files.append(file_path)

    print("\n--- Phase 2: Logic Pruning (Comments & Blank Lines) ---")
    for file_path in remaining_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Step A: Remove comments
            content = remove_comments(content)
            
            # Step B: Process lines (remove blank lines and strip trailing spaces)
            lines = content.splitlines()
            cleaned_lines = []
            for line in lines:
                if line.strip():
                    # Replace multiple spaces with a single space
                    line = re.sub(r'\s+', ' ', line).strip()
                    cleaned_lines.append(line)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(cleaned_lines) + '\n')
            
            print(f"Optimized: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print("\nIteration complete. RTL logic preserved, noise removed.")

if __name__ == "__main__":
    cleanup_dv_files()
