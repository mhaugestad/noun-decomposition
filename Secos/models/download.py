from .models import DecompoundingModel
import requests, shutil, zipfile, os, pickle
from tqdm import tqdm

def download(model_name):
    script_dir = os.path.dirname(os.path.abspath(__file__)) + '/data/'

    # Extract the file name from the URL
    base_url = 'https://secos-model-data.s3.eu-west-2.amazonaws.com/'
    
    # Download the zip file
    response = requests.get(base_url + model_name + '.json', stream=True)
    total_size = int(response.headers.get("Content-Length", 0))
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True)
    with open(script_dir + model_name + '.json', "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                # Write the chunk to the file
                file.write(chunk)
                # Update the progress bar with the chunk size
                progress_bar.update(len(chunk))

    # Close the progress bar
    progress_bar.close()

    print("Download completed!")