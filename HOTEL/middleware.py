from django.contrib.auth import authenticate, login

class PaymentAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.session.get('payment_completed'):
            user = request.user

            if user.is_authenticated:
                return response

            # If the user is not authenticated, attempt to authenticate them
            user = authenticate(request=request)

            if user is not None:
                login(request, user)

        return response
