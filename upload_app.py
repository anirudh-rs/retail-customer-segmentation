from huggingface_hub import HfApi
import os

api     = HfApi()
repo_id = "anirudh-rs/retail-segmentation"
app_dir = r"C:\Users\aniru\OneDrive\Desktop\Retail Seg\app"

for root, dirs, files in os.walk(app_dir):
    dirs[:] = [d for d in dirs if d != "__pycache__"]
    for fname in files:
        if fname.endswith(".pyc"):
            continue
        local_path = os.path.join(root, fname)
        relative   = os.path.relpath(local_path, app_dir)
        repo_path  = relative.replace("\\", "/")
        print(f"Uploading {repo_path}...")
        api.upload_file(
            path_or_fileobj=local_path,
            path_in_repo=repo_path,
            repo_id=repo_id,
            repo_type="space",
        )

print("\nApp uploaded.")