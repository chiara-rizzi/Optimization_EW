#!/bin/python
from BatchTools import *
##
##
## CLASS JOBSET
##
##
class JobSet:
    ##_________________________________________________________________________
    ##
    def __init__(self,platform):        
        if(platform.find("lxplus")>-1):
            self.platform = "lxplus"
        elif(platform.find("pic")>-1):
            self.platform = "pic"
        else:
            printError("<!> In JobSet class constructor ... Sorry guy I do not know the platform you run on ... yet ... " + platform)
            self.platform = "pic"
        self.jobs=[]
        self.logDir=""
        self.scriptDir=""
        self.scriptName=""
        self.tarballPath=""
        self.queue=""
        self.jobRecoveryFileName="JobCheck.chk"
        self.writeSubmissionCommandsToFileOnly=False
    ##_________________________________________________________________________
    ##
    def addJob(self,job):
        self.jobs += [job]
    ##_________________________________________________________________________
    ##
    def size(self):
        return len(self.jobs)
    ##_________________________________________________________________________
    ##
    def clear(self):
        self.jobs=[]
        self.scriptName=""
    ##_________________________________________________________________________
    ##
    def setQueue(self,queue):
        self.queue=queue
    ##_________________________________________________________________________
    ##
    def setSubmissionCommandsFile(self,submissioncommandsfile):
        self.writeSubmissionCommandsToFileOnly=True
        self.submissioncommandsfile=submissioncommandsfile
    ##_________________________________________________________________________
    ##
    def setLogDir(self,logDir):
        self.logDir=logDir    
    ##_________________________________________________________________________
    ##
    def setScriptDir(self,scriptDir):
        self.scriptDir=scriptDir
    ##_________________________________________________________________________
    ##
    def setScriptName(self,name):
        self.scriptName=name
    ##_________________________________________________________________________
    ##
    def setTarBall(self,tarBall):
        self.tarballPath=tarBall
    
    ##_________________________________________________________________________
    ##
    def setJobRecoveryFile(self,name):
        self.jobRecoveryFileName = name
    ##_________________________________________________________________________
    ##
    def Initialize(self,f):
        f.write("#!/bin/bash \n")
        f.write("export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase \n")
        f.write("source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh \n")
        f.write("lsetup root \n")
        f.write("cd $TMPDIR \n")
        f.write("\n")
        f.write("echo '==> Before copying tarball'\n")
        f.write("ls -lrth\n")
        f.write("\n")
        f.write("cp -r "+self.tarballPath+" AnaCode.tgz \n")
        f.write("\n")
        f.write("echo '==> After copying the tarball'\n")
        f.write("ls -lrth\n")
        f.write("\n")
        f.write("tar xf AnaCode.tgz \n")
        f.write("echo '==> After extracting the tarball'\n")
        f.write("ls -lrth\n")
        f.write("\n")
        #f.write("rcSetup \n")
        #f.write("\n")
        #f.write("echo '==> After the setup' \n")
        #f.write("ls -lrth \n")
        #f.write("\n")
        f.write("\n")
        f.write("\n")
    ##_________________________________________________________________________
    ##
    def Running(self,f,job):
        f.write("export OUTDIR='"+job.outDir+"' \n")
        f.write("\n")
        f.write(job.execName + " ")
        for iArg in range(len(job.jobArguments)):
            f.write(" \""+job.jobArguments[iArg]+"\"")
        for iOption in range(len(job.jobOptions)):
            f.write("--"+job.jobOptions[iOption][0]+"="+job.jobOptions[iOption][1]+" ")
        f.write(">& "+job.jobName+".log \n")
        f.write("\n")
        f.write("echo '==> After running the code'\n")
        f.write("mkdir -p $OUTDIR\n")
        f.write("\n")
        f.write("mv *.root $OUTDIR \n")
        f.write("mv *.log $OUTDIR \n")
        f.write("\n")
        f.write("\n")
        f.write("\n")
    ##_________________________________________________________________________
    ##
    def Terminate(self,f):
        f.write("rm -rf $TMPDIR/*")
        f.write("\n")
    ##_________________________________________________________________________
    ##
    def writeScript(self):
        if(self.scriptName==""):
            self.scriptName = self.jobs[len(self.jobs)-1].jobName
    
        #Declaration of the output recovery tool
        f_reco_file = 0
        if not self.jobRecoveryFileName == "":
            f_reco_file = open(self.jobRecoveryFileName,"a")
        #Writting the scripts
        current_merged_script_name = self.scriptDir+"/"+self.scriptName
        f = open(current_merged_script_name,"w")
        self.Initialize(f)
        for iJob in range(len(self.jobs)):
            temp_job = self.jobs[iJob]
            self.Running(f,temp_job)
            
            #Also write a sub-script to make easier the resubmission of the jobs
            current_sub_script_name = self.scriptDir+"/sub_"+self.scriptName+"_"+temp_job.jobName
            f_sub = open(current_sub_script_name,"w")
            self.Initialize(f_sub)
            self.Running(f_sub,temp_job)
            self.Terminate(f_sub)
            f_sub.close()
        
            #Write the file to possibly relaunch the missing jobs
            if not self.jobRecoveryFileName == "":
                for iOption in range(len(temp_job.jobOptions)):
                    if temp_job.jobOptions[iOption][0].upper()=="OUTPUTFILE":
                        f_reco_file.write(temp_job.outDir+"/"+temp_job.jobOptions[iOption][1]+" "+current_sub_script_name+"\n")
                        break
        self.Terminate(f)
        f_reco_file.close()
        f.close()
        os.chmod(current_merged_script_name, 0755)
    ##_________________________________________________________________________
    ##
    def submitSet(self):
        com=""
        if(self.platform == "lxplus"):
            com += "bsub -q "
        elif(self.platform == "pic"):
            com += "qsub -q "
        else:
            printError("The system you are running on is not supported yet ... Please move to lxplus or PIC")
        if(self.queue==""):
            self.queue="at3_short"
        com += self.queue
        com += " " + self.scriptDir+"/"+self.scriptName+" "
        if not(self.logDir==""):
            if(self.platform == "lxplus"):
                com += " -o "+self.logDir+"/"+self.scriptName+"_batch.log -e "+self.logDir+"/"+self.scriptName+"_batch.log"
            else:
                com += " -o "+self.logDir+" -e "+self.logDir
        if self.writeSubmissionCommandsToFileOnly:
            self.submissioncommandsfile.write("echo "+self.scriptName+"\n")
            self.submissioncommandsfile.write(com+"\n")
        else:
            os.system(com)
