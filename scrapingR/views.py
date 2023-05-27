from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import annonce


min_price = 10
max_price = 50

def list(request):
    if request.method == 'GET':
        search_query_link = request.GET.get('link', '')
        search_query_prix = request.GET.get('prix', '')
        if(search_query_link != '') :
            annonces = annonce.objects.filter(ANNONCE_LINK__icontains=search_query_link)
        elif(search_query_prix!= '') :
            annonces = annonce.objects.filter(annonce(prix__gte=min_price) & annonce(prix__lte=max_price))
        else:
            annonces = annonce.objects.all()
    else:
        annonces = annonce.objects.all()
    return render(request, 'list.html', {'annonces': annonces})


def sortbyprice(request):
    biens_immobiliers = BiensImmobilier.objects.all().order_by('prix')
    return render(request, 'list.html', {'annonces': biens_immobiliers})

def sortby_price(request):
    biens_immobiliers = BiensImmobilier.objects.all().order_by('-prix')
    return render(request, 'list.html', {'annonces': biens_immobiliers})

def sup_inf(request):
    if 'inf' in request.POST:
        query = request.POST.get('query')
        biens_immobiliers = BiensImmobilier.objects.filter(prix__lt=query)
        return render(request, 'list.html', {'annonces': biens_immobiliers})

    else:
        query = request.POST.get('query')
        biens_immobiliers = BiensImmobilier.objects.filter(prix__gt=query)
        return render(request, 'list.html', {'annonces': biens_immobiliers})

