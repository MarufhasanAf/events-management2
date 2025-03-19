from django.shortcuts import render, HttpResponse

# Create your views here.
def test(request):
    return render(request, "test.html")
def home(request):
    return render(request, "home.html")
def dashboard(request):
    return render(request, "dashboard.html")
def categories(request):
    return render(request, "category_list.html")

def participants(request):
    return render(request, "participants_list.html")
def event_details(request):
    return render(request, "event_details.html")