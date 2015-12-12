from django.db.models import Model, ForeignKey, OneToOneField, ManyToManyField,\
     CharField, EmailField, DateTimeField, IntegerField, BooleanField,\
     URLField, Manager
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField

from cobalt.util import random_string, string_to_url
from cobalt.counts import view_count_for_book_id, view_count_for_scene_id, view_count_for_art_id

# Common Lengths of fields
L5 = 5
L45 = 45
L100 = 100
L200 = 200
L300 = 300
L500 = 500

EMAIL_CONFIRMATION_CODE_LENGTH = 70
PASSWORD_RESET_CONFIRMATION_CODE_LENGTH = 99


def scale_stat(number):
    if number < 50:
        return number * 4
    elif  number < 100:
        return  number * 3
    elif number < 300:
        return number * 1.5
    elif number < 500:
        return number * 1.2
    else:
        return number
    

##
# Entity Type Models
##

class UserType(Model):
    usertypcd = CharField(max_length=L5, null=False, db_index=True, primary_key=True)
    name = CharField(max_length=L45, null=False)
    description = CharField(max_length=L100, null=True)
    datelastmaint = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserStatusType(Model):
    statustypcd = CharField(max_length=L5, null=False, db_index=True, primary_key=True)
    name = CharField(max_length=L45, null=False)
    description = CharField(max_length=L100, null=True)
    datelastmaint = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ArtType(Model):
    arttypcd = CharField(max_length=L5, null=False, db_index=True, primary_key=True)
    name = CharField(max_length=L45, null=False)
    description = CharField(max_length=L100, null=True)
    datelastmaint = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ImageType(Model):
    imagetypcd = CharField(max_length=L5, null=False, db_index=True, primary_key=True)
    name = CharField(max_length=L45, null=False)
    description = CharField(max_length=L100, null=True)
    datelastmaint = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class CommentStatusType(Model):
    commentstatustypcd = CharField(max_length=L5, null=False, db_index=True, primary_key=True)
    name = CharField(max_length=L45, null=False)
    description = CharField(max_length=L100, null=True)
    datelastmaint = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SceneType(Model):
    scenetypcd = CharField(max_length=L5, null=False, db_index=True, primary_key=True) 
    name = CharField(max_length=L45, null=False)
    description = CharField(max_length=L100, null=True)
    datelastmaint = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class RelationshipType(Model):
    relationshiptypcd = CharField(max_length=L5, null=False, db_index=True, primary_key=True) 
    name = CharField(max_length=L45, null=False)
    description = CharField(max_length=L100, null=True)
    datelastmaint = DateTimeField(auto_now=True)

##
# Primary Models
##
class Image(Model):
    # Foreign Keys
    imagetype = ForeignKey(ImageType, null=False)

    # Fields
    relativepath = CharField(max_length=L500, null=False)
    filename = CharField(max_length=L100, null=False)
    datelastmaint = DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename

class UserManager(BaseUserManager):

    def create_user(self, email, username, password, **kwargs):
        user = self.model(**kwargs)
        user.email = email
        user.username = username
        user.set_password(password)
        user.datelaststatustypchanged = timezone.now()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        email = username + "@djangoadmin.ex"
        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.save(using=self._db)
        return user 

    def set_user_email_confirmation_code(self, userid):
        """
        This will create a new email verification code for the user
        and will set their emailconfirmed = False
        """
        user = self.filter(id=userid).first()

        if not user:
            raise ValueError("Unable to find user with userid: %s" % userid)
        code = random_string(EMAIL_CONFIRMATION_CODE_LENGTH)
        user.emailconfirmationcode = code
        user.emailconfirmed = False
        user.save()
        return code

    def set_user_password_reset_confirmation_code(self, userid):
        """
        Sets user's password reset confirmation code
        """
        user = self.filter(id=userid).first()

        if not user:
            raise ValueError("Unable to find user with userid: %s" % userid)
        code = random_string(PASSWORD_RESET_CONFIRMATION_CODE_LENGTH)
        user.passwordresetconfirmationcode = code
        user.save()
        return code

