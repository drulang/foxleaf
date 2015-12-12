# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgfulltext.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(unique=True, max_length=45)),
                ('email', models.EmailField(db_index=True, unique=True, max_length=200)),
                ('fname', models.CharField(max_length=100, null=True)),
                ('mname', models.CharField(max_length=100, blank=True, null=True)),
                ('lname', models.CharField(max_length=100, null=True)),
                ('isfake', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_blocked', models.BooleanField(default=False)),
                ('betauser', models.BooleanField(default=True)),
                ('thefirst', models.BooleanField(default=False)),
                ('currpoint', models.IntegerField(default=0)),
                ('location', models.CharField(max_length=200, blank=True, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('bio', models.CharField(max_length=2000, blank=True)),
                ('twitter', models.CharField(max_length=200, blank=True)),
                ('emailconfirmed', models.BooleanField(default=False)),
                ('emailconfirmationcode', models.CharField(unique=True, max_length=100, blank=True, null=True)),
                ('passwordresetconfirmationcode', models.CharField(unique=True, max_length=100, blank=True, null=True)),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('datelaststatustypchanged', models.DateTimeField()),
                ('datelastlogout', models.DateTimeField(blank=True, null=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Art',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('title_url', models.CharField(db_index=True, max_length=100)),
                ('description', models.CharField(max_length=200, null=True)),
                ('nsfw', models.BooleanField(default=False)),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('datedeleted', models.DateTimeField(null=True)),
                ('datedisabled', models.DateTimeField(null=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
                ('blessed', models.BooleanField(default=False)),
                ('search_index', djorm_pgfulltext.fields.VectorField(db_index=True, serialize=False, default='', null=True, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArtType',
            fields=[
                ('arttypcd', models.CharField(db_index=True, serialize=False, primary_key=True, max_length=5)),
                ('name', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=100, null=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('isbn', models.CharField(unique=True, max_length=100)),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('title_url', models.CharField(db_index=True, max_length=200)),
                ('summary', models.CharField(max_length=3000)),
                ('author', models.CharField(max_length=200)),
                ('publisher', models.CharField(max_length=200)),
                ('nsfw', models.BooleanField(default=False)),
                ('coverurl', models.CharField(max_length=500, null=True)),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
                ('blessed', models.BooleanField(default=False)),
                ('search_index', djorm_pgfulltext.fields.VectorField(db_index=True, serialize=False, default='', null=True, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('comment', models.CharField(max_length=1500)),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('datedeleted', models.DateTimeField(blank=True, null=True)),
                ('datedisabled', models.DateTimeField(blank=True, null=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
                ('commentreply', models.ForeignKey(related_name='commentreply_comment', blank=True, to='cobalt.Comment', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentStatusType',
            fields=[
                ('commentstatustypcd', models.CharField(db_index=True, serialize=False, primary_key=True, max_length=5)),
                ('name', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=100, null=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommentVote',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(to='cobalt.Comment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200, blank=True, null=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
                ('image_url', models.CharField(max_length=200, blank=True, null=True)),
                ('parentgenre', models.ForeignKey(blank=True, to='cobalt.Genre', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('relativepath', models.CharField(max_length=500)),
                ('filename', models.CharField(max_length=100)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImageType',
            fields=[
                ('imagetypcd', models.CharField(db_index=True, serialize=False, primary_key=True, max_length=5)),
                ('name', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=100, null=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('code', models.CharField(db_index=True, max_length=5)),
                ('name', models.CharField(max_length=45)),
                ('value', models.IntegerField()),
                ('description', models.CharField(max_length=100, null=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelationshipType',
            fields=[
                ('relationshiptypcd', models.CharField(db_index=True, serialize=False, primary_key=True, max_length=5)),
                ('name', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=100, null=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=60)),
                ('title_url', models.CharField(db_index=True, max_length=60)),
                ('text', models.CharField(max_length=600)),
                ('startpage', models.IntegerField(blank=True, null=True)),
                ('endpage', models.IntegerField(blank=True, null=True)),
                ('nsfw', models.BooleanField(default=False)),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
                ('blessed', models.BooleanField(default=False)),
                ('search_index', djorm_pgfulltext.fields.VectorField(db_index=True, serialize=False, default='', null=True, editable=False)),
                ('book', models.ForeignKey(related_name='scene', to='cobalt.Book')),
                ('comments', models.ManyToManyField(to='cobalt.Comment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SceneType',
            fields=[
                ('scenetypcd', models.CharField(db_index=True, serialize=False, primary_key=True, max_length=5)),
                ('name', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=100, null=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserPoint',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('point', models.ForeignKey(to='cobalt.Point')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserRelationship',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
                ('otheruser', models.OneToOneField(related_name='otheruser', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserSignup',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('email', models.EmailField(unique=True, max_length=300)),
                ('datesignup', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserStatusType',
            fields=[
                ('statustypcd', models.CharField(db_index=True, serialize=False, primary_key=True, max_length=5)),
                ('name', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=100, null=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('usertypcd', models.CharField(db_index=True, serialize=False, primary_key=True, max_length=5)),
                ('name', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=100, null=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VoteType',
            fields=[
                ('votetypcd', models.CharField(db_index=True, serialize=False, primary_key=True, max_length=5)),
                ('name', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=100, null=True)),
                ('datelastmaint', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='scene',
            name='scenetype',
            field=models.ForeignKey(to='cobalt.SceneType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scene',
            name='topart',
            field=models.ForeignKey(related_name='topart', blank=True, to='cobalt.Art', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scene',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='imagetype',
            field=models.ForeignKey(to='cobalt.ImageType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commentvote',
            name='votetype',
            field=models.ForeignKey(to='cobalt.VoteType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='commentstatustype',
            field=models.ForeignKey(to='cobalt.CommentStatusType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='uservotes',
            field=models.ManyToManyField(related_name='user_comment_votes', through='cobalt.CommentVote', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='comments',
            field=models.ManyToManyField(to='cobalt.Comment', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(to='cobalt.Genre'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='art',
            name='arttype',
            field=models.ForeignKey(to='cobalt.ArtType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='art',
            name='book',
            field=models.ForeignKey(related_name='book', to='cobalt.Book'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='art',
            name='comments',
            field=models.ManyToManyField(to='cobalt.Comment', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='art',
            name='image',
            field=models.ForeignKey(to='cobalt.Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='art',
            name='scene',
            field=models.ForeignKey(related_name='art', to='cobalt.Scene', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='art',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='artfavorites',
            field=models.ManyToManyField(related_name='user_art_favorites', to='cobalt.Art'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='bookfavorites',
            field=models.ManyToManyField(related_name='user_book_favorites', to='cobalt.Book'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='followingbooks',
            field=models.ManyToManyField(related_name='user_following_book', to='cobalt.Book'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', blank=True, verbose_name='groups', to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='points',
            field=models.ManyToManyField(related_name='user_points', through='cobalt.UserPoint', to='cobalt.Point'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='profileimage',
            field=models.OneToOneField(to='cobalt.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='scenefavorites',
            field=models.ManyToManyField(related_name='user_scene_favorites', to='cobalt.Scene'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', blank=True, verbose_name='user permissions', to='auth.Permission', help_text='Specific permissions for this user.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='userstatustyp',
            field=models.ForeignKey(to='cobalt.UserStatusType', default='appem'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='usertype',
            field=models.ForeignKey(to='cobalt.UserType', default='stnd'),
            preserve_default=True,
        ),
    ]
