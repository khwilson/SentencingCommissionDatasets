# Converting Sentencing Commission Files into CSVs

The good news: The United States Sentencing Commission makes 
[_very_ detailed files](https://www.ussc.gov/research/datafiles/commission-datafiles#individual)
available about sentencing in the US. :tada:

The bad news: They are in a crazy fixed-width format and include SAS and SPSS scripts to read them into those programs and those programs alone. :scream:

So what can we do about it? Well, we can write a little converter that converts them all! These files will do that for you.

## Requirements

This is script has only been tested with Python 3 and it assumes you have `click` installed. But this is just for progress bars, so you can comment out those lines if you want.

## Usage

First you'll need to get the data from the Sentencing Commission. The script `getdata.sh` gives examples, and will itself download FY08-17's data files.

Next you'll need to point the script `convert.py` at the file. For instance,

```
$ python3 convert.py data/opafy14nid.zip
```

This will leave you a file called `data/opafy14nid.csv` in that folder.

Be warned, these files end up being quite large, so you may want to gzip or xzip them.

## License

MIT
