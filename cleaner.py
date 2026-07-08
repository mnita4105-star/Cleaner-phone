import os
import hashlib

# TARGET FOLDER: Only point this at a folder you want to clean
# DO NOT set this to / or /sdcard/ directly!
folder_path = "/sdcard/Download" 

def get_file_hash(file_path):
    """Generates an MD5 hash to identify identical content."""
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None

def remove_duplicates(directory):
    hashes = {} 
    deleted_count = 0
    
    print(f"--- Starting Cleanup in: {directory} ---")
    
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        
        # Only process files, ignore folders
        if os.path.isfile(path):
            file_hash = get_file_hash(path)
            
            if file_hash in hashes:
                print(f"Found duplicate: {filename}")
                try:
                    os.remove(path)
                    print(f"  Successfully deleted: {path}")
                    deleted_count += 1
                except Exception as e:
                    print(f"  Error deleting {filename}: {e}")
            else:
                hashes[file_hash] = path
    
    print(f"--- Cleanup complete. {deleted_count} duplicates removed. ---")

if __name__ == "__main__":
    # Safety check: confirm the path exists before running
    if os.path.exists(folder_path):
        remove_duplicates(folder_path)
    else:
        print(f"Error: The path {folder_path} does not exist.")
