from django.shortcuts import redirect,render

def main(request):
    return render(request, 'UserTemplates/404.html')    