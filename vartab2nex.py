#!/usr/bin/env python3

from docopt import docopt
import sys
import csv
import datetime
import regex


def validate_row( row, header ):
    assert( len( row )==len( header ) )
    if( row != header ):
        assert( set( row[1:] ).issubset( set( [ '-', '?', '0', '1' ] ) ) )
    return row


def to_nex( input_filepath, output_filepath, description ):
    nexus_codes = []

    with open( input_filepath, 'r' ) as csv_file:
        csv_reader = csv.reader( csv_file )
        header = next( csv_reader, None )
        nexus_codes.append( validate_row( header, header ) )
        for row in csv_reader:
            try:
                nexus_codes.append( validate_row( row, header ) )
            except AssertionError:
                sys.exit( 'Error, unable to transform to Nexus format. Non validating row: {}'.format( row ) )

    transposed = list( zip(*nexus_codes) )[1:]

    ntax = len( transposed )
    nchar = len( transposed[0][1:] )

    nexus_str = '''#nexus
[Variant information ({}): {} {}.]
begin data;
  dimensions ntax={} nchar={};
  format symbols="01" missing=? gap=-;
  matrix
{}  ;
end;
'''

    date = datetime.datetime.now().strftime("%Y%m%d")
    desc = description
    witnesses = 'Witnesses sigla:'
    matrix = ''
    for row in transposed:
        witnesses += ' {}'.format( row[0] )
        matrix += '    {}  {}\n'.format( row[0], ''.join( row[1:] ) )

    if( not output_filepath ):
        output_filepath = input_filepath + '.nex'
    with open( output_filepath, 'w' ) as nexus_files:
        nexus_files.write( nexus_str.format( date, desc, witnesses, ntax, nchar, matrix ) )


doc = """vartable2nex.

Usage:
  vartable2nex.py [-o <outputfile>] <inputfile>
  vartable2nex.py [-o <outputfile>] [-d <description>] <inputfile>
  vartable2nex.py (-h | --help)

Options:
  -h --help          Show this help information.
  -o <outputfile>    Specify output file. If none the name of the input file
                     will be used with an added extension of .nex.
  -d <description>   Name or description of the Nexus informtion, defaults to
                     the input filename given. Only alphanumeric characters,
                     hyphens, periods, and underscores allowed; all whitespace
                     will be reduced to single space.

"""

if __name__ == '__main__':
    arguments = docopt( doc, version='vartable2nex 0.1' )
    description = arguments['<inputfile>']
    if( arguments['-d'] ):
        description = arguments['-d']
        description = ''.join( ch for ch in description if( ch.isalnum() or ch in ".,;:_- " ) )
        description = regex.sub( r'\s+', ' ', description )
        if( description[-1] != '.' ): description += '.'
    to_nex( arguments['<inputfile>'], arguments['-o'], description )