class User(AbstractBaseUser, PermissionsMixin):
    # Foreign Keys
    usertype = ForeignKey(UserType, null=False, default='stnd')
    userstatustyp = ForeignKey(UserStatusType, null=False, default='appem')
    profileimage = OneToOneField(Image, null=True, blank=True)
    followingbooks = ManyToManyField('Book', related_name="user_following_book", blank=True)
    points = ManyToManyField('Point', through='UserPoint', related_name='user_points', blank=True)

    # Favorites
    bookfavorites = ManyToManyField('Book', related_name="user_book_favorites", blank=True)
    artfavorites = ManyToManyField('Art', related_name = "user_art_favorites", blank=True)
    scenefavorites = ManyToManyField('Scene', related_name = "user_scene_favorites", blank=True)

    # Fields
    username = CharField(max_length=L45, null=False, blank=False, unique=True)
    email = EmailField(max_length=L200, null=False, blank=False, unique=True, db_index=True)
    fname = CharField(max_length=L100, null=True, blank=True)
    mname = CharField(max_length=L100, null=True, blank=True)
    lname = CharField(max_length=L100, null=True, blank=True)
    isfake = BooleanField(default=False)

    # Deviant Art
    devart_profile_url = CharField(max_length=L200, null=True, blank=False, unique=True)

    # Needed for DjanoAdmin
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    is_blocked = BooleanField(default=False)

    betauser = BooleanField(default=True, null=False) # When this goes out of beta just set default=False
    thefirst = BooleanField(default=False, null=False) # Special flag for early adopters
    currpoint = IntegerField(default=0, null=False)
    location = CharField(max_length=L200, null=True, blank=True)
    website = URLField(null=True, blank=True)
    bio = CharField(max_length=2000, blank=True)
    twitter = CharField(max_length=200, blank=True)
    emailconfirmed = BooleanField(null=False, default=False)
    emailconfirmationcode = CharField(max_length=100, null=True, unique=True, blank=True)
    passwordresetconfirmationcode = CharField(max_length=100, null=True, unique=True, blank=True)
    datecreated = DateTimeField(auto_now_add=True)
    datelaststatustypchanged = DateTimeField()
    datelastlogout = DateTimeField(null=True, blank=True)
    datelastmaint = DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    def get_short_name(self):
        return self.username

    def profile_sort_of_complete(self):
        count = 0
        if self.fname:
            count += 1
        if self.lname:
            count += 1
        if self.location:
            count += 1
        if self.website:
            count += 1
        if self.bio:
            count += 2
        if self.twitter:
            count += 1

        return count >= 5

class UserPoint(Model):
    point = ForeignKey('Point', unique=False)
    user = ForeignKey(User, unique=False)

class UserRelationship(Model):
    # ForeignKey
    user = ForeignKey(User, null=False)

    # Fields
    otheruser = OneToOneField(User, related_name="otheruser", null=False)
    datelastmaint = DateTimeField(auto_now=True)

class CommentManager(Manager):

    def get_queryset(self):
        return super().get_queryset()

    def replies_to_comment(self, comment):
        return self.get_queryset().filter(commentreply=comment)

class VoteType(Model):
    votetypcd = CharField(max_length=L5, null=False, db_index=True, primary_key=True)
    name = CharField(max_length=L45, null=False)
    description = CharField(max_length=L100, null=True)
    datelastmaint = DateTimeField(auto_now=True)

class CommentVote(Model):
    comment = ForeignKey('Comment')
    user = ForeignKey(User)
    votetype = ForeignKey(VoteType)
    datelastmaint = DateTimeField(auto_now=True)

