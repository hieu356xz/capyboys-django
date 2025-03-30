from product.models import Book

class Cart:
    def __init__(self, request):
        self.__session = request.session

        cart = self.__session.get('cart_session')

        if not cart:
            cart = self.__session['cart_session'] = {}

        self.cart = cart

    def add(self, product: Book, quantity=1):
        product_id = str(product.id)
        
        if product.stock < quantity:
            return False
        
        if product_id not in self.cart:
            author_names = ""
            if product.authors.exists():
                authors = product.authors.all()
                author_names = ", ".join([str(author) for author in authors])
                
            # Calculate discount
            final_price = product.price
            if product.discount > 0:
                # Calculate discounted price
                discount_amount = (product.price * product.discount) / 100.0
                final_price = product.price - discount_amount
                
            # Add new product to cart with essential data
            self.cart[product_id] = {
                'quantity': quantity,
                'price': str(product.price),
                'final_price': str(final_price),
                'discount': str(product.discount),
                'title': product.title,
                'cover_img': str(product.cover_img) if product.cover_img else '',
                'author': author_names,
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
        # self.__session['cart_session'] = self.cart
        self.__session.modified = True  # Mark session as modified to ensure it's saved
    
    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            
    def update_quantity(self, product_id, quantity):
        product_id = str(product_id)
        if product_id not in self.cart:
            return False
            
        # Verify stock levels
        try:
            product = Book.objects.get(id=product_id)
            if quantity > product.stock:
                return False
                
            self.cart[product_id]['quantity'] = quantity
            self.save()
            return True
        except Book.DoesNotExist:
            self.remove(product_id)
            return False
            
    def get_total_price(self):
        return sum(float(item['final_price']) * item['quantity'] for item in self.cart.values())
    
    def get_item_count(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear(self):
        self.cart = {}
        self.save()
        
    def __iter__(self):
        product_ids = self.cart.keys()
        
        for product_id in product_ids:
            yield self.cart[product_id]
            
    def get_subtotal(self, product_id):
        if str(product_id) not in self.cart:
            return 0
            
        item = self.cart[str(product_id)]
        return float(item['final_price']) * item['quantity']