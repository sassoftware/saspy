#!/usr/bin/env python3

# Author: Damjan Krstajic

import argparse
import saspy
import os.path
import sys

# Usage:
# ./run_sas.py -s example_1.sas
# ./run_sas.py -s example_1.sas example_2.sas
# ./run_sas.py -s example_1.sas -l out1.log -o out1.lst
# ./run_sas.py -s example_1.sas -r TEXT
# ./run_sas.py -s example_1.sas -r HTML
# ./run_sas.py -s example_1.sas -r htMl -l out2.log -o out2.html
# ./run_sas.py -s example_1.sas -r teXt -l out3.log -o out3.lst
# ./run_sas.py -s /home/a/b/c/example_1.sas
# ./run_sas.py -s example_1.sas -r text -l out4.log -o out4.lst -c ssh


def main():
    parser = argparse.ArgumentParser(description="It executes SAS code using saspy.")
    parser.add_argument('-s', '--sas_fname',nargs='+',help='Name of the SAS file to be executed.')
    parser.add_argument('-l', '--log_fname', help='Name of the output LOG file name. If not specified then it is the same as the sas_fname with .sas removed and .log added.')
    parser.add_argument('-o', '--lst_fname', help='Name of the output LST file. If not specified then it is the same as the sas_fname with .sas removed and .lst/.html added depending on the results format.')
    parser.add_argument('-r', '--results_format', help='Results format for sas_session.submit(). It may be either TEXT or HTML. If not specified it is TEXT by default. It is case incesensitive.')
    parser.add_argument('-c', '--cfgname', help='Name of the Configuration Definition to use for the SASsession. If not specified then just saspy.SASsession() is executed.')
    options = parser.parse_args()

    if options.sas_fname is None:
        parser.print_help()
        sys.exit(0)
    else:
        sas_fname = options.sas_fname
        for sfile in sas_fname:
            if(not os.path.isfile(sfile)):
                print("WARNING: SAS file (" + sfile + ") does not exist!")
        if(not os.path.isfile(sas_fname[-1])):
            print("\nThe last one of the SAS file(s) must be exist!\n")
            sys.exit(0)

    if options.log_fname is None:
        log_fname = os.path.splitext(sas_fname[-1])[0] + ".log"
        print("log_fname is " + log_fname )
    else:
        log_fname = options.log_fname

    if options.results_format is None:
        results_format = 'TEXT'
    elif options.results_format.upper() in ('HTML','TEXT'):
        results_format = options.results_format
    else:
        parser.print_help()
        sys.exit(0)

    if options.lst_fname is None:
        if results_format == 'HTML':
            lst_fname = os.path.splitext(sas_fname[-1])[0] + ".html"
        else:
            lst_fname = os.path.splitext(sas_fname[-1])[0] + ".lst"
        print("lst_fname is " + lst_fname )
    else:
        lst_fname = options.lst_fname

    sas_code_txt = ""
    for sfile in sas_fname:
        if(os.path.isfile(sfile)):
            sas_file     = open(sfile,mode='r')
            sas_code_txt = sas_code_txt + "\n\n" + sas_file.read()
            sas_file.close()

    if options.cfgname is None:
        sas_session = saspy.SASsession()
    else:
        sas_session = saspy.SASsession(cfgname=options.cfgname)

    c = sas_session.submit(sas_code_txt,results=results_format)

    with open(log_fname, 'w') as f1:
        f1.write(c["LOG"])

    with open(lst_fname, 'w') as f2:
        f2.write(c["LST"])

    sas_session.endsas()

if __name__ == '__main__':
    main()
