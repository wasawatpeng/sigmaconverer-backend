from flask import Flask, request, redirect, url_for,json
import subprocess
import os

app = Flask(__name__)

def runEvt2Sigma(filename,title,author,level,desc,format):
    proc = subprocess.run(["python", "./evt2sigma/evt2sigma.py","-f","./input/EvtToSigma/"+filename,"-t",title,"-a",author,"-l",level,"-d",desc],capture_output="True",text="text")
    output = proc.stdout
    print(output,flush=True)
    return output

def runSigmaConverter(filename,format):
    match format:
        case "IBM Qradar":
            target = "qradar"
            config = "qradar"
        case "Splunk":
            target = "splunk"
            config = "splunk-windows"
        case "Elastic":
            target = "es-qs"
            config = "ecs-auditd"
        case "LogRhythm":
            target = "es-qs-lr"
            config = "logrhythm_winevent"
        case "Sumo Logic":
            target = "sumologic"
            config = "sumologic"
    proc = subprocess.run(["sigmac","-t",target,"-c",config,"./input/SigmaConverter/"+filename],capture_output="True",text="text")
    output = proc.stdout
    # print(output,flush=True)
    return output

def runSigma2Atk(uuid,filename):
    proc = subprocess.run(["sigma2attack","--rules-directory","./input/Sigma2Atk/"+uuid,"--out-file","./input/Sigma2Atk/"+uuid+"/output.json"],capture_output="True",text="text")
    output = proc.stdout
    print(output,flush=True)
    return output

@app.route('/api/EvtToSigma/<uuid>', methods=['POST'])
def EvtConvert(uuid):
    request_data = json.loads(request.data)
    reqContent = request_data['content']
    reqTitle = reqContent['title']
    reqAuthor = reqContent['author']
    reqLevel = reqContent['level']
    reqDesc = reqContent['desc']
    reqFormat = reqContent['format']
    reqSigma = reqContent['evtData']
    # print(reqContent,flush=True)
    filename = uuid+'.xml'
    file_obj = open('./input/EvtToSigma/'+filename,'w')
    file_obj.write(reqSigma)
    file_obj.close()
    convertOutput = runEvt2Sigma(filename,reqTitle,reqAuthor,reqLevel,reqDesc,reqFormat)
    return {"output":convertOutput}

@app.route('/api/sigmaConverter/<uuid>', methods=['POST'])
def ConvertToSigma(uuid):
    request_data = json.loads(request.data)
    reqContent = request_data['content']
    reqFormat =reqContent['format']
    reqSigma = reqContent['sigmaData']
    filename = uuid+'.yml'
    file_obj = open('./input/SigmaConverter/'+filename,'w')
    file_obj.write(reqSigma)
    file_obj.close()
    convertOutput = runSigmaConverter(filename,reqFormat)
    return {"output":convertOutput}

@app.route('/api/sigma2atk/<uuid>', methods=['POST'])
def Sigm2Atk(uuid):
    request_data = json.loads(request.data)
    reqContent = request_data['content']
    reqSigma = reqContent['sigmaData']
    filename = uuid+'.yml'
    os.mkdir("./input/Sigma2Atk/"+uuid)
    file_obj = open('./input/Sigma2Atk/'+uuid+"/"+filename,'w')
    file_obj.write(reqSigma)
    file_obj.close()
    runSigma2Atk(uuid,filename)
    file_out_obj = open('./input/Sigma2Atk/'+uuid+"/output.json",'r')
    convertOutput = file_out_obj.read()
    file_out_obj.close()
    print(convertOutput,flush=True)
    return {"output":convertOutput}

if __name__ == '__main__':
    app.run(debug=True)