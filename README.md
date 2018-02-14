# CallHome Database Plugin

## Download
Download the CallHome dataset from [here](https://talkbank.org/access/CABank/CallHome/eng.html)

## Generate
```bash
# Put CallHome transcripts and audio files in same folder

# Convert all files from mp3 to wav format
> python utils.py ~/Downloads/CABank_CallHome

# Get the training, validation and test splits
> python parse_transcripts.py ~/Downloads/CABank_CallHome 0.9 0.1
```
