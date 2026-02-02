import os

def cleanup_dv_files():
    """
    1. Deletes all files in current directory and subdirectories EXCEPT for those with 
       extensions: .sv, .v, .svh
    2. Removes all blank lines from the remaining files.
    """
    valid_extensions = {'.sv', '.v', '.svh'}
    
    # Track paths to process contents after cleanup
    remaining_files = []

    print("--- Starting cleanup process ---")
    
    for root, dirs, files in os.walk('.', topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            _, ext = os.path.splitext(name)
            
            if ext not in valid_extensions:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
            else:
                remaining_files.append(file_path)

    print("\n--- Cleaning up blank lines in remaining files ---")
    
    for file_path in remaining_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Remove blank lines (strip whitespace and check if empty)
            cleaned_lines = [line for line in lines if line.strip()]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(cleaned_lines)
            print(f"Processed: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print("\nDone! Your DV workspace is clean.")

if __name__ == "__main__":
    cleanup_dv_files()
