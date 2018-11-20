#!/bin/bash

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

mv opafy17-nid.zip opafy17nid.zip
mv opafy16-nid.zip opafy16nid.zip

mkdir -p data
mv *.zip data
