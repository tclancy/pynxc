#!/usr/bin/env python
import os
import glob
import sys
import subprocess

def do_cmd(cmdlist):
    
    S=""
    
    if sys.platform=='win32':
        output=subprocess.Popen(
            cmdlist,stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    else:
        output=subprocess.Popen(
            cmdlist,stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)

    S=S+''.join(output.stdout.readlines())+''.join(output.stderr.readlines())
    
    return S

fnames=glob.glob('tutorial_samples/*.py')

fnames_with_errors=[]
for fname in fnames:
    
    print fname,"...",
    
    cmdlist=['./pynxc', fname]
    
    val=do_cmd(cmdlist)
    
    if "Error" in val:
        print "Error."
        print val
        fnames_with_errors.append(fname)
    else:
        print "Ok."


print "The following files had errors:"
for fname in fnames_with_errors:
    print "\t",fname
