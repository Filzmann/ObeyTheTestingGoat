from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home_page(request):
    return render(
        request=request,
        template_name='home.html',
        context={
            'new_item_text': request.POST.get(key='item_text', default=''),
        }
    )
