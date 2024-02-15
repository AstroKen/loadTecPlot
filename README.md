# loadTecPlot

This library aims to provide an easy way to load tecplot formatted file to python program.

## Download
Download this library by
``` zsh
$ pip3 install git+https://github.com/AstroKen/loadTecPlot
```

## Usage

``` Python3
import loadTecPlot as ltp
import loadTecPlot.sshLoadTecPlot as sltp

fileData = ltp.loadTecPlot(<file path>)
fileData.loadFile()
print(fileData)

sshFileData = sltp.sshLoadTecPlot(HOSTNAME, USERNAME, KEY_FILENAME, SIGFILE, 1)
```

Access file contents from fileData object.
fileData object contains data in pandas dataframe format.
