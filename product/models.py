from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=511)
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    publish_year = models.PositiveSmallIntegerField(blank=True, null=True)
    cover_img = models.ImageField(max_length=511, upload_to='covers/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    stock = models.PositiveIntegerField(default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    authors = models.ManyToManyField('Author', through='BookAuthor')
    genres = models.ManyToManyField('Genre', through='BookGenre')
    attributes = models.ManyToManyField('Attribute', through='BookAttributeValue')
    collections = models.ManyToManyField('collection.Collection', through='collection.BookCollection')

    def __str__(self):
        return self.title
    
class Author(models.Model):
    name = models.CharField(max_length=511)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
    
class BookAuthor(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book', 'author'], name='unique_book_author_migration'),
        ]

    def __str__(self):
        return self.book.title + ' - ' + self.author.name
class Publisher(models.Model):
    name = models.CharField(max_length=511)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

class Attribute(models.Model):
    name = models.CharField(max_length=511)

    def __str__(self):
        return self.name

class BookAttributeValue(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE)
    value = models.CharField(max_length=511)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book', 'attribute'], name='unique_book_attribute_migration'),
        ]

    def __str__(self):
        return f"[{self.book.title}] {self.attribute.name}: {self.value}"

class Genre(models.Model):
    name = models.CharField(max_length=511)

    def __str__(self):
        return self.name
    
class BookGenre(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title + ' - ' + self.genre.name