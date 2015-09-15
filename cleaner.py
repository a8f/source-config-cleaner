import argparse
import os, sys


def Main():
    parser = argparse.ArgumentParser(description = "Clean up properly formatted Source cfg files")
    parser.add_argument('file', type=argparse.FileType('r'), nargs='+')
    parser.add_argument("-v", "--verbose", help = "Log operations verbosely", action ="store_true")
    parser.add_argument("-cl", "--cleanlines", help = "Remove empty lines from output file", action = "store_true")
    parser.add_argument("-r", "--recursive", help = "Run cleaner recursively on executed config files", action="store_true")
    args = parser.parse_args()
    
    global verbose, rm_empty_lines, recursive

    verbose = args.verbose
    rm_empty_lines = args.cleanlines
    recursive = args.recursive
    
    if not os.path.exists("output"):
        os.makedirs("output")
    
    for f in args.file:
        if verbose:
            print "Parsing file " + f.name + "\n"
        parseFile(f)
        f.close()
        if verbose:
            print "Done parsing file " + f.name + "\n"

# Make sure ./output exists before running this
def parseFile(infile):
    outfile = open('output/' + infile.name, 'w+')
    aliases = {}
    loaded_files = {}
    binds = {}
    output = []
    lineNo = -1
    for line in infile:
        lineNo += 1
        line = line.rstrip()
        if line == "":
            if rm_empty_lines:
                lineNo -= 1
            else:
                output.append(line)
            continue   
        try:
            split_line = line.split(' ')
            command = split_line[0].lower()
            arg = split_line[1]
            if verbose:
                print "Parsing line --- " + line
            if command == "alias":
                if arg in aliases.keys():
                    output[aliases[arg]] = line
                    if verbose:
                        print "Alias " + arg + " already existed, overwriting"  
                else:
                    aliases[arg] = lineNo
                    output.append(line)
                    if verbose:
                        print "New alias " + arg + " added"                
            elif command == "bind":
                if arg.replace('"', "") in binds.keys():
                    output[binds[arg]] = line                    
                    if verbose:
                        print "Bind " + arg + " already existed, overwriting"
                else:
                    binds[arg] = lineNo
                    output.append(line)
                    if verbose:
                        print "New bind " + arg + " added"
            elif command == "exec":
                if arg in loaded_files.keys():
                    if verbose:
                        print "File " + arg + " already loaded"                      
                else:
                    output.append(line)
                    loaded_files[arg] = lineNo
                    if verbose:
                        print "New file " + arg + " added"
                    if recursive:
                        # TODO add protection for infinite recursion
                        # including configs that exec themselves and
                        # config a execing config b which itself execs config a
                        # add ./ to prevent files in subfolders being opened in /
                        try:
                            print "Recursively cleaning " + arg + ".cfg"                            
                            rec_file = open("./" + arg + ".cfg")
                            parseFile(rec_file)
                            rec_file.close()
                        except IOError as e:
                            print "Couldn't open " + arg + ".cfg: {0}".format(e.strerror)
                            
            else:
                output.append(line)
        except IndexError:
            print "Invalid line at line " + str(lineNo + 1) + ". Ignoring line." 
            lineNo -= 1

    if verbose:
        print "Writing commands to file:"            
    for l in output:
        outfile.write(l + "\n")
        if verbose:
            print "\t" + l

if __name__ == "__main__":
    Main()