import os
import gdown
import zipfile
import shutil
from pathlib import Path

DATASET_FOLDER = "DATASET"
TEMP_FOLDER = "temp_download"

DATASET_CONFIG = {
    'filename': 'DATASET.zip',  
    'file_id': '1F99QfUPzWKrR8JK-JBD4cKANcLoPf_ip',  
    'extract_to': DATASET_FOLDER  
}

def create_directories():
    """Create necessary directories."""
    os.makedirs(DATASET_FOLDER, exist_ok=True)
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    print(f"✅ Created directories: {DATASET_FOLDER}, {TEMP_FOLDER}")

def is_dataset_already_downloaded():
    """Check if dataset is already downloaded by looking for files in DATASET folder."""
    expected_path = os.path.join(DATASET_FOLDER, DATASET_FOLDER)
    if not os.path.exists(expected_path):
        return False
    
    dataset_contents = os.listdir(DATASET_FOLDER)
    if len(dataset_contents) == 0:
        return False
    
    return True

def download_dataset():
    """Download the dataset zip file from Google Drive."""
    temp_zip_path = os.path.join(TEMP_FOLDER, DATASET_CONFIG['filename'])
    
    print(f"🔽 Downloading dataset: {DATASET_CONFIG['filename']}...")
    
    try:
        url = f"https://drive.google.com/uc?id={DATASET_CONFIG['file_id']}"
        result = gdown.download(url, temp_zip_path, quiet=False)
        
        if not result:
            print(f"❌ Failed to download dataset (Check Google Drive ID: {DATASET_CONFIG['file_id']})")
            return None
        
        if not os.path.exists(temp_zip_path):
            print(f"❌ Download failed - file not found: {temp_zip_path}")
            return None
            
        print(f"✅ Dataset downloaded successfully: {temp_zip_path}")
        return temp_zip_path
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return None

def extract_dataset(zip_path):
    """Extract the dataset zip file."""
    print(f"📦 Extracting dataset to {DATASET_FOLDER}...")
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            print(f"📁 Found {len(file_list)} files in the zip")
            
            zip_ref.extractall(DATASET_FOLDER)
            
        print(f"✅ Dataset extracted successfully to {DATASET_FOLDER}")
        
        extracted_items = os.listdir(DATASET_FOLDER)
        print(f"📂 Extracted contents: {extracted_items}")
        
        return True
        
    except zipfile.BadZipFile:
        print(f"❌ Error: Downloaded file is not a valid zip file")
        return False
    except Exception as e:
        print(f"❌ Error extracting dataset: {e}")
        return False

def cleanup_temp_files():
    """Clean up temporary download files."""
    if os.path.exists(TEMP_FOLDER):
        try:
            shutil.rmtree(TEMP_FOLDER)
            print(f"🧹 Cleaned up temporary files: {TEMP_FOLDER}")
        except Exception as e:
            print(f"⚠️ Warning: Could not clean up temp folder: {e}")

def main():
    print("🚀 Starting dataset download process...")
    
    create_directories()
    
    if is_dataset_already_downloaded():
        print(f"✅ Dataset already exists in {DATASET_FOLDER}, skipping download.")
        return
    
    zip_path = download_dataset()
    if not zip_path:
        print("❌ Dataset download failed. Exiting.")
        return
    
    if extract_dataset(zip_path):
        print("✅ Dataset setup completed successfully!")
    else:
        print("❌ Dataset extraction failed.")
        return
    
    cleanup_temp_files()
    
    print("🎉 Dataset download and setup process completed!")

if __name__ == "__main__":
    main()