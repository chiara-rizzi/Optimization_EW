#!/usr/bin/env python
import os
import string
import random
import re
import time
import socket
import getpass
import sys
import glob
##___________________________________________________________________
##
def printError(text):
    #prints text in red
    os.system("echo -e '\\033[41;1;37m "+text+" \\033[0m'")
##___________________________________________________________________
##
def printWarning(text):
    #prints text in orange
    os.system("echo -e '\\033[43;1;37m "+text+" \\033[0m'")
##___________________________________________________________________
##
def printGoodNews(text):
    #prints text in green
    os.system("echo -e '\\033[42;1;37m "+text+" \\033[0m'")
##___________________________________________________________________
##
def getSampleJobs():
    Result = "Optimization_new.py"
    return Result
##___________________________________________________________________
##
def filterListWithTemplate( originalTotalFile, templates, filterFile):
    com = "less "+originalTotalFile
    if len(templates):
        for temp in templates:
            com += " | grep "+temp
    com += " > "+filterFile
    result = os.system(com)
    return result
##___________________________________________________________________
##
def produceList(Patterns, InputDirectory, listName):
    com = "ls "+InputDirectory+"{*,*/*}.root*"
    if "/eos/atlas/" in InputDirectory:
        com = "/afs/cern.ch/project/eos/installation/atlas/bin/eos.select find -f "+InputDirectory+" | grep \"\\.root\""
    for iPattern in range(len(Patterns)):
        if Patterns[iPattern]=="": continue
        com += " | grep "+Patterns[iPattern]
    com += " | grep -v \":\""
    if "/eos/atlas/" in InputDirectory:
        com+=" | sed \'s/\/eos\/atlas\//root:\/\/eosatlas\/\/eos\/atlas\//g\'"
    com += " > "+listName
    result = os.system(com)
    return result
##___________________________________________________________________
##
def getCommandLineFromFile(listFileName):
    f = open(listFileName,"r")
    command_line = ""
    for line in f:
        line=line.replace("\n","")
        command_line += line
        command_line += ","
    command_line=command_line[:-1]#removing the last coma
    return command_line
##___________________________________________________________________
##
def prepareTarBall(pathToPackage,pathToTarball):
    current_folder = os.getcwd()
    os.chdir(pathToPackage)
    
    printGoodNews("=> Creating tarball !")
    print "   -> ", pathToTarball
    com = "tar czf " + pathToTarball + " * "
    os.system(com)
    printGoodNews("=> Tarball done :-)")
    
    os.chdir(current_folder)
