from django.shortcuts import render, redirect

# Create your views here.
from lists.models import Item


def home_page(request):
    return render(request=request, template_name='home.html')


def view_list(request):
    items = Item.objects.all()
    return render(
        request=request,
        template_name='list.html',
        context={'items': items}
    )


def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world/')
