from .models import Product

def global_search_bar(request):
    return {
        "FullProductList": Product.objects.all()
    }