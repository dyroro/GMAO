# monapp/middleware.py
class CacheRequestBodyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lire et stocker le corps de la requête
        request._body = request.body
        return self.get_response(request)