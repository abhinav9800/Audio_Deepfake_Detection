# Fake Speech Detection (FSD) Model

This repository contains two main scripts for preparing data and training a Self-Distillation Fake Speech Detection (FSD) model to distinguish between natural and spoofed audio samples.

## Prerequisites

- Python 3.6+
- PyTorch
- Librosa
- NumPy
- Pandas
- tqdm
- Matplotlib
- scikit-learn
- SciPy

You can install all required packages with:s

```bash
pip install torch numpy pandas librosa tqdm matplotlib scikit-learn scipy
```

## Data Organization Script

The first script (`directory.py`) organizes your audio files into the required directory structure for training the FSD model.

### Usage:

```bash
python directory.py --natural_dir /path/to/natural/audio \
                    --spoof_dir /path/to/spoofed/audio \
                    --output_dir /path/to/organized/output \
                    --train_ratio 0.7 \
                    --dev_ratio 0.15 \
                    --eval_ratio 0.15 \
                    --seed 42
```

### Arguments:

- `--natural_dir`: Directory containing natural (bonafide) audio files
- `--spoof_dir`: Directory containing spoofed audio files
- `--output_dir`: Output directory for organized files
- `--train_ratio`: Ratio of files for training (default: 0.7)
- `--dev_ratio`: Ratio of files for development (default: 0.15)
- `--eval_ratio`: Ratio of files for evaluation (default: 0.15)
- `--seed`: Random seed for reproducibility (default: 42)

The script will:
1. Create the necessary directory structure
2. Scan and locate all audio files
3. Split the data into train/dev/eval sets
4. Copy files to the appropriate locations
5. Create protocol files needed for training

## FSD Model Training Script

The second script (`fsd_model.py`) trains the Self-Distillation Fake Speech Detection model using the organized data.

### Usage:

Before running, make sure to update the `BASE_DIR` variable in the script to point to your organized data directory:

```python
BASE_DIR = '/path/to/organized/audio/output'  # Update this path
```

Then run the script:

```bash
python fsd_model.py
```

### Configuration:

The script contains several configuration parameters you can modify:

- **Model parameters**: `MODEL_TYPE` ('eca' or 'se'), `MODEL_DEPTH` (9, 18, 34, or 50)
- **Training parameters**: Batch size, learning rate, number of epochs, etc.
- **Feature extraction parameters**: FFT settings, window type, etc.
- **Self-Distillation parameters**: Temperature, loss weights, etc.

### Output:

The training script will:
1. Extract F0 subband features from the audio files
2. Train the FSD model with self-distillation
3. Save the best model based on validation performance
4. Generate training curves and plots
5. Calculate and report the final Equal Error Rate (EER) and min t-DCF scores

## Directory Structure

After running the data organization script, your directory structure will look like this:

```
output_dir/
├── protocols/
│   ├── train.txt
│   ├── dev.txt
│   ├── eval.txt
│   └── eval_asv_scores.txt
├── train/
│   ├── natural/
│   └── spoof/
├── dev/
│   ├── natural/
│   └── spoof/
└── eval/
    ├── natural/
    └── spoof/
```

## Note on ASV Scores

For proper t-DCF calculation, you need to provide ASV scores for the evaluation set in the `eval_asv_scores.txt` file. If this file is not available or is empty, t-DCF calculation will be skipped, and the model will be evaluated using EER only.