class Comment(Model):
    # ForeignKey
    commentstatustype = ForeignKey(CommentStatusType, null=False)
    user = ForeignKey(User, null=False)
    commentreply = ForeignKey('Comment', related_name='commentreply_comment', null=True, blank=True)
    uservotes = ManyToManyField('User', through='CommentVote', related_name='user_comment_votes')
    
    # Fields
    comment = CharField(max_length=1500, null=False, blank=False)
    datecreated = DateTimeField(auto_now_add=True)
    datedeleted = DateTimeField(null=True, blank=True) 
    datedisabled = DateTimeField(null=True, blank=True)
    datelastmaint = DateTimeField(auto_now=True)

    objects = CommentManager()


    @property
    def replies(self):
        return Comment.objects.replies_to_comment(self)

    @property
    def upvotecnt(self):
        """
        :returns: Number of upvotes
        """
        upvotes = CommentVote.objects.filter(
            comment_id=self.id
        ).filter(
           votetype_id="upvt" 
        ).count()

        downvotes = CommentVote.objects.filter(
            comment_id=self.id
        ).filter(
           votetype_id="dwnvt" 
        ).count()

        return upvotes - downvotes

    def __str__(self):
        return "%s / %s" % (self.user.username, self.comment[0: 100])

    def user_upvote(self, user_id):
        return True

class Genre(Model):
    # ForeignKey
    parentgenre = ForeignKey('Genre', null=True, blank=True)

    # Fields
    name = CharField(max_length=L100, null=False, blank=False)
    description = CharField(max_length=L200, null=True, blank=True)
    datelastmaint = DateTimeField(auto_now=True)
    image_url = CharField(max_length=L200,null=True, blank=True)

    def __str__(self):
        return self.name

class BooksForFrontPage(Manager):
    def get_queryset(self):
        return super(BooksForFrontPage, self)\
                .get_queryset()\
                .filter(blessed=True)

class BookManager(Manager):
    def get_queryset(self):
        return super().get_queryset()

class Book(Model):
    # Foreign Keys
    genres = ManyToManyField(Genre)
    comments = ManyToManyField(Comment, blank=True)

    # Fields
    isbn = CharField(max_length=L100, unique=True)
    title = CharField(max_length=L200, null=False, blank=False, db_index=True)
    title_url = CharField(max_length=L200, null=False, blank=False, db_index=True)
    summary = CharField(max_length=3000, null=False, blank=False)
    author = CharField(max_length=L200, null=False, blank=False)
    publisher = CharField(max_length=L200)
    nsfw = BooleanField(default=False, null=False)
    coverurl = CharField(max_length=L500, null=True)
    datecreated = DateTimeField(auto_now_add=True)
    datelastmaint = DateTimeField(auto_now=True)
    blessed = BooleanField(null=False, default=False)
    search_index = VectorField()

    # Calculated Properties
    @property
    def dict(self):
        # TODO: User serializer
        return {
            "title": self.title,
            "title_url": self.title_url,
            "summary": self.summary,
            "short_summary": self.short_summary,
            "author": self.author,
            "publisher": self.publisher,
            "nsfw": self.nsfw,
            "coverurl": self.coverurl,
        }

    @property
    def short_summary(self):
        return self.summary[0:300]

    @property
    def url(self):
        prefix = "book/"
        if prefix in self.title_url:
            return self.title_url
        else:
            return "book/" + self.title_url

    @property
    def favorite_cnt(self):
        cnt = self.user_book_favorites.count()
        return scale_stat(cnt)

    @property
    def comment_cnt(self):
        return self.comments.count()

    @property
    def view_count(self):
        return view_count_for_book_id(self.id)

    # Managers
    objects = SearchManager(
        fields = ('title', 'author', 'isbn'),
        search_field = 'search_index',
        auto_update_search_field = True
    )
    front_page = BooksForFrontPage()

    def __str__(self):
        return self.title

