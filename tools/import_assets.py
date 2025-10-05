import zipfile, sys, os
def main(zip_path):
    if not zipfile.is_zipfile(zip_path):
        print("Not a zip file:", zip_path); return
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall("assets")
    print("Extracted into ./assets")
if __name__ == "__main__":
    main(sys.argv[1])
