from .models import DecompoundingModel
import argparse
import urllib.request
import zipfile
import os

def download(model_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Extract the file name from the URL
    base_url = 'https://github.com/mhaugestad/noun-decomposition/tree/main/pretrained-models/'
    file_name = os.path.basename(base_url + model_name)

    # Download the tar.gz file
    urllib.request.urlretrieve(base_url, model_name)

    # Extract the contents of the tar.gz file
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(script_dir)

    # Remove the zip file
    os.remove(script_dir + file_name)

    print("Extraction complete!")
    return None

def main():
    parser = argparse.ArgumentParser(description="Command line tool")
    subparsers = parser.add_subparsers(dest="command")

    # Create a subparser for the "download" command
    download_parser = subparsers.add_parser("download", help="Download command")
    download_parser.add_argument("model", action="store_true", help="Specify model to download")

    args = parser.parse_args()

    # Call the appropriate function based on the provided command
    if args.command == "download":
        download()

if __name__ == "__main__":
    main()