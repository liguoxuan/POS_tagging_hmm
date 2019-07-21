# POS Tagging Using HMM

Use the following command to train and test:

```bash
python train_and_test.py --filename your_dataset --times n
```

The dataset will be randomly partitioned into train set and test set with a ratio of 9:1 and an HMM model will be trained and tested based on those two sets. The process will be repeated n times.

The default setting of filename and times are 'brown-universal.txt' and 10.

### Notice

The format of your dataset has to be the same as the one provided. 