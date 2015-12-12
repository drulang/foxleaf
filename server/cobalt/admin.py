from django.contrib import admin
from cobalt.models import Book, Genre, Comment, Scene, SceneType, Art, ArtType, Image, ImageType, CommentStatusType, Point, User, UserSignup, UserStatusType

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    fields = ['title', 'isbn', 'summary', 'author', 'publisher', 'nsfw', 'coverurl', 'title_url', 'comments', 'genres', 'blessed']
    search_fields = ['title', 'author', 'genres__name', 'isbn']

class GenreAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'parentgenre', 'image_url']

class SceneAdmin(admin.ModelAdmin):
    fields = ['user', 'scenetype', 'book', 'title', 'text', 'startpage', 'endpage', 'nsfw', 'title_url', 'blessed']

class ArtAdmin(admin.ModelAdmin):
    fields = ['arttype', 'scene', 'image', 'user', 'title', 'nsfw', 'title_url', 'comments', 'blessed', 'devart_url']

class UserAdmin(admin.ModelAdmin):
    fields = [
        'username',
        'password',
        'userstatustyp',
        'fname',
        'lname',
        'email',
        'isfake',
        'devart_profile_url',
        'thefirst',
        'datelaststatustypchanged',
    ]


admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Comment)
admin.site.register(CommentStatusType)
admin.site.register(Scene, SceneAdmin)
admin.site.register(SceneType)
admin.site.register(Art, ArtAdmin)
admin.site.register(ArtType)
admin.site.register(Image)
admin.site.register(ImageType)
admin.site.register(Point)
admin.site.register(User, UserAdmin)
admin.site.register(UserSignup)
admin.site.register(UserStatusType)
