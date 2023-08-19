from django import template
from cart.models import CartItems,Wishlist, WishlistItem


register = template.Library()

@register.simple_tag(takes_context=True)
def cart_items_count(context):
    user = context['request'].user
    cart_items_count = CartItems.objects.filter(cart__user=user).count()
    return cart_items_count
@register.simple_tag(takes_context=True)
def whishlist_count(context):
    user = context['request'].user
    user_wishlist = Wishlist.objects.filter(user=user).first()  # Retrieve the user's wishlist
    items=WishlistItem.objects.filter(wishlist=user_wishlist)
    whishlist_count = items.count()
    return whishlist_count 