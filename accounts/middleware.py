from django.http import HttpResponseRedirect
from django.urls import reverse

class AdminRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/admin/' and (not request.user.is_authenticated or not request.user.is_superuser):
            return HttpResponseRedirect(reverse('home'))
        
        response = self.get_response(request)
        return response