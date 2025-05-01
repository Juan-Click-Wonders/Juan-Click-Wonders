from django.shortcuts import render

def custom_page_not_found(request, exception):
    """
    Custom 404 error handler
    """
    return render(request, '404.html', status=404)

def custom_server_error(request):
    """
    Custom 500 error handler
    """
    return render(request, '500.html', status=500)
