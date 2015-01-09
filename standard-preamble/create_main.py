#!/usr/bin/env python2



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument( '--docclass', '-d', default='', type=str, help='Define document class of latex document. Empty string uses standard docclass.' )
    
    parser.add_argument( '--title',  '-t', default='', type=str, help='Title tex Document. If empty, no call to \\maketitle.' )
    parser.add_argument( '--date',   '-D', default='', type=str, help='Date of tex document.' )
    parser.add_argument( '--author', '-a', default='', type=str, help='Author of tex document.' )

    parser.add_argument( '--input',  '-i', default='main.tex.in', type=str, help='Template file for tex document.' )
    parser.add_argument( '--output', '-o', default='main.tex', type=str, help='Target file for tex document.' )


    args = parser.parse_args()

    if args.docclass:
        docclass = 'docclass-%s' % args.docclass
    else:
        docclass = 'docclass'

    if args.title:
        maketitle = '\\maketitle'
    else:
        maketitle = ''

    with open( args.input, 'r' ) as i:
        template = i.read()
        document = template % ( docclass, args.title, args.author, args.date, maketitle )

    if args.output:
        with open( args.output, 'w' ) as o:
            o.write( document )
    else:
        print document
