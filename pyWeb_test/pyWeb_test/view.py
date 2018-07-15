# coding: utf-8
import time
from django.http import HttpResponse
from django.shortcuts import render
import textScore
import os


def upload_file(myfile):
    nowTime = int(time.time())
    newPath = os.path.join("C:\\Users\\13249\\Downloads\\sap_project\\pyWeb_test\\upload\\", myfile.name + str(nowTime))
    newFile = open(newPath, 'wb+')
    for chunk in myfile.chunks():
        newFile.write(chunk)
    newFile.close()

    fob = open(newPath)
    text = fob.read()
    newFile.close()
    return text


def processReq(request):
    ctx = {}
    if request.POST:
        text = request.POST['user_input']
        if text == "":
            myfile = request.FILES.get("user_file", None)
            if not myfile:
                return HttpResponse("no file and no text!")

            text = upload_file(myfile)

        ctx['rlt'] = textScore.mainProcess(text)
    return render(request, "index.html", ctx)
