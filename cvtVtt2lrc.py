import os
import pdb
import re
import copy
import time

def cvt_vtt2lrc(input:str,output:str) -> None:
    inFile = open(input,'r',encoding="utf-8")
    Block_Ofst:int = 0
    outInfoList:list = list()
    curInfo:dict = None
    for line in inFile.readlines():
        if line.startswith("WEBVTT"):
            continue
        elif line == "\n":
            if curInfo != None:
                pushDict:dict = copy.deepcopy(curInfo)
                outInfoList.append(pushDict)
            Block_Ofst = 0
            curInfo = dict()
        elif Block_Ofst == 1:
            try:
                curInfo["BlockId"] = int(line)
            except:
                Block_Ofst = 0
        elif Block_Ofst == 2:
            curInfo["TimeMark"] = line
        elif Block_Ofst == 3:
            curInfo["Subtitle"] = line.replace("\n"," ")
        else:
            curInfo["Subtitle"] += line.replace("\n"," ") 
        Block_Ofst+=1
    inFile.close()

    outFile = open(output,'w',encoding="utf-8")
    for Info in outInfoList:
        startTime:str = Info["TimeMark"].replace("\n","").split("-->")[0]
        startTimeList:list = startTime.split(":")
        Hour:int = int(startTimeList[0])
        Mins:int = int(startTimeList[1])
        Scnd:str = startTimeList[2].replace(" ","")
        
        CvtMins:int = Hour*60 + Mins
        
        CvtTime:str = "%02d" % CvtMins

        outputLine:str = f"[{CvtTime}:{Scnd}]{Info['Subtitle']}\n"
        outFile.write(outputLine)
    outFile.close()


for root,dirs,files in os.walk('./'):
    for file in files:
        if file.endswith('.vtt'):
            inFilePath:str = f"{root}/{file}"
            outFilePath:str = f"{root}/{file.replace("vtt","lrc")}"
            cvt_vtt2lrc(inFilePath,outFilePath)
            
