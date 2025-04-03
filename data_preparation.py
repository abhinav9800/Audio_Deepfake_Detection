import os
import argparse
import random
import glob
import shutil
import numpy as np
from tqdm import tqdm

def create_directory_structure(output_dir):
    """Create the required directory structure for the FSD model."""
    # Create main directories
    os.makedirs(output_dir, exist_ok=True)
    
    # Create subdirectories for protocols
    protocols_dir = os.path.join(output_dir, "protocols")
    os.makedirs(protocols_dir, exist_ok=True)
    
    # Create directories for train, dev, and eval data
    for split in ["train", "dev", "eval"]:
        for label in ["natural", "spoof"]:
            os.makedirs(os.path.join(output_dir, split, label), exist_ok=True)
    
    return protocols_dir

def scan_audio_files(natural_dir, spoof_dir):
    """Scan directories to find all audio files."""
    natural_files = []
    spoof_files = []
    
    # Find all audio files in natural directory
    for root, _, files in os.walk(natural_dir):
        for file in files:
            if file.endswith(('.wav', '.flac', '.mp3')):
                natural_files.append(os.path.join(root, file))
    
    # Find all audio files in spoof directory
    for root, _, files in os.walk(spoof_dir):
        for file in files:
            if file.endswith(('.wav', '.flac', '.mp3')):
                spoof_files.append(os.path.join(root, file))
    
    return natural_files, spoof_files

def split_data(files, train_ratio=0.7, dev_ratio=0.15, eval_ratio=0.15, seed=42):
    """Split files into train, dev, and eval sets."""
    random.seed(seed)
    random.shuffle(files)
    
    total_files = len(files)
    train_end = int(total_files * train_ratio)
    dev_end = train_end + int(total_files * dev_ratio)
    
    train_files = files[:train_end]
    dev_files = files[train_end:dev_end]
    eval_files = files[dev_end:]
    
    return train_files, dev_files, eval_files

def organize_files(files, output_dir, split_name, label_name):
    """Copy files to the organized directory structure."""
    organized_files = []
    
    for src_file in tqdm(files, desc=f"Organizing {split_name} {label_name} files"):
        # Create a destination filename
        filename = os.path.basename(src_file)
        rel_path = os.path.join(split_name, label_name, filename)
        dst_file = os.path.join(output_dir, rel_path)
        
        # Make sure subdirectories exist
        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
        
        # Copy the file
        shutil.copy2(src_file, dst_file)
        organized_files.append(rel_path)
    
    return organized_files

def create_protocol_files(train_natural, train_spoof, dev_natural, dev_spoof, 
                         eval_natural, eval_spoof, protocols_dir):
    """Create protocol files for training, development, and evaluation."""
    # Training protocol
    with open(os.path.join(protocols_dir, "train.txt"), "w") as f:
        for file_path in train_natural:
            f.write(f"{file_path} bonafide\n")
        for file_path in train_spoof:
            f.write(f"{file_path} spoof\n")
    
    # Development protocol
    with open(os.path.join(protocols_dir, "dev.txt"), "w") as f:
        for file_path in dev_natural:
            f.write(f"{file_path} bonafide\n")
        for file_path in dev_spoof:
            f.write(f"{file_path} spoof\n")
    
    # Evaluation protocol
    with open(os.path.join(protocols_dir, "eval.txt"), "w") as f:
        for file_path in eval_natural:
            f.write(f"{file_path} bonafide\n")
        for file_path in eval_spoof:
            f.write(f"{file_path} spoof\n")
    
    # Create an empty eval_asv_scores.txt file for compatibility
    # This is just to maintain the expected file structure without adding dummy scores
    with open(os.path.join(protocols_dir, "eval_asv_scores.txt"), "w") as f:
        f.write("# Empty ASV scores file - not used in this implementation\n")

def main():
    parser = argparse.ArgumentParser(description="Organize audio files for FSD model.")
    parser.add_argument("--natural_dir", required=True, help="Directory containing natural audio files")
    parser.add_argument("--spoof_dir", required=True, help="Directory containing spoofed audio files")
    parser.add_argument("--output_dir", required=True, help="Output directory for organized files")
    parser.add_argument("--train_ratio", type=float, default=0.7, help="Ratio of files for training")
    parser.add_argument("--dev_ratio", type=float, default=0.15, help="Ratio of files for development")
    parser.add_argument("--eval_ratio", type=float, default=0.15, help="Ratio of files for evaluation")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    args = parser.parse_args()
    
    # Validate ratios
    total_ratio = args.train_ratio + args.dev_ratio + args.eval_ratio
    if not 0.99 <= total_ratio <= 1.01:
        raise ValueError(f"The sum of ratios should be 1.0, got {total_ratio}")
    
    # Create directory structure
    protocols_dir = create_directory_structure(args.output_dir)
    
    # Scan audio files
    print("Scanning for audio files...")
    natural_files, spoof_files = scan_audio_files(args.natural_dir, args.spoof_dir)
    print(f"Found {len(natural_files)} natural files and {len(spoof_files)} spoof files")
    
    # Split data
    print("Splitting data into train, dev, and eval sets...")
    train_natural, dev_natural, eval_natural = split_data(natural_files, 
                                                         args.train_ratio, 
                                                         args.dev_ratio, 
                                                         args.eval_ratio, 
                                                         args.seed)
    
    train_spoof, dev_spoof, eval_spoof = split_data(spoof_files, 
                                                   args.train_ratio, 
                                                   args.dev_ratio, 
                                                   args.eval_ratio, 
                                                   args.seed)
    
    # Organize files
    print("Organizing files...")
    train_natural_rel = organize_files(train_natural, args.output_dir, "train", "natural")
    train_spoof_rel = organize_files(train_spoof, args.output_dir, "train", "spoof")
    
    dev_natural_rel = organize_files(dev_natural, args.output_dir, "dev", "natural")
    dev_spoof_rel = organize_files(dev_spoof, args.output_dir, "dev", "spoof")
    
    eval_natural_rel = organize_files(eval_natural, args.output_dir, "eval", "natural")
    eval_spoof_rel = organize_files(eval_spoof, args.output_dir, "eval", "spoof")
    
    # Create protocol files
    print("Creating protocol files...")
    create_protocol_files(train_natural_rel, train_spoof_rel,
                         dev_natural_rel, dev_spoof_rel,
                         eval_natural_rel, eval_spoof_rel,
                         protocols_dir)
    
    print(f"Data organization complete. Organized data is in {args.output_dir}")
    print(f"Protocol files are in {protocols_dir}")
    print(f"Directory structure created for the FSD model.")
    
    # Print example command to run the FSD model
    print("\nExample command to run the FSD model:")
    print(f"python fsd_model.py --base_dir {args.output_dir}")

if __name__ == "__main__":
    main()