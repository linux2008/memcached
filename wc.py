#!/usr/bin/env python

from optparse import OptionParser
import sys
import os

' a test argument'
'__autho__=json'

def opt():
    parser=OptionParser(usage="usage:%prog",version='%prog 1.2.1')
    parser.add_option('-c','--char',
                       dest='char',
                       action='store_true',
                       default=False,
                       help='only char')
    parser.add_option('-w','--word',
                       dest='word',
                       action='store_true',
                       default=False,
                       help='only word')
    parser.add_option('-l','--line',
                       dest='line',
                       action='store_true',
                       default=False,
                       help='only line')
    
    option,args=parser.parse_args()
    return option,args

def get_count(data):
    line=data.count('\n')
    word=len(data.split())
    char=len(data)
    return line,word,char

def main():
    option,args=opt()
    if not (option.char or option.word or option.line):
        option.char,option.word,option.line=True,True,True
    if args:
        line_total,word_total,char_total=0,0,0
        for fn in args:
            if os.path.isfile(fn):
                with open(fn) as fd:
                    data=fd.read()
                line,word,char=get_count(data)
                print_wc(option,line,word,char,fn)
                line_total += line
                word_total += word
                char_total += char 
            elif os.path.isdir(fn):
                print >> sys.stderr, '%s is a directory' %fn
            else:
                sys.stderr.write('%s: no such file or directory \n' %fn)
        if len(args) >1:        
            print_wc(option,line_total,word_total,char_total,'total')


    else:
        data=sys.stdin.read()
        fn=''
        line,word,char=get_count(data)
        print_wc(option,line,word,char,fn)

def print_wc(option,line,word,char,fn):
    if option.line:
        print line,    
    if option.word:
        print word,
    if option.char:
        print char,
    print fn
main()
