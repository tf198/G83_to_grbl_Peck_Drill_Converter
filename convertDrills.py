# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 12:54:25 2016

@author: DTalaiver

This script converts G83 instructions to grbl accepted G-code.

Modified by Tris Forster for command line usage
"""

#drill parser


def g83_to_grbl(src, dst, retractFeed=20, clearHeight=0.25):

    for line in src:
        content = line.strip()
        elements = content.split(" ")
        if elements[0] != "G83": #if its not G83 just pass it out
            dst.write(content)
            dst.write('\n')
        else:
            dst.write(f';{content}\n')
            #extract elements from command
            for q in range(0,len(elements)):
                if "X" in elements[q]:
                    xCmd = elements[q]
                elif "Y" in elements[q]:
                    yCmd = elements[q]
                elif "Z" in elements[q]:
                    bottom = float(elements[q][1:])
                elif "Q" in elements[q]:
                    increment = float(elements[q][1:])
                elif "R" in elements[q]:
                    retract = (elements[q][1:])
                elif "F" in elements[q]:
                    plunge = elements[q]
            #begin pecking
            #go to position
            dst.write(f'G0{xCmd}{yCmd}\n')
            curDepth=0
            dst.write(f'G0Z0\n')
            while (curDepth>bottom):
                curDepth=curDepth-increment
                if curDepth<=bottom:
                    curDepth=bottom
                #plunge
                dst.write(f'G1Z{curDepth}{plunge}\n')
                #retract
                dst.write(f'G1Z{retract}F{retractFeed}\n')
            #pecking done
            dst.write(f'G0Z{clearHeight}\n')
           
                    
if __name__ == '__main__':

    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Convert G83 commands to GRBL")
    parser.add_argument('source',
            help="Source file")
    parser.add_argument('--outfile', '-o', default=None,
            help="Write to this file")
    parser.add_argument('--retract', '-r', type=float, default=20,
            help="Retract feed rate")
    parser.add_argument('--clearance', '-c', type=float, default=0.25,
            help="Clearance height")
    options = parser.parse_args()


    dest = sys.stdout

    if options.outfile:
        dest = open(options.outfile, 'w')

    with open(options.source) as f:
        g83_to_grbl(f, dest, options.retract, options.clearance)

    dest.close
