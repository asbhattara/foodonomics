from django.shortcuts import render

# Create your views here.
def home(request):
	context = {}
	a = 1
	context['a'] = 1
	return render(request, 'base.html', context)