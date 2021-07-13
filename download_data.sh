# Download model 
pip3 install -q spacy>=3.0.0
python3 -m spacy download en_core_web_lg


# Download data
wget -O train.json         https://aiclub.uit.edu.vn/file-server/Databases/DocVQA_2020-21/task_3/train/infographicVQA_train_v1.0.json
wget -O train_images.zip   https://aiclub.uit.edu.vn/file-server/Databases/DocVQA_2020-21/task_3/train/infographicVQA_train_v1.0_images.zip
wget -O train_ocr.tar.gz   https://aiclub.uit.edu.vn/file-server/Databases/DocVQA_2020-21/task_3/train/infographicVQA_train_v1.0_ocr_outputs.tar.gz

wget -O val.json           https://aiclub.uit.edu.vn/file-server/Databases/DocVQA_2020-21/task_3/val/infographicVQA_val_v1.0.json
wget -O val_images.zip     https://aiclub.uit.edu.vn/file-server/Databases/DocVQA_2020-21/task_3/val/infographicVQA_val_v1.0_images.zip
wget -O val_ocr.zip        https://aiclub.uit.edu.vn/file-server/Databases/DocVQA_2020-21/task_3/val/infographicVQA_val_v1.0_ocr_outputs.zip

wget -O test.json          https://aiclub.uit.edu.vn/file-server/Databases/DocVQA_2020-21/task_3/test/infographicVQA_val_v1.0.json
wget -O test_images.zip    https://aiclub.uit.edu.vn/file-server/Databases/DocVQA_2020-21/task_3/test/infographicVQA_val_v1.0_images.zip
wget -O test_ocr.zip       https://aiclub.uit.edu.vn/file-server/Databases/DocVQA_2020-21/task_3/test/infographicVQA_val_v1.0_ocr_outputs.zip

# For trainset
tar -xf train_ocr.tar.gz
unzip -q train_images.zip
ls -1 | grep info | sed -E "s/(.*)(_train_v1.0_)([^_]*)(.*)/\1\2\3\4 train_\3/" | xargs -n 2 mv
mkdir train
mv train_images/* train_ocr/* train

# For testset
unzip -q test_images.zip
unzip -q test_ocr.zip
ls -1 | grep info | sed -E "s/(.*)(_val_v1.0_)([^_]*)(.*)/\1\2\3\4 test_\3/" | xargs -n 2 mv
mkdir test
mv test_images/* test_ocr/* test

# For testset
unzip -q val_images.zip
unzip -q val_ocr.zip
ls -1 | grep info | sed -E "s/(.*)(_val_v1.0_)([^_]*)(.*)/\1\2\3\4 val_\3/" | xargs -n 2 mv
mkdir val
mv val_images/* val_ocr/* val

# Create folder to store all of dataset
mkdir info_VQA json_files
mv train/ val/ test/ info_VQA/
mv *.json json_files

# Remove empty folder and downloaded file
rm *.zip 
rm *tar.gz
find . -type d -empty -delete