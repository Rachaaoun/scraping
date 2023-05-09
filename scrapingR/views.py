from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Produit
from django.db.models import Q

def list(request):
    produits = Produit.objects.all()
    return render(request, 'list.html', {'produits': produits})

def filter(request):
    produitF =Produit.objects.filter(titre='racha')
    return render(request, 'filter.html', {'produits': produitF})

def filter(request):
    query = request.GET.get("q", None)
    qs = Produit.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(titre__icontains=query)
                )

    context = {
        "list": qs,
    }
    template = "filter.html"
    return render(request, template, context)