##
##
## CLASS JOB
##
##
class Job:
    """
    Class allowing to deal transparently with all batch systems. The interface
    is done in the class (by the means of the platform variable), and not in 
    the script itself
    """
    ##_________________________________________________________________________
    ##
    def __init__(self,platform):
        if(platform.find("pic")>-1):
            self.platform = "pic"
        elif(platform.find("lxplus")>-1):
            self.platform = "lxplus"
        else:
            printError("<!> In Job class constructor ... Sorry guy I do not know the platform you run on ... " + platform)
            self.platform = "pic"
        self.debug = False
        self.jobOptions=[]
        self.jobArguments=[]
        self.jobName=""
        self.execName=""
        self.outDir=""
    ##_________________________________________________________________________
    ##
    def setDebug(self,debug):
        self.debug = debug
    ##_________________________________________________________________________
    ##
    def addOption(self,option,value):
        self.jobOptions += [[option,value]]
    ##_________________________________________________________________________
    ##
    def addArgument(self,value):
        self.jobArguments += [value]
    ##_________________________________________________________________________
    ##
    def setName(self,name):
        self.jobName=name
    
    ##_________________________________________________________________________
    ##
    def setExecutable(self,exe):
        self.execName = exe
    
    ##_________________________________________________________________________
    ##
    def setOutDir(self,outDir):
        self.outDir = outDir
