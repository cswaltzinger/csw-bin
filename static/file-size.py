#!/Users/csw/.config/anaconda3/bin/python


import os
from sys import argv as args 
args = args[1:] 

maxLen = max([len(arg) for arg in args])


def get_file_size(file_path):
    try:
        file_size_bytes = os.path.getsize(file_path)
        file_size_kb = file_size_bytes / 1024
        file_size_mb = file_size_kb / 1024
        file_size_gb = file_size_mb / 1024
        return file_size_bytes, file_size_kb, file_size_mb, file_size_gb
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")

for file in args:
    b, kb, mb, gb = get_file_size(file)
    while len(file) < maxLen:
        file += " "
    if b == None:
        continue
    # print(f"{file}: {b:>10} bytes | {kb:>10.2f} KB | {mb:>10.2f} MB | {gb:>10.2f} GB")

    print(f"{file}: {kb:>10.2f} KB | {mb:>10.2f} MB | {gb:>10.2f} GB")

