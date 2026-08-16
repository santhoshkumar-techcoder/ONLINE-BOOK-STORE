from django.contrib import admin
from store.models import Category, Book, Subscriber, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'is_featured', 'is_best_seller', 'is_new_arrival', 'is_audiobook')
    list_filter = ('category', 'is_featured', 'is_best_seller', 'is_new_arrival', 'is_audiobook', 'created_at')
    search_fields = ('title', 'author', 'description')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('General Details', {
            'fields': ('title', 'author', 'slug', 'category', 'price', 'description')
        }),
        ('Media Assets', {
            'fields': ('cover_image', 'cover_image_url')
        }),
        ('Featured States', {
            'fields': ('is_featured', 'is_best_seller', 'is_new_arrival')
        }),
        ('Audiobook Settings', {
            'fields': ('is_audiobook', 'audio_url')
        }),
        ('AI Summaries Cache', {
            'classes': ('collapse',),
            'fields': ('summary_cache',),
            'description': 'AI-generated dynamic content fetched automatically from Google Gemini API.'
        }),
    )


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    ordering = ('-subscribed_at',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('book', 'quantity', 'price', 'total_price')
    fields = ('book', 'quantity', 'price', 'total_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'email', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'first_name', 'last_name', 'email', 'phone')
    inlines = [OrderItemInline]
    readonly_fields = ('total_amount', 'created_at')
    
    fieldsets = (
        ('Order Overview', {
            'fields': ('id', 'status', 'total_amount', 'created_at')
        }),
        ('Recipient Shipping Details', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'zip_code')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'zip_code')
        return self.readonly_fields
