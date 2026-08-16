from store.cart import Cart

def cart(request):
    """Context processor that exposes the Cart object globally to all templates."""
    return {'cart': Cart(request)}
