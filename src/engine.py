import hashlib
import os

class Engine:
    def __init__(self, malware_hashes_file="malware_hashes.txt"):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(self.current_dir, malware_hashes_file)
        
        malware_hashes = open(full_path, "r").readlines()
        

    def sha256_hash(self, filename):
        try:
            with open(filename, "rb") as f:
                bytes = f.read()
                hash_value = hashlib.sha256(bytes).hexdigest()
                f.close()
            return hash_value
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            return None
        
    def malware_identification(self, filename):
        hash_of_file = self.sha256_hash(filename)
        if hash_of_file in self.malware_hashes:
            print(f"Malware detected: {filename}")
        else:
            print(f"No malware detected: {filename}")
    
        
    def folder_scan(self, folder_path):
        dir_list = list()
        full_path = os.path.join(self.current_dir, folder_path)
        for dirpath, dirnames, filenames in os.walk(full_path):
            for file in filenames:
                dir_list.append(os.path.join(dirpath, file))
        
        
