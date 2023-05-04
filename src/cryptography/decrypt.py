import sys
import pyAesCrypt

def decrypt_file(file_path, password, buffer_size=64 * 1024):
    output_path = file_path[:-4] if file_path.endswith(".aes") else file_path + ".dec"
    pyAesCrypt.decryptFile(file_path, output_path, password, buffer_size)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python decrypt.py <file_path> <password>")
        sys.exit(1)

    file_path, password = sys.argv[1], sys.argv[2]

    decrypt_file(file_path, password)