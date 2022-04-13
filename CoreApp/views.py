from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import uuid
import base64

import boto3
from botocore.exceptions import NoCredentialsError


# Create your views here.
@csrf_exempt
def mainApp(request):
    key = request.POST['subs_key']
    endpoint = request.POST['endpoint']
    dataWajah = request.POST['imgData']
    ENDPOINT_S3 = request.POST['ENDPOINT_S3']
    ACCESS_KEY = request.POST['ACCESS_KEY']
    SECRET_KEY = request.POST['SECRET_KEY']

    subscription_key = key
    endpoint = endpoint
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    imgRandom = uuid.uuid4()
    nama_gambar = str(imgRandom)+".png"
    format, imgstr = dataWajah.split(";base64,")
    dataDecode = ContentFile(base64.b64decode(imgstr))
    # os.mkdir("ladun/sandbox_file/tempWebcam/"+ str(imgRandom))
    with open("ladun/tempImg/" + nama_gambar, "wb+") as f:
        for chunk in dataDecode.chunks():
            f.write(chunk)

    file_path = "ladun/tempImg/"+str(nama_gambar)

    upload_to_aws(file_path, 'facecloud-storage-3562', "data_trs/"+nama_gambar, ENDPOINT_S3, ACCESS_KEY, SECRET_KEY)


    read_image_url = "https://s3.jagoanstorage.com/facecloud-storage-3562/data_trs/"+nama_gambar

    # Call API with URL and raw response (allows you to get the operation location)
    read_response = computervision_client.read(read_image_url,  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)
    hasil = []
    # Print the detected text, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                # print(line.text)
                hasil.append(line.text)
    # print()

    context = {
        'status' : 'sukses',
        'hasil' : hasil,
        'path' : file_path
    }
    return JsonResponse(context, safe=False)
    

def upload_to_aws(local_file, bucket, s3_file, ENDPOINT_S3, ACCESS_KEY, SECRET_KEY):
    session = boto3.session.Session()
    client = session.client('s3', endpoint_url=ENDPOINT_S3, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    # s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    try:
        
        client.upload_file(local_file, bucket, s3_file, ExtraArgs={'ACL': 'public-read'})
        print("Upload Successful file : "+local_file)
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
