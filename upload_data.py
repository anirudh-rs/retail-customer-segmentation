from huggingface_hub import HfApi
import os

api      = HfApi()
repo_id  = "anirudh-rs/retail-segmentation-data"
folder   = r"C:\Users\aniru\OneDrive\Desktop\Retail Seg\data\processed"

files = [
    "uci_clean.parquet",
    "hm_clean.parquet",
    "inst_clean.parquet",
    "rfm_uci_clustered.parquet",
    "rfm_hm_clustered.parquet",
    "rfm_inst_clustered.parquet",
]

for fname in files:
    path = os.path.join(folder, fname)
    print(f"Uploading {fname}...")
    api.upload_file(
        path_or_fileobj=path,
        path_in_repo=fname,
        repo_id=repo_id,
        repo_type="dataset",
    )
    print(f"Done: {fname}")

print("\nAll files uploaded.")