from decimal import Decimal
from django.db import models
from cart.models import Cart, CartItem
from product.models import Book

class CartSession:
    def __init__(self, request):
        self.session = request.session
        self.user = request.user

        if self.user.is_authenticated:
            self.use_db = True
            # Get or create cart for this user
            self.db_cart, created = Cart.objects.get_or_create(user=self.user)

            # If we just created a cart and there's a session cart, migrate items
            if created and 'cart_session' in self.session:
                self._migrate_session_to_db()
        else:
            # Use session cart for anonymous users
            self.use_db = False
            cart = self.session.get('cart_session')

            if not cart:
                cart = self.session['cart_session'] = {}

            self.cart = cart

    def _migrate_session_to_db(self):
        session_cart = self.session.get('cart_session')
        if not session_cart:
            return

        for product_id, item, in session_cart.items():
            try:
                product = Book.objects.get(pk=product_id)
                quantity = min(item["quantity"], product.stock)

                if quantity > 0:
                    CartItem.objects.create(cart=self.db_cart, book=product, quantity=quantity)
            except Exception:
                pass

    def add(self, product: Book, quantity=1):

        if product.stock < quantity or quantity < 1:
            return False

        if self.use_db:
            existing_item = CartItem.objects.filter(cart=self.db_cart, book=product).first()

            if existing_item:
                # Update quantity if already in cart
                new_quantity = existing_item.quantity + quantity
                if new_quantity > product.stock:
                    return False

                existing_item.quantity = new_quantity
                existing_item.save()
            else:
                # Add new item to cart
                CartItem.objects.create(
                    cart=self.db_cart,
                    book=product,
                    quantity=quantity
                )

            self.db_cart.save()  # Update timestamp
            return True
        else:
            product_id = str(product.id)

            if product_id not in self.cart:
                author_names = ""
                if product.authors.exists():
                    authors = product.authors.all()
                    author_names = ", ".join([str(author) for author in authors])

                # Calculate discount
                final_price = product.price
                if product.discount > 0:
                    # Calculate discounted price
                    discount_amount = (product.price * product.discount) / Decimal('100.0')
                    final_price = product.price - discount_amount

                # Add new product to cart with essential data
                self.cart[product_id] = {
                    'title': product.title,
                    'quantity': quantity,
                    'price': str(product.price),
                    'final_price': str(final_price),
                    'discount': str(product.discount),
                    'cover_img': str(product.cover_img) if product.cover_img else '',
                    'authors': author_names,
                    'publisher': product.publisher.name if product.publisher else 'Unknown',
                    'slug': product.slug,
                }
            else:
                # Update quantity if product already in cart
                new_quantity = self.cart[product_id]['quantity'] + quantity
                if new_quantity > product.stock:
                    return False

                self.cart[product_id]['quantity'] = new_quantity

            self.save()
            return True

    def save(self):
        self.session['cart_session'] = self.cart
        self.session.modified = True  # Mark session as modified to ensure it's saved

    def remove(self, product_id):
        product_id = str(product_id)
        if self.use_db:
            deleted, _ = CartItem.objects.filter(cart=self.db_cart, book__id=product_id).delete()
            return deleted > 0
        else:
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()
                return True

            return False

    def update_quantity(self, product_id, quantity):
        product_id = str(product_id)

        # Verify stock levels
        try:
            product = Book.objects.get(id=product_id)
            if quantity > product.stock or quantity < 1:
                return False, product

            if self.use_db:
                existing_item = CartItem.objects.filter(cart=self.db_cart, book=product).first()
                if not existing_item:
                    return False, None

                existing_item.quantity = quantity
                existing_item.save()
                self.db_cart.save()

            else:
                if product_id not in self.cart:
                    return False, None

                self.cart[product_id]['quantity'] = quantity
                self.save()
                return True, product
        except Book.DoesNotExist:
            self.remove(product_id)
            return False, None

    def get_total_price(self):
        if self.use_db:
            total = 0
            for item in self.db_cart.items.all().select_related('book'):
                total += item.book.final_price * item.quantity
            return total

        else:
            return sum(float(item['final_price']) * item['quantity'] for item in self.cart.values())

    def get_item_count(self):
        if self.use_db:
            return CartItem.objects.filter(cart=self.db_cart).aggregate(
                total=models.Sum('quantity'))['total'] or 0
        else:
            return sum(item['quantity'] for item in self.cart.values())

    def get_item_quantity(self, product_id):
        product_id = str(product_id)
        if self.use_db:
            item = CartItem.objects.filter(cart=self.db_cart, book__id=product_id).first()
            if item:
                return item.quantity
        else:
            if product_id in self.cart:
                return self.cart[product_id]["quantity"]

        return 0

    def clear(self):
        if self.use_db:
            self.db_cart.items.all().delete()
        else:
            self.cart = {}
            self.save()

    def __iter__(self):
        if self.use_db:
            items = self.db_cart.items.all()

            for item in items:
                yield item
        else:
            product_ids = self.cart.keys()

            for product_id in product_ids:
                yield self.cart[product_id]

    def get_subtotal(self, product_id):
        product_id = str(product_id)
        if self.use_db:
            item = CartItem.objects.filter(cart=self.db_cart, book__id=product_id).select_related('book').first()
            if item:
                return item.book.final_price * item.quantity

        else:
            if product_id not in self.cart:
                return 0

            item = self.cart[str(product_id)]
            return float(item['final_price']) * item['quantity']