from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from store.models import Category, Book, Subscriber, Order, OrderItem
from store.cart import Cart
from store.gemini_helper import get_book_summary

def home(request):
    """Render the landing home page with featured books, best sellers, etc."""
    featured_books = Book.objects.filter(is_featured=True)[:4]
    best_sellers = Book.objects.filter(is_best_seller=True)[:4]
    new_arrivals = Book.objects.filter(is_new_arrival=True).order_by('-created_at')[:4]
    audiobooks = Book.objects.filter(is_audiobook=True)[:4]
    categories = Category.objects.all()

    context = {
        'featured_books': featured_books,
        'best_sellers': best_sellers,
        'new_arrivals': new_arrivals,
        'audiobooks': audiobooks,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


def book_list(request, category_slug=None):
    """Display the full catalog of books with category and keyword search filters."""
    category = None
    categories = Category.objects.all()
    books = Book.objects.all()
    
    # Text search
    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) | 
            Q(description__icontains=query)
        )

    # Category filter
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'books': books,
        'query': query,
    }
    return render(request, 'store/book_list.html', context)


def book_detail(request, slug):
    """Display detail page for a single book, triggering AI summary on demand."""
    book = get_object_or_404(Book, slug=slug)
    
    # Check if AI Summary is cached, otherwise fetch it from Gemini
    if not book.summary_cache or len(book.summary_cache.strip()) < 10:
        summary = get_book_summary(
            title=book.title, 
            author=book.author, 
            description=book.description,
            category_name=book.category.name
        )
        book.summary_cache = summary
        book.save(update_fields=['summary_cache'])
        
    context = {
        'book': book,
    }
    return render(request, 'store/book_detail.html', context)


# Newsletter Subscriber view
def newsletter_subscribe(request):
    """Handle newsletter submissions from the page footer."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            if Subscriber.objects.filter(email=email).exists():
                messages.warning(request, "This email is already subscribed to our newsletter!")
            else:
                Subscriber.objects.create(email=email)
                messages.success(request, "Thank you! You have successfully subscribed to our newsletter.")
        else:
            messages.error(request, "Please enter a valid email address.")
    
    # Redirect back to the page the user subscribed from, or home
    next_url = request.META.get('HTTP_REFERER', 'store:home')
    return redirect(next_url)


# Shopping Cart Views
def cart_detail(request):
    """Render the shopping cart details page."""
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def cart_add(request, book_id):
    """Add a book to the shopping cart."""
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    
    quantity = int(request.POST.get('quantity', 1))
    override_quantity = request.POST.get('override', False) == 'True'
    
    cart.add(book=book, quantity=quantity, override_quantity=override_quantity)
    messages.success(request, f"Added '{book.title}' to your cart.")
    return redirect('store:cart_detail')


def cart_remove(request, book_id):
    """Remove a book from the shopping cart."""
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    messages.success(request, f"Removed '{book.title}' from your cart.")
    return redirect('store:cart_detail')


def cart_update(request, book_id):
    """Update book quantity in the shopping cart."""
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart.add(book=book, quantity=quantity, override_quantity=True)
        messages.success(request, f"Updated quantity for '{book.title}'.")
    else:
        cart.remove(book)
        messages.success(request, f"Removed '{book.title}' from your cart.")
        
    return redirect('store:cart_detail')


# Checkout & Order Success Views
def checkout(request):
    """Handle dummy customer checkout processing."""
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty! Add books to your cart first.")
        return redirect('store:book_list')
        
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        
        # Create Order
        order = Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            zip_code=zip_code,
            total_amount=cart.get_total_price(),
            status='Pending'
        )
        
        # Create OrderItems
        for item in cart:
            OrderItem.objects.create(
                order=order,
                book=item['book'],
                quantity=item['quantity'],
                price=item['price']
            )
            
        # Clear cart session
        cart.clear()
        
        messages.success(request, "Your order has been placed successfully!")
        return redirect('store:order_success', order_id=order.id)
        
    return render(request, 'store/checkout.html', {'cart': cart})


def order_success(request, order_id):
    """Render the thank you and order receipt page."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {'order': order})
