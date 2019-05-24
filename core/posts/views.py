from django.shortcuts import render



def hello(request):
    return render(request, template_name='posts/main.html', context={'test':'AWESOME, ALL FINE.', 'profile':request.user})