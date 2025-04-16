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

    out_file = "/publicfs/cms/user/wangzebing/ALP/NTuples/UL/18/data/"
    base_path = "/publicfs/cms/user/wangzebing/ALP/NTuples/UL/18/data/t2"

    dir_list = [
    #"DoubleMuon/crab_DoubleMuon_Run2018A-UL2018_MiniAODv2-v1/220127_103127/0000/*.root",
    #"DoubleMuon/crab_DoubleMuon_Run2018B-UL2018_MiniAODv2-v1/220127_103259/0000/*.root",
    #"DoubleMuon/crab_DoubleMuon_Run2018C-UL2018_MiniAODv2-v1/220127_103433/0000/*.root",
    #"DoubleMuon/crab_DoubleMuon_Run2018D-UL2018_MiniAODv2-v1/220127_103609/0000/*.root",
    #"DoubleMuon/crab_DoubleMuon_Run2018D-UL2018_MiniAODv2-v1/220127_103609/0001/*.root",
    #"EGamma/crab_EGamma_Run2018A-UL2018_MiniAODv2-v1/220127_101842/0000/*.root",
    #"EGamma/crab_EGamma_Run2018A-UL2018_MiniAODv2-v1/220127_101842/0001/*.root",
    #"EGamma/crab_EGamma_Run2018A-UL2018_MiniAODv2-v1/220127_101842/0002/*.root",
    #"EGamma/crab_EGamma_Run2018A-UL2018_MiniAODv2-v1/220127_101842/0003/*.root",
    #"EGamma/crab_EGamma_Run2018B-UL2018_MiniAODv2-v1/220127_102024/0000/*.root",
    #"EGamma/crab_EGamma_Run2018B-UL2018_MiniAODv2-v1/220127_102024/0001/*.root",
    #"EGamma/crab_EGamma_Run2018C-UL2018_MiniAODv2-v1/220127_102203/0000/*.root",
    #"EGamma/crab_EGamma_Run2018C-UL2018_MiniAODv2-v1/220127_102203/0001/*.root",
    #"EGamma/crab_EGamma_Run2018D-UL2018_MiniAODv2-v1/220127_102340/0000/*.root",
    #"EGamma/crab_EGamma_Run2018D-UL2018_MiniAODv2-v1/220127_102340/0001/*.root",
    #"EGamma/crab_EGamma_Run2018D-UL2018_MiniAODv2-v1/220127_102340/0002/*.root",
    #"EGamma/crab_EGamma_Run2018D-UL2018_MiniAODv2-v1/220127_102340/0003/*.root",
    #"EGamma/crab_EGamma_Run2018D-UL2018_MiniAODv2-v1/220127_102340/0004/*.root",
    #"EGamma/crab_EGamma_Run2018D-UL2018_MiniAODv2-v1/220127_102340/0005/*.root",
    #"EGamma/crab_EGamma_Run2018D-UL2018_MiniAODv2-v1/220127_102340/0006/*.root",
    #"EGamma/crab_EGamma_Run2018D-UL2018_MiniAODv2-v1/220127_102340/0007/*.root",
    #"MuonEG/crab_MuonEG_Run2018A-UL2018_MiniAODv2-v1/220127_102514/0000/*.root",
    #"MuonEG/crab_MuonEG_Run2018B-UL2018_MiniAODv2-v1/220127_102647/0000/*.root",
    #"MuonEG/crab_MuonEG_Run2018C-UL2018_MiniAODv2-v1/220127_102819/0000/*.root",
    #"MuonEG/crab_MuonEG_Run2018D-UL2018_MiniAODv2-v1/220127_102954/0000/*.root",
    #"SingleMuon/crab_SingleMuon_Run2018A-UL2018_MiniAODv2-v3/220127_101150/0000/*.root",
    #"SingleMuon/crab_SingleMuon_Run2018A-UL2018_MiniAODv2-v3/220127_101150/0001/*.root",
    #"SingleMuon/crab_SingleMuon_Run2018A-UL2018_MiniAODv2-v3/220127_101150/0002/*.root",
    #"SingleMuon/crab_SingleMuon_Run2018B-UL2018_MiniAODv2-v2/220127_101330/0000/*.root",
    #"SingleMuon/crab_SingleMuon_Run2018B-UL2018_MiniAODv2-v2/220127_101330/0001/*.root",
    "SingleMuon/crab_SingleMuon_Run2018C-UL2018_MiniAODv2-v2/220127_101522/0000/*.root",
    "SingleMuon/crab_SingleMuon_Run2018C-UL2018_MiniAODv2-v2/220127_101522/0001/*.root",
    "SingleMuon/crab_SingleMuon_Run2018D-UL2018_MiniAODv2-v3/220127_101701/0000/*.root",
    "SingleMuon/crab_SingleMuon_Run2018D-UL2018_MiniAODv2-v3/220127_101701/0001/*.root",
    "SingleMuon/crab_SingleMuon_Run2018D-UL2018_MiniAODv2-v3/220127_101701/0002/*.root",
    "SingleMuon/crab_SingleMuon_Run2018D-UL2018_MiniAODv2-v3/220127_101701/0003/*.root",
    "SingleMuon/crab_SingleMuon_Run2018D-UL2018_MiniAODv2-v3/220127_101701/0004/*.root",
    "SingleMuon/crab_SingleMuon_Run2018D-UL2018_MiniAODv2-v3/220127_101701/0005/*.root",
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
        if (verbose):
            print "skimmed_globbed_file_list has size =", len(skimmed_globbed_file_list)
        print "Files with 0B found:", len(globbed_list)-len(skimmed_globbed_file_list)


        out_path = out_file + "ntuple_" + dir_k.split('/')[0] + "_" + dir_k.split('/')[1].split('_')[2].split('-')[0] + "_" + dir_k.split('/')[3] + ".root"

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
