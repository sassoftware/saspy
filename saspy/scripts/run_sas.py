#!/usr/bin/env python3

# Author: Damjan Krstajic

import argparse
import saspy
import os.path
import sys

# Usage:
# ./run_sas.py -s example_1.sas 
# ./run_sas.py -s example_1.sas -l saspy.log -o saspy.lst

def main():
    parser = argparse.ArgumentParser(description="Execute SAS code using saspy.")
    parser.add_argument('-s', '--sas_fname',help='name of the SAS file to be executed')
    parser.add_argument('-l', '--log_fname', help='name of the output LOG file name')
    parser.add_argument('-o', '--lst_fname', help='name of the output LST file')
    options = parser.parse_args()

    if options.sas_fname is None:
        parser.print_help()
        sys.exit(0)
    elif(not os.path.isfile(options.sas_fname)):
        print("\nSAS file does not exist\n")
        sys.exit(0)

    sas_fname = options.sas_fname

    if options.log_fname is None:
        base      = os.path.basename(sas_fname)
        log_fname = os.path.splitext(base)[0] + ".log"
        print("log_fname is " + log_fname )
    else:
        log_fname = options.log_fname

    if options.lst_fname is None:
        base      = os.path.basename(sas_fname)
        lst_fname = os.path.splitext(base)[0] + ".lst"
        print("lst_fname is " + lst_fname )
    else:
        lst_fname = options.lst_fname

    sas_file     = open(sas_fname,mode='r')
    sas_code_txt = sas_file.read()
    sas_file.close()

    sas_session = saspy.SASsession()
    
    c = sas_session.submit(sas_code_txt,results="TEXT")

    with open(log_fname, 'w') as f1:
        f1.write(c["LOG"])

    with open(lst_fname, 'w') as f2:
        f2.write(c["LST"])

    sas_session.endsas()

if __name__ == '__main__':
    main()

