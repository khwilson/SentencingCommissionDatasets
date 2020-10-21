"""
Convert Sentencing Commission files into CSVs.

Usage:
  $ python3 convert.py [LIST OF FILES TO CONVERT]

@author Kevin H. Wilson <khwilson@gmail.com>
"""
import csv
import os
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Dict, List, Union

import click


def read_columns(filename: Union[str, Path]) -> List[Dict[str, Union[bool, int, str]]]:
    """
    Read the column names from the file with the passed name.
    Assumes it's in a SAS format that begins with INPUT and ends with
    a semicolon.

    Args:
      filename: The file name to read

    Returns:
      The list of column names where each element is a dict with key/vals:
        * name (str): The column name
        * is_char (bool): Whether the column is a string column
        * start (int): The (1-delimited) starting position of the column
        * end (int): The (1-delimited and inclusive) ending position of the column
    """
    columns = []
    with open(filename, "rt") as f:
        # Search for the line that starts with INPUT
        for line in f:
            if line.startswith("INPUT"):
                break

        for line in f:
            # Kill all the extra whitespace
            line = line.strip()

            # Is this the last line?
            if line.endswith(";"):
                # If so, strip the ; and the extra whitespace
                last_line = True
                line = line[:-1].strip()
            else:
                last_line = False

            # Parse row into column names
            i = 0
            sline = line.split()
            while i < len(sline):
                col_name = sline[i]
                i += 1

                if sline[i] == "$":
                    is_char = True
                    i += 1
                else:
                    is_char = False

                field_range = sline[i]
                i += 1

                # Field ranges are formatted either as # or #-#
                sfield_range = field_range.split("-")
                if len(sfield_range) == 1:
                    sfield_range = (sfield_range[0], sfield_range[0])

                # Write out the column to the list
                columns.append(
                    {
                        "name": col_name,
                        "is_char": is_char,
                        "start": int(sfield_range[0]),
                        "end": int(sfield_range[1]),
                    }
                )

            if last_line:
                break

    return columns


def convert_file(filename: Union[str, Path]):
    """
    Convert a file from the Sentencing Commission format into a CSV.
    Assumes the file is a ZIP file containing at least the following:
      - .sas: A file with the same name as `filename` except ending in .sas
      - .dat: A file with the same name as `filename` except ending in .dat

    The .dat file is a fixed-width file whose columns are described by the .sas
    file. If you're looking at the .sas file, search for INPUT and LENGTH to
    see the two main parts of the file. There are a _lot_ of columns.

    Args:
      filename: The name of the file to convert
    """
    filename = Path(filename)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Unzip the contents of the file
        with zipfile.ZipFile(filename, "r") as thefile:
            thefile.extractall(tmpdir)

        # Read in the column names from the .sas file
        sasfilename = filename.with_suffix(".sas").name
        saspath = tmpdir / sasfilename
        columns = read_columns(saspath)

        # Setup the path to the .dat file
        datfilename = filename.with_suffix(".dat").name
        datpath = tmpdir / datfilename

        # Open the output file
        outfilename = filename.with_suffix(".csv")
        badlines = []
        with open(outfilename, "wt") as outfile:
            # Write the column headers
            writer = csv.writer(outfile)
            writer.writerow([col["name"] for col in columns])

            # Read in the data
            with click.progressbar(length=os.stat(datpath).st_size) as bar:
                with open(datpath, "rb") as infile:
                    for line in infile:
                        bar.update(len(line))
                        line = line.decode("latin1")

                        # Read in a single row
                        readrow = []
                        for col in columns:
                            val = line[col["start"] - 1 : col["end"]].strip()

                            # If it's numeric and not missing, format it nicely
                            if val and not col["is_char"]:
                                if "." in val:
                                    val = float(val)
                                else:
                                    val = int(float(val))  # Handle 6e+10
                            readrow.append(val)

                        # Write out the row
                        writer.writerow(readrow)

    if badlines:
        badfilename = filename.with_suffix(".bad")
        with open(badfilename, "wb") as f:
            for line in badlines:
                f.write(line)


def main():
    for filename in sys.argv[1:]:
        convert_file(filename)


if __name__ == "__main__":
    main()
