#!/bin/bash

wget https://www.ussc.gov/sites/default/files/zip/opafy19nid.zip
wget https://www.ussc.gov/sites/default/files/zip/opafy18nid.zip
wget https://www.ussc.gov/sites/default/files/zip/opafy17-nid.zip
wget https://www.ussc.gov/sites/default/files/zip/opafy16-nid.zip
wget https://www.ussc.gov/sites/default/files/zip/opafy15nid.zip
wget https://www.ussc.gov/sites/default/files/zip/opafy14nid.zip
wget https://www.ussc.gov/sites/default/files/zip/opafy13nid.zip
wget https://www.ussc.gov/sites/default/files/zip/opafy12nid.zip
wget https://www.ussc.gov/sites/default/files/zip/opafy11nid.zip
wget https://www.ussc.gov/sites/default/files/zip/opafy10nid.zip
wget https://www.ussc.gov/sites/default/files/zip/opafy09nid.zip
wget https://www.ussc.gov/sites/default/files/zip/opafy08nid.zip

mkdir -p data
mv *.zip data

for filename in $(ls data/*.zip); do
  echo "Working on ${filename}"
  python3 convert.py "${filename}"
  echo "Converting to xz"
  pv "${filename%????}.csv" | xz --stdout - > "${filename%????}.csv.xz"
  rm "${filename}"
done
