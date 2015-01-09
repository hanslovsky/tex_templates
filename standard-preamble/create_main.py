#!/usr/bin/env python2

import os

PREAMBLE_FILES = {
    'docclass' : '%s',
    'commands' : 'commands.tex'
}

def create_default_package_list( directory ):
    with open( '%s/packages.tex' % directory ) as f:
        packages = []
        for line in f.readlines():
            packages.append( line.rstrip('\n') )
    return packages
   
def create_package_include_list( include, exclude, directory ):
    if include:
        packages = include
    else:
        packages = create_default_package_list( directory )

    deleteIndices = []
    for index, p in enumerate( packages ):
        if p in exclude:
            deleteIndices.append( index )


    for d in deleteIndices[::-1]:
        del packages[d]

    return packages

def package_list_to_string( packages, relative_path ):
    result = '\n'.join( '\\input{%s/packages/%s}%%' % ( relative_path, p ) for p in packages )
    return result

def copy_preamble_files( file_list, input_dir, preamble_dir ):
    for k, v in file_list.iteritems():
        copy_by_read_write( '%s/%s' % ( input_dir, v ), '%s/%s' % ( preamble_dir, v ) )

def remove_all_occurences( arr, val ):
    indices = []
    for i, a in enumerate( arr ):
        if a == val:
            indices.append( i )
    for i in indices[::-1]:
        del arr[i]

def copy_by_read_write( source, target ):
    with open( source, 'r' ) as s:
        with open( target, 'w' ) as t:
            t.write( s.read() )

if __name__ == "__main__":
    import argparse
    import copy
    parser = argparse.ArgumentParser()
    parser.add_argument( '--docclass', '-c', default='', type=str, help='Define document class of latex document. Empty string uses standard docclass.' )
    
    parser.add_argument( '--title',  '-t', default='', type=str, help='Title tex Document. If empty, no call to \\maketitle.' )
    parser.add_argument( '--date',   '-d', default='', type=str, help='Date of tex document.' )
    parser.add_argument( '--author', '-a', default='', type=str, help='Author of tex document.' )

    parser.add_argument( '--input',  '-i', default='.', type=str, help='Template file for tex document.' )
    parser.add_argument( '--output', '-o', default='main.tex', type=str, help='Target file for tex document.' )
    parser.add_argument( '--preamble-dir', '-p', default='preamble', type=str, help='Directory for storing preamble files, relative to tex master file.' )

    parser.add_argument( '--include-packages', '-I', default='', type=str, help='Include packages. Use all, if empty string.' )
    parser.add_argument( '--exclude-packages', '-E', default='', type=str, help='Exclude packages. None, if empty string.' )

    args = parser.parse_args()

    if args.docclass:
        docclass = 'docclass-%s' % args.docclass
    else:
        docclass = 'docclass'

    if args.title:
        maketitle = '\\maketitle'
    else:
        maketitle = ''

    include = args.include_packages.split(',')
    exclude = args.exclude_packages.split(',')

    remove_all_occurences( include, '' )
    remove_all_occurences( exclude, '' )

    files = copy.deepcopy( PREAMBLE_FILES )
    files[ 'docclass' ] = '%s.tex' % docclass

    replacements = ( args.preamble_dir,
                     docclass,
                     args.preamble_dir,
                     args.preamble_dir,
                     args.title,
                     args.author,
                     args.date,
                     maketitle )

    template_file = '%s/main.tex.in' % args.input

    packages = create_package_include_list( include, exclude, args.input )
    packages_string = package_list_to_string( packages, args.preamble_dir )

    target_root = os.path.dirname(os.path.abspath( args.output ) )

    with open( template_file, 'r' ) as i:
        template = i.read()
        document = template % replacements

    if args.output:
        preamble_dir = '%s/%s' % ( target_root, args.preamble_dir )
        packages_dir = '%s/packages' % ( preamble_dir, )
        try:
            os.makedirs( packages_dir )
        except Exception as e:
            pass
        with open( args.output, 'w' ) as o:
            o.write( document )
        with open( '%s/packages.tex'  % preamble_dir, 'w' ) as p:
            p.write( packages_string )

        for p in packages:
            copy_by_read_write( '%s/packages/%s.tex' % ( args.input, p ), '%s/%s.tex' % ( packages_dir, p ) )

        copy_preamble_files( files, args.input, preamble_dir )

        
            
    else:
        print document
        print
        print packages_string
        print
