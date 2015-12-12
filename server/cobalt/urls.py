from django.conf.urls import patterns, url 

from cobalt import views
from cobalt.views import bookviews
from cobalt.views import exploreviews
from cobalt.views import beeradmin

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^search/', exploreviews.search, name='search'),
    # Profile
    url(r'^weblogin/', views.weblogin, name='weblogin'),
    url(r'^weblogout/', views.weblogout, name='weblogout'),
    url(r'^createprofile/', views.createprofile, name='createprofile'),
    url(r'^signup/', views.signup, name="signup"),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^profileimage/', views.profileimage, name='profileimage'),
    url(r'^userprofileimage/(?P<userid>\d+)', views.userprofileimage, name='userprofileimage'),
    url(r'^user/(?P<username>\S+)', views.userpublicprofile, name='userpublicprofile'),
    url(r'^verifyemail/', views.verifyemail, name='verifyemail'),
    url(r'^resendemailverification', views.resendemailverification, name='resendemailverification'),
    url(r'^forgotpassword', views.forgotpassword, name='forgotpassword'),
    url(r'^resetpassword', views.resetpassword, name='resetpassword'),
    url(r'^changepassword', views.changepassword, name='changepassword'),
    url(r'^favorites', views.favorites, name='favorites'),
    url(r'^sitemap.xml', views.sitemap, name='sitemap'),

    #Admin
    url(r'^beer', beeradmin.bookadmin, name='bookadmin'),

    # Art Image URL
    url(r'^artimage/(?P<arttitle>[\w-]+)', bookviews.artimage, name='artimage'),

    # Art URL
    url(r'^book/(?P<booktitle>[\w-]+)/art/(?P<arttitle>[\w-]+)', bookviews.specificart, name='art'),
    url(r'^book/(?P<booktitle>[\w-]+)/art', bookviews.art, name='art'),
    url(r'^art/(?P<artid>\d+)/favorite', bookviews.artfavorite, name='artfavorite'),
    url(r'^art/(?P<artid>\d+)/comment', bookviews.artcomment, name='artcomment'),
    url(r'^art/(?P<artid>\d+)', bookviews.alterartbyid, name='artid'),

    # Scene URL
    url(r'^book/(?P<booktitle>[\w-]+)/scene/(?P<scenetitle>[\w-]+)', bookviews.specificscene, name='scene'),
    url(r'^scene/(?P<scenetitle>[\w-]+)/topart', bookviews.scenetopart, name='scenetopart'),
    url(r'^book/(?P<booktitle>[\w-]+)/scene', bookviews.scene, name='scene'),
    url(r'^scene/(?P<sceneid>\d+)/favorite', bookviews.scenefavorite, name='scenefavorite'),
    url(r'^scene/(?P<sceneid>\d+)', bookviews.alterscenebyid, name='sceneid'),

    # Book URLs
    url(r'^book/search', bookviews.booksearch, name='booksearch'),
    url(r'^book/(?P<bookid>\d+)/comment', bookviews.bookcomment, name='bookcomment'),
    url(r'^book/(?P<bookid>\d+)/favorite', bookviews.bookfavorite, name='bookfavorite'),
    url(r'^book/(?P<booktitle>[\w-]+)', bookviews.book, name='book'),

    # Comment URLs
    url(r'^comment/(?P<commentid>\d+)/reply', bookviews.commentreply, name='commentreply'),
    url(r'^comment/(?P<commentid>\d+)/edit', bookviews.artcommentedit, name='artcommentedit'),
    url(r'^comment/(?P<commentid>\d+)/vote', bookviews.commentvote, name='comment_vote'),
    url(r'^comment/(?P<commentid>\d+)', bookviews.comment, name='comment_vote'),

    # Explore Views
    url(r'explore/books/(?P<genre_name>[\w-]+)', exploreviews.explorebooks),
    url(r'explore/books', exploreviews.explorebooks),
    url(r'explore/books', exploreviews.explorebooks),
    url(r'explore/scenes', exploreviews.explorescenes),
    url(r'explore/art', exploreviews.exploreart),

    # Misc
    url(r'terms', views.terms, name='terms'),
    url(r'privacy', views.privacy, name='privacy'),
)

