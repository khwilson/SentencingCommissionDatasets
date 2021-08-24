# Converting Sentencing Commission Files into CSVs

The good news: The United States Sentencing Commission makes
[_very_ detailed files](https://www.ussc.gov/research/datafiles/commission-datafiles#individual)
available about sentencing in the US. :tada:

The bad news: They are in a crazy fixed-width format and include SAS and SPSS scripts to read them into those programs and those programs alone. :scream:

So what can we do about it? Well, we can write a little converter that converts them all! These files will do that for you.

## I just want the data

It turns out the data is small enough that you can upload it to GitHub! However, it's lzma compressed. Here's how you can decompress them.

### First, a warning

These files are filled with tons of nulls. The typical file size compressed is around 10MB and uncompressed aroung 1.5GB. So so so many blank fields. Loading this directly into pandas on a small box will probably make your box sad. Instead, you should really look at the `usecols` kwarg of [pd.read_csv](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html).

### Mac

If you're using homebrew, just do

```
$ brew install xz
```

Then you can open the files by doing

```
$ unxz [FILENAME].xz
```

### Debian/Ubuntu

First install xz utilties

```
$ sudo apt update && sudo apt install xz-utils
```

Then you should be able to open files thus

```
$ xz -d [FILENAME].xz
```

### Windows

Both 7zip and WinZip will open these files for you. Download and install them at your leisure.

## Requirements

This is script has only been tested with Python 3 and it assumes you have `click` installed. But this is just for progress bars, so you can comment out those lines if you want.

## Usage

First you'll need to get the data from the Sentencing Commission. The script `getdata.sh` gives examples, and will itself download FY08-20's data files.

Next you'll need to point the script `convert.py` at the file. For instance,

```
$ python3 convert.py data/opafy14nid.zip
```

This will leave you a file called `data/opafy14nid.csv` in that folder.

Be warned, these files end up being quite large, so you may want to gzip or xzip them.

## License

MIT
