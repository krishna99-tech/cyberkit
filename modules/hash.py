#import hashlib
#text = "Hello, World!"
#hash_object = hashlib.sha256(text.encode())
#hash_digest = hash_object.hexdigest()
#print(f"SHA-256 hash of '{text}': {hash_digest}")

import hashlib


def hash_file(file_path):
    h = hashlib.new("sha256")
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(1024)
            if chunk == b"":
                break
            h.update(chunk)
    return h.hexdigest()
def verify_integrity(file1,file2):
    hash1 = hash_file(file1)
    hash2 = hash_file(file2)
    result_str = f"Hash of file 1: {hash1}\nHash of file 2: {hash2}\n\n"
    if hash1 == hash2:
        result_str += "Files are identical."
    else:
        result_str += "Files are different."
    return result_str
       
                            

if __name__ == "__main__":
    print(hash_file(r"C:\Users\vakav\Documents\learnpy\cyberkit\samplefiles\sample.txt"))
    print(verify_integrity(r"C:\Users\vakav\Documents\learnpy\cyberkit\samplefiles\sample.txt", r"C:\Users\vakav\Documents\learnpy\cyberkit\samplefiles\sample_copy.txt"))