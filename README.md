# Larynx

A fast, local neural text to speech system.

``` sh
echo 'Welcome to the world of speech synthesis!' | \
  ./larynx --model en-us-blizzard_lessac-medium.onnx --output_file welcome.wav
```

## Voices

* [U.S. English](https://github.com/rhasspy/larynx2/releases/download/v0.0.2/voice-english.tar.gz) (22Khz, single speaker)
* [German](https://github.com/rhasspy/larynx2/releases/download/v0.0.2/voice-german.tar.gz) (16Khz, single speaker)
* [Danish](https://github.com/rhasspy/larynx2/releases/download/v0.0.2/voice-danish.tar.gz) (22Khz, multispeaker)
* [Norweigian](https://github.com/rhasspy/larynx2/releases/download/v0.0.2/voice-norweigian.tar.gz) (22Khz, single speaker)
* [Nepali](https://github.com/rhasspy/larynx2/releases/download/v0.0.2/voice-nepali.tar.gz) (16Khz, multispeaker)
* [Vietnamese](https://github.com/rhasspy/larynx2/releases/download/v0.0.2/voice-vietnamese.tar.gz) (16Khz, multispeaker)


## Purpose

Larynx is meant to sound as good as [CoquiTTS](https://github.com/coqui-ai/TTS), but run reasonably fast on the Raspberry Pi 4.

Voices are trained with [VITS](https://github.com/jaywalnut310/vits/) and exported to the [onnxruntime](https://onnxruntime.ai/).


## Installation

Download a release:

* [amd64](https://github.com/rhasspy/larynx2/releases/download/v0.0.2/larynx_amd64.tar.gz) (desktop Linux)
* [arm64](https://github.com/rhasspy/larynx2/releases/download/v0.0.2/larynx_arm64.tar.gz) (Raspberry Pi 4)

If you want to build from source, see the [Makefile](Makefile) and [C++ source](src/cpp). Last tested with [onnxruntime](https://github.com/microsoft/onnxruntime) 1.13.1.


## Usage

1. [Download a voice](#voices) and extract the `.onnx` and `.onnx.json` files
2. Run the `larynx` binary with text on standard input, `--model /path/to/your-voice.onnx`, and `--output_file output.wav`

For example:

``` sh
echo 'Welcome to the world of speech synthesis!' | \
  ./larynx --model blizzard_lessac-medium.onnx --output_file welcome.wav
```

For multi-speaker models, use `--speaker <number>` to change speakers (default: 0).

See `larynx --help` for more options.


## Training

See [src/python](src/python)

Start by creating a virtual environment:

``` sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install --upgrade pip
pip3 install --upgrade wheel setuptools
pip3 install -r requirements.txt
```

Ensure you have [espeak-ng](https://github.com/espeak-ng/espeak-ng/) installed (`sudo apt-get install espeak-ng`).

Next, preprocess your dataset:

``` sh
python3 -m larynx_train.preprocess \
  --language en-us \
  --input-dir /path/to/ljspeech/ \
  --output-dir /path/to/training_dir/ \
  --dataset-format ljspeech \
  --sample-rate 22050
```

Datasets must either be in the [LJSpeech](https://keithito.com/LJ-Speech-Dataset/) format or from [Mimic Recording Studio](https://github.com/MycroftAI/mimic-recording-studio) (`--dataset-format mycroft`).

Finally, you can train:

``` sh
python3 -m larynx_train \
    --dataset-dir /path/to/training_dir/ \
    --accelerator 'gpu' \
    --devices 1 \
    --batch-size 32 \
    --validation-split 0.05 \
    --num-test-examples 5 \
    --max_epochs 10000 \
    --precision 32
```

Training uses [PyTorch Lightning](https://www.pytorchlightning.ai/). Run `tensorboard --logdir /path/to/training_dir/lightning_logs` to monitor. See `python3 -m larynx_train --help` for many additional options.

It is highly recommended to train with the following `Dockerfile`:

``` dockerfile
FROM nvcr.io/nvidia/pytorch:22.03-py3

RUN pip3 install \
    'pytorch-lightning'

ENV NUMBA_CACHE_DIR=.numba_cache
```

See the various `infer_*` and `export_*` scripts in [src/python/larynx_train](src/python/larynx_train) to test and export your voice from the checkpoint in `lightning_logs`. The `dataset.jsonl` file in your training directory can be used with `python3 -m larynx_train.infer` for quick testing:

``` sh
head -n5 /path/to/training_dir/dataset.jsonl | \
  python3 -m larynx_train.infer \
    --checkpoint lightning_logs/path/to/checkpoint.ckpt \
    --sample-rate 22050 \
    --output-dir wavs
```

