#!/usr/bin/python
import glob
import sys, os, pwd, commands
import optparse, shlex, re
import time
from time import gmtime, strftime
import math
import subprocess

import datetime
import threading
import multiprocessing

# define function for processing the external os commands
def processCmd(cmd, quite = 0):
    #    print cmd
    status, output = commands.getstatusoutput(cmd)
    if (status !=0 and not quite):
        print 'Error in processing command:\n   ['+cmd+']'
        print 'Output:\n   ['+output+'] \n'
        return "ERROR!!! "+output
    else:
        return output

def execCmd(cmd):
    try:
        print "cmd: %s start running%s" % (cmd,datetime.datetime.now())
        #os.system(cmd)
        subprocess.call(cmd)
        print "cmd: %s end running%s" % (cmd,datetime.datetime.now())
    except Exception, e:
        print '%s\t failed,reason: \r\n%s' % (cmd,e)

def hadd_file(*cmd):
    subprocess.call(cmd)

def hadd():
    start = time.time()
    verbose = 0

    train = 0

    if train:
        out_file = "/publicfs/cms/user/wangzebing/ALP/NTuples/UL/18/sig/train/"
    else:    
        out_file = "/publicfs/cms/user/wangzebing/ALP/NTuples/UL/18/sig/"
    base_path = "/publicfs/cms/user/wangzebing/ALP/NTuples/UL/18/sig/t2"

    dir_list = [
    "HZaTo2l2g_M1_TuneCP5_PSWeights_13TeV-madgraph_pythia8/*/*/0000/*.root",
    "HZaTo2l2g_M2_TuneCP5_PSWeights_13TeV-madgraph_pythia8/*/*/0000/*.root",
    "HZaTo2l2g_M3_TuneCP5_PSWeights_13TeV-madgraph_pythia8/*/*/0000/*.root",
    "HZaTo2l2g_M4_TuneCP5_PSWeights_13TeV-madgraph_pythia8/*/*/0000/*.root",
    "HZaTo2l2g_M5_TuneCP5_PSWeights_13TeV-madgraph_pythia8/*/*/0000/*.root",
    "HZaTo2l2g_M6_TuneCP5_PSWeights_13TeV-madgraph_pythia8/*/*/0000/*.root",
    "HZaTo2l2g_M7_TuneCP5_PSWeights_13TeV-madgraph_pythia8/*/*/0000/*.root",
    "HZaTo2l2g_M8_TuneCP5_PSWeights_13TeV-madgraph_pythia8/*/*/0000/*.root",
    "HZaTo2l2g_M9_TuneCP5_PSWeights_13TeV-madgraph_pythia8/*/*/0000/*.root",
    "HZaTo2l2g_M10_TuneCP5_PSWeights_13TeV-madgraph_pythia8/*/*/0000/*.root",
    "HZaTo2l2g_M15_TuneCP5_PSWeights_13TeV-madgraph_pythia8/*/*/0000/*.root",
    "HZaTo2l2g_M20_TuneCP5_PSWeights_13TeV-madgraph_pythia8/*/*/0000/*.root",
    "HZaTo2l2g_M25_TuneCP5_PSWeights_13TeV-madgraph_pythia8/*/*/0000/*.root",
    "HZaTo2l2g_M30_TuneCP5_PSWeights_13TeV-madgraph_pythia8/*/*/0000/*.root",
    ]

    total_file_list = []

    file_list1 = []
    file_list2 = []
    file_list3 = []
    file_list4 = []
    cmds = {}
    sub_p = {}

    for dir_k in dir_list:

        if (verbose): print "Searching through ", dir_k
        path_dir_k = os.path.join(base_path, dir_k)
        globbed_list = glob.glob(path_dir_k)
        if (verbose): print "globbed_list has size", len(globbed_list)
        total_file_list += globbed_list
        if (verbose): print "total_file_list has size", len(total_file_list), "\n"

        skimmed_globbed_file_list = list(filter(lambda x : os.path.getsize(x) > 0, globbed_list))

        # split signal sample to train and application sample
        if train:
            skimmed_globbed_file_list = list(filter(lambda x : float(x.split('/')[-1].split('_')[-1].split('.')[0])%2 == 0, skimmed_globbed_file_list))
        else:
            skimmed_globbed_file_list = list(filter(lambda x : float(x.split('/')[-1].split('_')[-1].split('.')[0])%2 == 1, skimmed_globbed_file_list))

        if (verbose):
            print "skimmed_globbed_file_list has size =", len(skimmed_globbed_file_list)
        print "Files with 0B found:", len(globbed_list)-len(skimmed_globbed_file_list)

        
        #out_path = out_file + "ntuple_" + dir_k.split('/')[0] + "_" + dir_k.split('/')[1].split('_')[2].split('-')[0] + "_" + dir_k.split('/')[3] + ".root"
        out_path = out_file + "ntuple_" + dir_k.split('/')[0].split('_')[1] + ".root"

        #print out_path


        cmds[dir_k] = ['hadd', '-f'] + [out_path] + skimmed_globbed_file_list
        #print cmds[dir_k]
        sub_p[dir_k] = multiprocessing.Process(target=hadd_file,args=(cmds[dir_k]))
        

    
    for dir_k in dir_list:
        sub_p[dir_k].start()

    for dir_k in dir_list:
        sub_p[dir_k].join()


    end = time.time()
    print str(round(end-start,3))+'s'
    



# run the submitAnalyzer() as main()
if __name__ == "__main__":
    hadd()
