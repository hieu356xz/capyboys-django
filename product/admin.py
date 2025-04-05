from django.contrib import admin
from django.template.defaultfilters import slugify
from unidecode import unidecode
from .models import Book, Author, Attribute, BookAttributeValue, Publisher, Genre, BookGenre, BookAuthor
from collection.models import BookCollection
from django.forms import ModelForm, ModelMultipleChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple

class BookAttributeValueInline(admin.StackedInline):
    model = BookAttributeValue
    extra = 1

    autocomplete_fields = ('attribute',)
class BookCollectionInline(admin.TabularInline):
    model = BookCollection
    extra = 1

    autocomplete_fields = ('collection',)

class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1

    autocomplete_fields = ('author',)

# Chat GPT save me from going insane
class BookAdminForm(ModelForm):
    # Add a multiple choice field for genres
    _genres = ModelMultipleChoiceField(
        label='',
        queryset=Genre.objects.all(),
        required=False,
        widget=FilteredSelectMultiple('Genre', is_stacked=False),
    )
    
    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # If editing an existing book
            # Get currently selected genres
            self.fields['_genres'].initial = Genre.objects.filter(
                bookgenre__book=self.instance
            )

    def save(self, commit=True):
        book = super().save(commit=False)
        
        if commit:
            book.save()
            self._save_genres(book)
        else:
            # Store original save_m2m method
            original_save_m2m = self.save_m2m
            
            # Create a new save_m2m that calls both the original and our custom method
            def updated_save_m2m():
                original_save_m2m()
                self._save_genres(book)
            
            # Replace the save_m2m method
            self.save_m2m = updated_save_m2m
        
        return book
    
    def _save_genres(self, book):
        """Save genre relationships for the book."""
        # Clear existing relationships
        BookGenre.objects.filter(book=book).delete()
        
        # Create new relationships
        selected_genres = self.cleaned_data.get('_genres', [])
        for genre in selected_genres:
            BookGenre.objects.create(book=book, genre=genre)

class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm

    prepopulated_fields = {"slug": ["title"]}

    def display_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])
    display_authors.short_description = "Authors"

    list_display = ('title', 'display_authors', 'publisher', 'price', 'stock', 'discount', 'publish_year', 'description')

    inlines = [BookAttributeValueInline, BookCollectionInline, BookAuthorInline]

    list_filter = ['collections', 'genres', 'publish_year', 'authors', 'publisher']
    search_fields = ['title', 'authors__name', 'publisher__name']
    autocomplete_fields = ['publisher']

    def save_model(self, request, obj, form, change):
        if 'slug' not in form.changed_data or not change:
            obj.slug = slugify(unidecode(obj.title))
        return super().save_model(request, obj, form, change)


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']

class PublisherAdmin(admin.ModelAdmin):
    search_fields = ['name']

class AttributeAdmin(admin.ModelAdmin):
    search_fields = ['attribute']

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Genre)
admin.site.register(BookAttributeValue)
