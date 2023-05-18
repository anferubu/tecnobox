from django.shortcuts import render
from django.views import View




class AboutUs(View):
    """
    Página "Sobre Nosotros".
    """

    def get(self, request):
        """
        Muestra la página con información sobre la empresa.
        """
        return render(request, 'shop/about_us.html')