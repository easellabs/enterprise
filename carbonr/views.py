from django.http import JsonResponse

def health_check(request):
    """
    Health check endpoint to verify that the server is running.
    This can be used by load balancers or monitoring services.
    """
    return JsonResponse({"status": "healthy"}, status=200)
