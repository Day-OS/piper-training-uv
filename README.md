# Why even does this repository exists

Because I got tired of python libraries requirements not being stable enough and needing to read 
3 different github issues telling about how x thing solved it, how y thing was the solution.

So I decided I'm just going to use "UV" to have one ONLY stable setup that will work

```sh
task preprocess --input-dir '<input-path>' --output-dir '<output-path>' --language pt-br --sample-rate 16000 --dataset-format ljspeech --single-speaker --max-workers 1
```

[Grab a checkpoint from here](https://huggingface.co/datasets/rhasspy/piper-checkpoints/tree/main)
```sh
task train --dataset-dir '<output-path>' --batch-size 32 --accelerator 'cpu' --resume_from_checkpoint '<checkpoint-file>' --max_epochs 10000 
```