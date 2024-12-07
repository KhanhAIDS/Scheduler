import os
import platform
import requests
import zipfile

def get_system_details():
    system = platform.system().lower()
    arch = platform.machine().lower()

    if system == "windows":
        os_type = "win64" if arch == "amd64" else "win32"
    elif system == "darwin":
        os_type = "mac-arm64" if "arm" in arch else "mac-x64"
    elif system == "linux":
        os_type = "linux64"
    else:
        raise ValueError(f"Unsupported OS: {system}")

    return system, os_type

def download_file(url, dest_folder):
    file_name = url.split("/")[-1]
    file_path = os.path.join(dest_folder, file_name)

    print(f"Downloading {file_name}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Downloaded: {file_path}")
    else:
        raise Exception(f"Failed to download {url}: {response.status_code}")

    return file_path

def extract_zip(file_path, extract_to):
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted: {file_path} to {extract_to}")

def setup_chrome_and_chromedriver():
    base_url = "https://storage.googleapis.com/chrome-for-testing-public"
    chrome_version = "131.0.6778.85"  # Replace with the desired version or fetch dynamically.

    _, os_type = get_system_details()

    dest_folder = os.path.join(os.getcwd(), "selenium_binaries")
    os.makedirs(dest_folder, exist_ok=True)

    chrome_url = f"{base_url}/{chrome_version}/{os_type}/chrome-{os_type}.zip"
    chromedriver_url = f"{base_url}/{chrome_version}/{os_type}/chromedriver-{os_type}.zip"

    chrome_zip_path = download_file(chrome_url, dest_folder)
    extract_zip(chrome_zip_path, dest_folder)

    chromedriver_zip_path = download_file(chromedriver_url, dest_folder)
    extract_zip(chromedriver_zip_path, dest_folder)

    os.remove(chrome_zip_path)
    os.remove(chromedriver_zip_path)

    print(f"Setup completed. Binaries are in: {dest_folder}")
    return dest_folder

if __name__ == "__main__":
    setup_dir = setup_chrome_and_chromedriver()
    print(f"Binaries ready in: {setup_dir}")