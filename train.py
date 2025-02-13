import argparse
import os
from pathlib import Path
import subprocess
import sys


def find_last_checkpoint(path: Path) -> Path | None:
    checkpoint_dirs = sorted(path.glob('lightning_logs/version_*'), key=lambda p: int(p.name.split('_')[-1]), reverse=True)
    if checkpoint_dirs is None:
        print('Lightning logs not found')
        return None
    
    for checkpoint_dir in checkpoint_dirs:
        checkpoint_files = list(checkpoint_dir.glob('checkpoints/*.ckpt'))
        if not checkpoint_files:
            continue
        return checkpoint_files[-1]
    else:
        print('Checkpoints not found')
        return None
    
ap = argparse.ArgumentParser()
ap.add_argument("--dataset-dir", required=True, help="path")
ap.add_argument("--resume_from_checkpoint")
a, u = ap.parse_known_args()
args = vars(a)


checkpoint_tag = "--resume_from_checkpoint"
path: Path | None = None
if args["resume_from_checkpoint"] is None:
    path = find_last_checkpoint(Path(args['dataset_dir']))
else:
    index = sys.argv.index("--resume_from_checkpoint")
    path = Path(sys.argv[index + 1])
    sys.argv.pop(index)
    sys.argv.pop(index + 1)


while True:
    args = sys.argv[1:].copy()
    args.extend([checkpoint_tag, str(path)])
    command = "cd piper/src/python && uv run -m piper_train " + " ".join(args)
    os.system(command)
    path = find_last_checkpoint(Path(args['dataset_dir']))

