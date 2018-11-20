import csv
import os
import sys
import tempfile
import zipfile

def read_columns(filename):
  columns = []
  with open(filename) as f:
    for line in f:
      if line.startswith('INPUT'):
        break
    
    for line in f:
      line = line.strip()
    
      # Is this the last line?
      if line.endswith(';'):
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
        if sline[i] == '$':
          is_char = True
          i += 1
        else:
          is_char = False
        field_range = sline[i]
        i += 1
        sfield_range = field_range.split('-')
        if len(sfield_range) == 1:
          sfield_range = (sfield_range[0], sfield_range[0])
        columns.append({
          'name': col_name,
          'is_char': is_char,
          'start': int(sfield_range[0]),
          'end': int(sfield_range[1])
        })
      if last_line:
        break
  return columns


def convert_file(filename):
  with tempfile.TemporaryDirectory() as tmpdir:
    with zipfile.ZipFile(filename, 'r') as thefile:
      thefile.extractall(tmpdir)

    sasfilename = os.path.basename(filename)[:-4] + '.sas'
    saspath = os.path.join(tmpdir, sasfilename)
    columns = read_columns(saspath)

    datfilename = os.path.basename(filename)[:-4] + '.dat'
    datpath = os.path.join(tmpdir, datfilename)

    outfilename = filename[:-4] + '.csv'
    with open(outfilename, 'wt') as outfile:
      writer = csv.writer(outfile)
      writer.writerow([col['name'] for col in columns])
      with open(datpath) as infile:
        for row_num, line in enumerate(infile):
          readrow = []
          for col in columns:
            val = line[col['start'] - 1:col['end']].strip()
            if val and not col['is_char']:
              if '.' in val:
                val = float(val)
              else:
                val = int(val)
            readrow.append(val)
          writer.writerow(readrow)

def main():
  filename = sys.argv[1]
  convert_file(filename)

if __name__ == '__main__':
  main()
