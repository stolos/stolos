from django.shortcuts import render

# Create your views here.
def projects_view(request):
    return render(request, 'dashboard/index.html')
