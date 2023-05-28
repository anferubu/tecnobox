from django.shortcuts import render
from django.views import View




class Home(View):

    def get(self, request):
        context = {
            'user': request.user,
            'path': request.path
        }
        return render(request, 'shop/home.html', context)