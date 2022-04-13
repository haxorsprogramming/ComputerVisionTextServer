from django.shortcuts import render
from django.http import JsonResponse
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
# Create your views here.
@csrf_exempt
def mainApp(request):
    key = request.POST['subs_key']
    endpoint = request.POST['endpoint']
    img = request.post['imgData']

    subscription_key = key
    endpoint = endpoint
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))



    read_image_url = "https://s3.jagoanstorage.com/aditia-storage/asset/ktp_bg_anul.jpg"

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
        'hasil' : hasil
    }
    return JsonResponse(context, safe=False)
    