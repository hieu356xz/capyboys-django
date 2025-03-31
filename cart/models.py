from django.db import models
from django.contrib.auth import get_user_model
from product.models import Book
User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cart', 'book')
        
    def __str__(self):
        return f"{self.quantity}x {self.book.title}"
    
class Order(models.Model):
    ORDER_STATUS = (
        ('pending', 'Chờ xác nhận'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đã giao cho đơn vị vận chuyển'),
        ('delivered', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy'),
        ('refunded', 'Đã hoàn tiền')
    )
    
    PAYMENT_METHOD = (
        ('cod', 'Thanh toán khi nhận hàng'),
        ('bank_transfer', 'Chuyển khoản ngân hàng'),
        ('credit_card', 'Thẻ tín dụng/Ghi nợ'),
        ('e_wallet', 'Ví điện tử')
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    phone = models.CharField(max_length=20)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    payment_status = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255, blank=True)

    total_price = models.DecimalField(max_digits=15, decimal_places=2)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"
    
    @property
    def is_paid(self):
        return self.payment_status
    
    @property
    def full_name(self):
        return f"{self.user.last_name} {self.user.first_name}"
    
    @property
    def total_item(self):
        return self.items.all().aggregate(
                total=models.Sum('quantity'))['total'] or 0
    
    def save(self, *args, **kwargs):
        if not self.final_price:
            self.final_price = sum([item.subtotal for item in self.items.all()])
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2)  # Original price
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=15, decimal_places=2)  # Price after discount
    
    def __str__(self):
        return f"{self.quantity}x {self.book_title}"
    
    @property
    def subtotal(self):
        return self.quantity * self.final_price
    
    def save(self, *args, **kwargs):
        if not self.final_price and self.price and self.discount:
            discount_amount = (self.price * self.discount) / 100.0
            self.final_price = self.price - discount_amount
        super().save(*args, **kwargs)