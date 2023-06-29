## Introduction
![Model propose](images/mohinhtongquan.png"Overview model")

### A NOVEL WEB ATTACK DETECTION MODEL BASED ON REINFORCEMENT

Detect web attack using RL

## Structure

```
.
├── code-test (code evaluate DL)
│   └── model_DL (model DL after train)
├── data (data use for model RL)
│   ├── matrix1
│   ├── matrix2
│   ├── matrix3
│   ├── matrix4
│   └── matrix5 (final data)
│       ├── normal (dataset for RL)
│       ├── origin
│       └── temp
├── demo (code train/test model RL)
│   ├── model-x-x (model RL train at x/x)
│   └── model-OK (final model)
├── images 
├── new_data (data original)
│   ├── anomalous
│   │   ├── ECML-PKDD-2007
│   │   ├── fwaf
│   │   ├── HTTP_DATASET_CSIC_2010
│   │   └── HttpParamsDataset-master
│   └── normal
│       ├── ECML-PKDD-2007
│       ├── fwaf
│       ├── HTTP_DATASET_CSIC_2010
│       └── HttpParamsDataset-master
└── process_Data (code preprocess dataset and train DL)
    └── create_new_dataset (code create new dataset for RL)
```

Hai Ha - 30.06.2023