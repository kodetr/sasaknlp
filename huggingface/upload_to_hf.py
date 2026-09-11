"""Helper script to upload SasakNLP to Hugging Face Spaces & Datasets.

Usage:
    python3 huggingface/upload_to_hf.py --type space --repo-id <username>/sasaknlp-demo
    python3 huggingface/upload_to_hf.py --type dataset --repo-id <username>/sasak-benchmark-100k
"""

import argparse
import os
import sys
from huggingface_hub import HfApi, create_repo

def upload_space(repo_id: str, token: str = None):
    print(f"🚀 Creating and uploading Hugging Face Space: {repo_id}...")
    api = HfApi(token=token)
    
    try:
        create_repo(
            repo_id=repo_id,
            repo_type="space",
            space_sdk="static",
            exist_ok=True,
            token=token
        )
    except Exception as e:
        print(f"Catatan: create_repo dilewati atau repo sudah ada ({e}). Melanjutkan upload file...")
    
    # Upload files
    space_dir = os.path.join(os.path.dirname(__file__), "space")
    api.upload_folder(
        folder_path=space_dir,
        repo_id=repo_id,
        repo_type="space",
        token=token
    )
    print(f"✅ Berhasil! Space Anda live di: https://huggingface.co/spaces/{repo_id}")

def upload_dataset(repo_id: str, token: str = None):
    print(f"🚀 Creating and uploading Hugging Face Dataset: {repo_id}...")
    api = HfApi(token=token)
    
    # Create dataset repo if not exists
    create_repo(
        repo_id=repo_id,
        repo_type="dataset",
        exist_ok=True,
        token=token
    )
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Upload README Dataset Card
    api.upload_file(
        path_or_fileobj=os.path.join(os.path.dirname(__file__), "dataset", "README.md"),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="dataset",
        token=token
    )
    
    # Upload benchmark 100k (parquet & csv)
    b100k_p = os.path.join(base_dir, "datasets", "benchmark", "benchmark_100k.parquet")
    if os.path.exists(b100k_p):
        print("Uploading benchmark_100k.parquet...")
        api.upload_file(
            path_or_fileobj=b100k_p,
            path_in_repo="benchmark_100k.parquet",
            repo_id=repo_id,
            repo_type="dataset",
            token=token
        )
    b100k = os.path.join(base_dir, "datasets", "benchmark", "benchmark_100k.csv")
    if os.path.exists(b100k):
        print("Uploading benchmark_100k.csv...")
        api.upload_file(
            path_or_fileobj=b100k,
            path_in_repo="benchmark_100k.csv",
            repo_id=repo_id,
            repo_type="dataset",
            token=token
        )
        
    # Upload sentences (parquet & csv)
    corpus_p = os.path.join(base_dir, "datasets", "corpus", "sasak_sentences_large.parquet")
    if os.path.exists(corpus_p):
        print("Uploading sasak_sentences_large.parquet...")
        api.upload_file(
            path_or_fileobj=corpus_p,
            path_in_repo="sasak_sentences_large.parquet",
            repo_id=repo_id,
            repo_type="dataset",
            token=token
        )
    corpus = os.path.join(base_dir, "datasets", "corpus", "sasak_sentences_large.csv")
    if os.path.exists(corpus):
        print("Uploading sasak_sentences_large.csv...")
        api.upload_file(
            path_or_fileobj=corpus,
            path_in_repo="sasak_sentences_large.csv",
            repo_id=repo_id,
            repo_type="dataset",
            token=token
        )
        
    # Upload kamus (parquet & csv)
    kamus_p = os.path.join(base_dir, "datasets", "sasaklex", "kamus_balai_bahasa_ntb.parquet")
    if os.path.exists(kamus_p):
        print("Uploading kamus_balai_bahasa_ntb.parquet...")
        api.upload_file(
            path_or_fileobj=kamus_p,
            path_in_repo="kamus_balai_bahasa_ntb.parquet",
            repo_id=repo_id,
            repo_type="dataset",
            token=token
        )
    kamus = os.path.join(base_dir, "datasets", "sasaklex", "kamus_balai_bahasa_ntb.csv")
    if os.path.exists(kamus):
        print("Uploading kamus_balai_bahasa_ntb.csv...")
        api.upload_file(
            path_or_fileobj=kamus,
            path_in_repo="kamus_balai_bahasa_ntb.csv",
            repo_id=repo_id,
            repo_type="dataset",
            token=token
        )
        
    print(f"✅ Berhasil! Dataset Anda live di: https://huggingface.co/datasets/{repo_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload to Hugging Face")
    parser.add_argument("--type", choices=["space", "dataset"], required=True, help="Type of upload: 'space' or 'dataset'")
    parser.add_argument("--repo-id", required=True, help="HF Repo ID, e.g., 'kodetr/sasaknlp-demo'")
    parser.add_argument("--token", default=None, help="Optional Hugging Face write token")
    
    args = parser.parse_args()
    
    token = args.token or os.getenv("HF_TOKEN")
    
    if args.type == "space":
        upload_space(args.repo_id, token)
    else:
        upload_dataset(args.repo_id, token)
