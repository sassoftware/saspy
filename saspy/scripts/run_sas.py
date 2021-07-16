#!/usr/bin/env python3

import argparse
import saspy
import os.path
import sys

# Usage:
# ./run_sas.py -s example_1.sas -l saspy.log -o saspy.lst

def main():
    parser = argparse.ArgumentParser(description="Execute SAS code using saspy.")
    parser.add_argument('-s', '--sas_fname',help='name of the SAS file to be executed')
    parser.add_argument('-l', '--log_fname', help='name of the output LOG file name')
    parser.add_argument('-o', '--lst_fname', help='name of the output LST file')
    options = parser.parse_args()

    if options.log_fname is None:
        parser.print_help()
        sys.exit(0)

    if options.lst_fname is None:
        parser.print_help()
        sys.exit(0)

    if options.sas_fname is None:
        parser.print_help()
        sys.exit(0)
    elif(not os.path.isfile(options.sas_fname)):
        print("\nSAS file does not exist\n")
        sys.exit(0)

    sas_fname = options.sas_fname
    log_fname = options.log_fname
    lst_fname = options.lst_fname

    sas_file     = open(sas_fname,mode='r')
    sas_code_txt = sas_file.read()
    sas_file.close()

    sas_session = saspy.SASsession()
    
    c = sas_session.submit(sas_code_txt,results="TEXT")

    original_stdout = sys.stdout

    with open(log_fname, 'w') as f1:
        sys.stdout = f1
        print(c["LOG"])
        sys.stdout = original_stdout

    with open(lst_fname, 'w') as f2:
        sys.stdout = f2
        print(c["LST"])
        sys.stdout = original_stdout

    sas_session.endsas()

if __name__ == '__main__':
    main()

