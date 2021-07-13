# Preprocess data for infographicsVQA

Run download_data.sh to download data
```
bash download_data.sh
```
Directory folder structure after run ```download_data.py``` will like this:
```
|-- info_VQA
|   |-- test
|   |   |-- 10022.jpeg
|   |   |-- 10022.json
...
|   |-- train
|   `-- val
|-- json_files
|   |-- test.json
|   |-- train.json
|   `-- val.json
|-- =3.0.0
|-- download_data.sh
|-- generate_features.py
`-- README.md
```

Run generate_features.py to generate features for train, val or test set.
```
python3 generate_features.py --data train
                                    val
                                    test
```