import os
import re
import argparse

def remove_comments(text):
    """
    Removes Verilog/SystemVerilog style comments from the provided text.
    """
    # Remove multi-line comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    # Remove single-line comments
    text = re.sub(r'//.*', '', text)
    return text

def optimize_file(file_path, flatten=True, keep_comments=False):
    """
    Optimizes a single RTL file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not keep_comments:
            content = remove_comments(content)
        
        lines = content.splitlines()
        cleaned_lines = []
        
        for line in lines:
            if line.strip():
                if flatten:
                    # Flatten: replace multiple spaces with single, and strip leading/trailing
                    line = re.sub(r'\s+', ' ', line).strip()
                else:
                    # No flatten: strip trailing, but keep relative leading indentation (normalized to spaces)
                    line = line.rstrip()
                    # Optional: Convert tabs to 4 spaces, then normalize inner spaces
                    line = line.replace('\t', '    ')
                
                cleaned_lines.append(line)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cleaned_lines) + '\n')
        
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="DV Skills Tool: Optimize RTL codebases for AI token efficiency.")
    parser.add_argument("--path", default=".", help="Target directory to process (default: current)")
    parser.add_argument("--no-flatten", action="store_true", help="Preserve indentation (do not flatten lines)")
    parser.add_argument("--keep-comments", action="store_true", help="Do not remove comments")
    parser.add_argument("--extensions", default=".sv,.v,.svh", help="Comma-separated list of extensions to keep")
    
    args = parser.parse_args()
    
    valid_extensions = set(args.extensions.split(','))
    
    print(f"--- Starting optimization in: {os.path.abspath(args.path)} ---")
    
    files_to_optimize = []
    
    for root, dirs, files in os.walk(args.path, topdown=False):
        # Skip git directory
        if '.git' in root.split(os.sep):
            continue
            
        for name in files:
            file_path = os.path.join(root, name)
            _, ext = os.path.splitext(name)
            
            if ext not in valid_extensions and name != 'cleanup_dv.py':
                try:
                    os.remove(file_path)
                    print(f"Deleted junk file: {file_path}")
                except Exception as e:
                    pass
            elif ext in valid_extensions:
                files_to_optimize.append(file_path)

    print(f"\n--- Optimizing {len(files_to_optimize)} RTL files ---")
    success_count = 0
    for file_path in files_to_optimize:
        if optimize_file(file_path, flatten=not args.no_flatten, keep_comments=args.keep_comments):
            print(f"Optimized: {file_path}")
            success_count += 1

    print(f"\nDone! {success_count} files processed. RTL logic is now token-optimized. 🪬")

    # Final touch: remove empty directories
    for root, dirs, files in os.walk(args.path, topdown=False):
        if not dirs and not files and '.git' not in root:
            try:
                os.rmdir(root)
                print(f"Removed empty directory: {root}")
            except:
                pass

if __name__ == "__main__":
    main()
