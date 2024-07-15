from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .script import maincalc
from .forms import UploadFileForm
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def say_hello(request):
    return HttpResponse('Hello World')

@csrf_exempt
def run_maincalc(request):
    if request.method == 'POST':
        print(request.FILES)
        if 'file' not in request.FILES:
            return JsonResponse({"error": "No file uploaded", "files_received": list(request.FILES.keys())})
            #return HttpResponseBadRequest("No file uploaded")

        try:
            file = request.FILES['file']
            result = maincalc(file)
            #return result
            return JsonResponse(result)
        except Exception as e:
            return HttpResponseBadRequest(f"An error occurred: {str(e)}")
    else:
        return JsonResponse({"message": "Send a POST."})