class ScenesNeedingAttentionManager(Manager):
    def get_queryset(self):
        #TODO: This will need some relevancy 
        return super(ScenesNeedingAttentionManager, self)\
                .get_queryset()

class SceneManager(Manager):
    def get_queryset(self):
        return super(SceneManager, self).get_queryset()

class Scene(Model):
    # Foreign Keys
    user = ForeignKey(User)
    scenetype = ForeignKey(SceneType, null=False)
    book = ForeignKey(Book, null=False, related_name="scene")
    comments = ManyToManyField(Comment)
    topart = ForeignKey('Art', null=True, blank=True, related_name='topart')

    # Fields
    title = CharField(max_length=60, null=False)
    title_url = CharField(max_length=60, null=False, db_index=True)
    text = CharField(max_length=600)
    startpage = IntegerField(null=True, blank=True)
    endpage = IntegerField(null=True, blank=True)
    nsfw = BooleanField(default=False, null=False)
    datecreated = DateTimeField(auto_now_add=True)
    datelastmaint = DateTimeField(auto_now=True)
    blessed = BooleanField(null=False, default=False)
    search_index = VectorField()

    # Managers
    needing_attention = ScenesNeedingAttentionManager()
    objects = SearchManager(
        fields = ('title'),
        search_field = 'search_index',
        auto_update_search_field = True
    )

    @property
    def favorite_cnt(self):
        cnt = self.user_scene_favorites.count()
        return scale_stat(cnt)

    @property
    def comment_cnt(self):
        return self.comments.count()

    @property
    def view_count(self):
        return view_count_for_scene_id(self.id)

    @property
    def dict(self):
        return {
           "id": self.id,
           "title": self.title,
           "title_url": self.title_url,
           "text": self.text,
           "startpage": self.startpage,
           "endpage": self.endpage,
           "nsfw": self.nsfw,
           "scenetypcd": self.scenetype.scenetypcd,
        }

    def __str__(self):
        return "%s : %s" % (self.title, self.book.title)

class Art(Model):
    # Foreign Keys
    arttype = ForeignKey(ArtType, null=False)
    scene = ForeignKey(Scene, null=True, related_name='art', blank=True)
    book = ForeignKey(Book, null=False, related_name='book')
    image = ForeignKey(Image, null=False)
    user = ForeignKey(User, null=False)
    comments = ManyToManyField(Comment, blank=True)

    # Fields
    title = CharField(max_length=L100, null=False)
    title_url = CharField(max_length=L100, null=False, db_index=True)
    devart_url = CharField(max_length=L200, null=True, blank=True, unique=True)
    description = CharField(max_length=L200, null=True) 
    nsfw = BooleanField(default=False, null=False)
    datecreated = DateTimeField(auto_now_add=True)
    datedeleted = DateTimeField(null=True)
    datedisabled = DateTimeField(null=True)
    datelastmaint = DateTimeField(auto_now = True)
    blessed = BooleanField(null=False, default=False)
    search_index = VectorField()

    @property
    def favorite_cnt(self):
        cnt = self.user_art_favorites.count()
        return scale_stat(cnt)

    @property
    def comment_cnt(self):
        return self.comments.count()

    @property
    def view_count(self):
        return view_count_for_art_id(self.id)

    def __str__(self):
        if self.scene:
            return "%s / %s" % (self.title, self.scene.book.title)
        else:
            return "%s / No Scene" % (self.title)

    objects = SearchManager(
        fields = ('title',),
        search_field = 'search_index',
        auto_update_search_field = True
    )

class Notification(Model):
    #TODO: Implement
    pass

class Point(Model):
    code = CharField(max_length=L5, null=False, db_index=True)
    name = CharField(max_length=L45, null=False)
    value = IntegerField(null=False)
    description = CharField(max_length=L100, null=True)
    datelastmaint = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserSignup(Model):
    email = EmailField(max_length=L300, null=False, blank=False, unique=True)
    datesignup = DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

