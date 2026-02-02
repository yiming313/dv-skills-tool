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
    Returns (success, original_size, optimized_size)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        orig_size = len(content)
        
        if not keep_comments:
            content = remove_comments(content)
        
        lines = content.splitlines()
        cleaned_lines = []
        
        for line in lines:
            if line.strip():
                if flatten:
                    line = re.sub(r'\s+', ' ', line).strip()
                else:
                    line = line.rstrip()
                    line = line.replace('\t', '    ')
                cleaned_lines.append(line)
        
        final_content = '\n'.join(cleaned_lines) + '\n'
        opt_size = len(final_content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        return True, orig_size, opt_size
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, 0, 0

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
    total_orig = 0
    total_opt = 0
    success_count = 0
    
    for file_path in files_to_optimize:
        success, orig, opt = optimize_file(file_path, flatten=not args.no_flatten, keep_comments=args.keep_comments)
        if success:
            total_orig += orig
            total_opt += opt
            reduction = (1 - opt/orig) * 100 if orig > 0 else 0
            print(f"Optimized: {file_path} ({reduction:.1f}% reduction)")
            success_count += 1

    print(f"\nDone! {success_count} files processed.")
    if total_orig > 0:
        saved_chars = total_orig - total_opt
        # Heuristic: 1 token approx 4 characters
        est_tokens_saved = saved_chars // 4
        print(f"Summary: Reduced code size from {total_orig} to {total_opt} chars.")
        print(f"Estimated Token Savings: ~{est_tokens_saved} tokens ({(1 - total_opt/total_orig)*100:.1f}% smaller). 🪬")

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
