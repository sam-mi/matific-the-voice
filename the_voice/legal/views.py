from django.shortcuts import render


def terms_of_service(request):
    location = request.path
    return render(request, 'legal/terms-of-service.html', {
            'title': "Terms and Conditions",
            'location': location},
            )

def privacy_policy(request):
    location = request.path

    return render(request, 'legal/privacy-policy.html', {
            'title': "Privacy Policy",
            'location': location},
            )
