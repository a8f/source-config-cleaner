## Source Config Cleaner ##
Cleans up config files that are used by Source Engine games such as TF2 and CSGO 

#### Usage ####
```
cleaner.py [-h] [-o] [-v] [-rl] [-cl] [-R] [-re] [-rc] file [file ...]

positional arguments:
  file               File to parse

optional arguments:
  -h, --help         Show help message and exit
  -o, --outputdir	 Where to store output files. Default ./output/
  -v, --verbose      Log operations verbosely
  -rl, --rmlines     Remove empty lines from output file
  -cl, --cleanlines  Replace multiple empty lines with one empty line
  -R, --recursive    Run cleaner recursively on executed config files
  -re, --reverse     When overwriting binds and aliases use the first
                     assignment in the file rather than the last
  -rc, --rmcomments  Remove lines that are only comments. Leaves inline
                     comments intact.
```
	
#### Built with ####
	- Python 2.7