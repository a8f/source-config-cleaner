import argparse
import os
import sys


def Main():
    parser = argparse.ArgumentParser(
        description="Refactor Source config files")
    parser.add_argument("file", help="File to parse", nargs="+")
        parser.add_argument(
        "-o", "--outputdir", help="Where to store output files. Default ./output", action="store")
    parser.add_argument("-v", "--verbose",
                        help="Log operations verbosely", action="store_true")
    parser.add_argument(
        "-rl", "--rmlines", help="Remove empty lines from output file", action="store_true")
    parser.add_argument("-cl", "--cleanlines",
                        help="Replace multiple empty lines with one empty line", action="store_true")
    parser.add_argument(
        "-R", "--recursive", help="Run cleaner recursively on executed config files", action="store_true")
    parser.add_argument(
        "-re", "--reverse", help="When overwriting binds and aliases use the first assignment in the file rather than the last", action="store_true")
    parser.add_argument("-rc", "--rmcomments",
                        help="Remove comment lines. Leaves inline comments intact.", action="store_true")

    args = parser.parse_args()

    global verbose, rm_empty_lines, reduce_empty_lines, recursive, reverse, rm_comments, output_file_loc

    output_file_loc = args.outputdir if args.outputdir is not None else "./output/"
    verbose = args.verbose
    rm_empty_lines = args.rmlines
    recursive = args.recursive
    reduce_empty_lines = args.cleanlines
    reverse = args.reverse
    rm_comments = args.rmcomments

    if not os.path.exists("output"):
        os.makedirs("output")

    for filename in args.file:
        if verbose:
            print "Parsing file " + filename + "\n"
        parse_status = parseFile(filename)
        if parse_status == -1:
            print "Could not parse file " + filename + ".\n"
        elif verbose:
            print "Successfully parsed " + parse_status + " lines of file " + filename + "\n"

# Open file named infile_name and parse it, writing output to output_file_loc/infile_name
# Returns how many lines were parsed or -1 if an error ocurred
def parseFile(infile_name, loaded_files={}):
    outfile = open(output_file_loc + infile_name, 'w+')
    aliases = {}
    binds = {}
    output = []
    lineNo = 0
    removedLines = 0
    with open(infile_name) as infile:
        for line in infile:
            lineNo += 1
            line = line.rstrip()
            if line == "":
                if rm_empty_lines:
                    lineNo -= 1
                elif reduce_empty_lines:
                    removedLines += 1
                else:
                    output.append(line)
                continue
            else:
                removedLines = 0
            try:
                split_line = line.split(' ')
                command = split_line[0].lower()
                arg = split_line[1]
                if verbose:
                    print "Parsing line: " + line
                if command[:2] == "//":
                    if rm_comments:
                        print "Removed comment on line " + lineNo
                        continue
                elif command == "alias":
                    if arg in aliases.keys():
                        if reverse:
                            print "Alias " + arg + " ignored on line " + lineNo
                        elif verbose:
                            output[aliases[arg]] = line
                            print "Alias " + arg + " already existed, overwriting"
                    else:
                        aliases[arg] = lineNo
                        output.append(line)
                        if verbose:
                            print "Alias " + arg + " parsed"
                elif command == "bind":
                    if reverse:
                        print "Bind " + arg + " ignored on line " + lineNo
                    else:
                        if arg.replace('"', "") in binds.keys():
                            if verbose:
                                print "Bind " + arg + " already existed at line" + output[binds[arg]] + ", overwriting"
                            output[binds[arg]] = line
                        else:
                            binds[arg] = lineNo
                            output.append(line)
                            if verbose:
                                print "Bind " + arg + " parsed"
                elif command == "exec":
                    if arg in loaded_files.keys():
                        if reverse:
                            if arg in loaded_files.keys():
                                print "exec" + arg + " on line " + lineNo + " ignored because " + arg + " was already executed"
                                continue
                        else:
                            output.pop(loaded_files[arg])
                            if verbose:
                                print "File " + arg + " already cleaned"
                    else:
                        output.append(line)
                        loaded_files[arg] = lineNo
                        if verbose:
                            print "Cleaned file " + arg + (".cfg" if ".cfg" not in arg else "")
                        if recursive:
                            if arg in loaded_files:
                                print arg + " already cleaned, ignoring line " + lineNo
                            try:
                                print "Recursively cleaning " + arg + ".cfg"
                                parseFile(rec_file)
                                rec_file.close()
                            except IOError as e:
                                print "Couldn't open " + arg + ".cfg: {0}".format(e.strerror)

                else:
                    output.append(line)
            except IndexError:
                output.append(line)
                if verbose:
                    print "Line " + lineNo + " has no argument, copying anyway"

    if verbose:
        print "Writing commands to file:"
    for l in output:
        outfile.write(l + "\n")
        if verbose:
            print "\t" + l

    return lineNo


def validate(line):
    return


if __name__ == "__main__":
    Main()
