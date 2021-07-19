#!/usr/bin/env python3

# Author: Damjan Krstajic

import argparse
import saspy
import os.path
import sys

# Usage:
# ./run_sas.py -s example_1.sas 
# ./run_sas.py -s example_1.sas -l out1.log -o out1.lst
# ./run_sas.py -s example_1.sas -r TEXT
# ./run_sas.py -s example_1.sas -r HTML 
# ./run_sas.py -s example_1.sas -r HTML -l out2.log -o out2.html 
# ./run_sas.py -s example_1.sas -r TEXT -l out3.log -o out3.lst 
# ./run_sas.py -s /home/a/b/c/example_1.sas 
 

def main():
    parser = argparse.ArgumentParser(description="Execute SAS code using saspy.")
    parser.add_argument('-s', '--sas_fname',help='name of the SAS file to be executed')
    parser.add_argument('-l', '--log_fname', help='name of the output LOG file name')
    parser.add_argument('-o', '--lst_fname', help='name of the output LST file')
    parser.add_argument('-r', '--results_format', help='results format for sas_session.submit(). It may be either TEXT or HTML. If not specified it is TEXT by default')
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

    if options.results_format is None:
        results_format = 'TEXT' 
    elif options.results_format in ('HTML','TEXT'):
        results_format = options.results_format
    else:
        parser.print_help()
        sys.exit(0)

    if options.lst_fname is None:
        base = os.path.basename(sas_fname)
        if results_format == 'HTML':
            lst_fname = os.path.splitext(base)[0] + ".html"
        else:
            lst_fname = os.path.splitext(base)[0] + ".lst"
        print("lst_fname is " + lst_fname )
    else:
        lst_fname = options.lst_fname

    sas_file     = open(sas_fname,mode='r')
    sas_code_txt = sas_file.read()
    sas_file.close()

    sas_session = saspy.SASsession()
    
    c = sas_session.submit(sas_code_txt,results=results_format)

    with open(log_fname, 'w') as f1:
        f1.write(c["LOG"])

    with open(lst_fname, 'w') as f2:
        f2.write(c["LST"])

    sas_session.endsas()

if __name__ == '__main__':
    main()

