from django.db import models

class Collection(models.Model):
    name = models.CharField(max_length=511)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    books = models.ManyToManyField('product.Book', through='BookCollection')

    def __str__(self):
        return self.name
    
class BookCollection(models.Model):
    book = models.ForeignKey('product.book', on_delete=models.CASCADE)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book', 'collection'], name='unique_book_collection_migration'),
        ]

    def __str__(self):
        return f"{self.book.title} - {self.collection.name}"