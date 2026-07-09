import os
import zipfile
import kaggle

dataset_name='shashwatwork/dataco-smart-supply-chain-for-big-data-analysis'
download_path='data/raw'
os.makedirs(download_path, exist_ok=True)
kaggle.api.dataset_download_files(dataset_name,path=download_path, unzip=True)
old_file='data/raw/DataCoSupplyChainDataset.csv'
new_file='data/raw/dataco.csv'
os.rename(old_file, new_file)