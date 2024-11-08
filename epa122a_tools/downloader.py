import os
import sys
import zipfile
import requests
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib.metadata

name2link = {
    'lab-00': 'https://surfdrive.surf.nl/files/index.php/s/YiKmYp8ekFhLlIH',
    'lab-01': 'https://surfdrive.surf.nl/files/index.php/s/qwy7IacNP6nHtgt',
    'lab-02': 'https://surfdrive.surf.nl/files/index.php/s/1hEN47ncLbR0B3W',
    'lab-03': 'https://surfdrive.surf.nl/files/index.php/s/XynFJCP7u1ksuUe',
    'lab-04': 'https://surfdrive.surf.nl/files/index.php/s/lqGbKXWDSIWUdTT',
    'lab-05': 'https://surfdrive.surf.nl/files/index.php/s/Fl21mSCbXJo3Axk',
    'lab-06': 'https://surfdrive.surf.nl/files/index.php/s/NzNuekCD932ExLA',
    'lab-07': 'https://surfdrive.surf.nl/files/index.php/s/DdvWjI9umIx8iPM',
}

def fetch(data_name: str, force: bool = False):
    package_name = 'epa122a_tools'
    version = importlib.metadata.version(package_name)
    print(f"Using {package_name} version: {version}")

    # Define the download URL based on the dataset name
    try:
        url = name2link[data_name] + '/download'
    except:
        print(f'{data_name} not supported')
        sys.exit(1)

    # Set the target folder where data will be extracted
    current_dir = Path.cwd()
    data_dir = current_dir / "data"

    # Check if the data folder already exists
    if data_dir.exists() and data_dir.is_dir():
        if not force:
            print(f"The folder '{data_dir}' already exists. Use force=True to redownload and extract.")
            return
        else:
            print(
                f"The folder '{data_dir}' already exists. Force download enabled, proceeding with redownload and extraction.")
    else:
        print(f"The folder '{data_dir}' does not exist. Proceeding with download and extraction.")

    # Create the 'data' directory if it doesn't exist
    current_dir.mkdir(parents=True, exist_ok=True)

    # Create a temporary directory to download the zip file
    with TemporaryDirectory() as tmpdirname:
        zip_path = os.path.join(tmpdirname, f"{data_name}.zip")

        # Download the zip file
        print(f"Downloading {data_name}.zip from {url}...")
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Save the zip file to the temporary directory
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        print(f"{data_name}.zip successfully downloaded to {zip_path}.")

        # Unzip the file to the data directory
        print(f"Extracting {data_name}.zip to {current_dir}...")
        count_files = 0
        count_dirs = 0
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for member in zip_ref.infolist():
                extracted_path = Path(current_dir) / member.filename

                if extracted_path.exists():
                    print(f"Overwriting existing file or directory: {extracted_path}")

                if member.is_dir():
                    # print(f"Extracting directory: {extracted_path}")
                    extracted_path.mkdir(parents=True, exist_ok=True)
                    count_dirs += 1
                else:
                    # print(f"Extracting file     : {extracted_path}")
                    count_files += 1
                    extracted_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(extracted_path, 'wb') as f:
                        f.write(zip_ref.read(member))
        # with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        #     zip_ref.extractall(current_dir)
        print(f"Extracted {count_files} files and {count_dirs} directories.")
        print(f"{data_name}.zip successfully extracted to {current_dir}.")

    print(f"Download and extraction of {data_name} completed.")

# Example usage:
# fetch("sample_data", force=True)

if __name__ == "__main__":
    fetch(sys.argv[1], force=True)
