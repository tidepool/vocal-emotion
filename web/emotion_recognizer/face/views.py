from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import pymir
import pybetaface
from test_face import *
from image_rotate import *

@csrf_exempt
def home(request):
	if request.method == 'POST':
		f = request.FILES['file']
		destination = open('/Users/mayank/Developer/vocal-emotion-test/web/emotion_recognizer/old/test.jpg', 'wb+')
		for chunk in f.chunks():
			destination.write(chunk)
		destination.close()
		fix_orientation('/Users/mayank/Developer/vocal-emotion-test/web/emotion_recognizer/old/test.jpg', True)
		return HttpResponse(PerformSVM())
	else:
		return render_to_response('upload.html',{})