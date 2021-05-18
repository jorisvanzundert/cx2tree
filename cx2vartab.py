#!/usr/bin/env python3

from docopt import docopt
import csv

def to_variant_table( input_filepath, output_filepath, gap_as_variant=False, ignore_invariants=False ):

    witnesses = []
    with open( input_filepath, 'r' ) as csv_file:
        csv_reader = csv.reader( csv_file )
        for row in csv_reader:
            witnesses.append( row )
    ranks = list( zip(*witnesses) )

    variant_table = [ [ 'variant', *ranks[0] ] ]
    for rank in ranks[1:]:
        variants = set( rank )
        if( ( not ignore_invariants ) or ( len( variants ) > 1 ) ):
            for variant in variants:
                if( gap_as_variant ):
                    nexus_code = [ ( '-' if not variant.strip() else variant.strip() ) ]
                    for token in rank:
                        nexus_code.append( int( token==variant ) )
                    variant_table.append( nexus_code )
                else:
                    nexus_code = [ variant.strip() ]
                    if( nexus_code[0] != '' ):
                        for token in rank:
                            nexus_code.append( int( token==variant ) ) if( token.strip() != '' ) else nexus_code.append( '-' )
                        variant_table.append( nexus_code )

    if( not output_filepath ):
        output_filepath = input_filepath + '.csv'
    with open( output_filepath, 'w' ) as csv_file:
        writer = csv.writer( csv_file )
        writer.writerows( variant_table )


doc = """cx2vartabl.

Usage:
  cx2vartabl.py [-gn] [-o <outputfile>] <inputfile>
  cx2vartabl.py (-h | --help)

Options:
  -h --help           Show this help information.
  -o <outputfile>     Specify output file. If none the name of the input file
                      will be used with an added extension of .csv.
  -g --gap-variants   Encode gaps as variants (not -).
  -n --no-invariants  Do not encode non-variants.

"""

if __name__ == '__main__':
    arguments = docopt( doc, version='vartable2nex 0.1' )
    to_variant_table( arguments['<inputfile>'], arguments['-o'], arguments['--gap-variants'], arguments['--no-invariants'] )
