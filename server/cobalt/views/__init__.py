import json
import os
from random import shuffle, randint
from datetime import datetime, date

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.core.validators import validate_email

from cobalt import models
from cobalt.util import err_resp, OK, group_into_groups_of, divide_into_columns, json_response
from cobalt.image import handle_uploaded_image, PROFILE_IMAGE_PATH, PROFILE_IMAGE_TYPE
from bluebutter import emailtasks, imagetasks, usertasks

json_mime = "application/json"


# Create your views here.

def index(request):
    template = loader.get_template('cobalt/index.html')

    book_count = models.Book.objects.count()

    # 3 popular pieces of art that have a scene attached (i.e not a generic)
    all_media = list(models.Art.objects.all())
    all_media.extend(list(models.Book.front_page.all()))
    shuffle(all_media)

    columns = divide_into_columns(4, all_media)

    context = {
        "col_1": columns[0],
        "col_2": columns[1],
        "col_3": columns[2],
        "col_4": columns[3],
        "book_count": book_count,
    }
    return render(request, 'cobalt/index.html', context)

@csrf_exempt
def weblogin(request):
    """
    @returns: json
    """
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    resp_data = {}
    if user:
        login(request, user)

        resp_data['status'] = OK
        resp_data['username'] = user.username
        resp_data['points'] = user.currpoint
        resp_data['badges'] = "-"
        resp_data['userid'] = user.id
    else:
        resp_data['status'] = "ERR"
        resp_data['message'] = "Username/password not recognized"


    return HttpResponse(json.dumps(resp_data),
                        content_type=json_mime)

@csrf_exempt
def weblogout(request):
    logout(request)
    return redirect("/")

@csrf_exempt
def createprofile(request):
    """
    @returns: JSON
    """
    if request.method == "POST":
        resp_data = {}

        # Create
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        try:
            new_user = models.User.objects.create_user(email, username, password)
            # Log user in
            user = authenticate(username=username, password=password)
            login(request, user)

            emailtasks.send_user_verification_email.delay(new_user.id)

            resp_data = {
                "status": OK,
                "username": new_user.username,
                "profileImg": None,
            }
        except IntegrityError as e:
            if "username" in str(e):
                error_msg = "Username already exists"
            elif "email" in str(e):
                error_msg = "Email already exists"

            resp_data = err_resp(error_msg, str(e))
        except Exception as e:
            resp_data = err_resp("Unable to create user at this time",
                                 str(e))

        return HttpResponse(json.dumps(resp_data),
                            content_type=json_mime)
    else:
        return HttpResponseNotAllowed(["POST"])

@csrf_exempt
@login_required(login_url='/')
def profile(request):
    if request.method == "POST":
        # Edit User Profile
        # Because Django is stupid and doesn't deserialize PUT data, going to
        # just use POST as an easy workaround
        user = request.user

        if "fname" in request.POST:
            user.fname = request.POST['fname']

        if "lname" in request.POST:
            user.lname = request.POST['lname']
            
        if "password" in request.POST:
            password = request.POST['password']
            user.set_password(request.POST['password'])
            # Relogin
            user.save()
            update_session_auth_hash(request, user)

        if 'location' in request.POST:
            user.location = request.POST['location']

        if "bio" in request.POST:
            user.bio = request.POST['bio']

        if "website" in request.POST:
            user.website = request.POST['website']

        if "twitter" in request.POST:
            user.twitter = request.POST['twitter']

        user.save()

        # Grant user points if updated enough info
        if user.profile_sort_of_complete():
            if not user.points.filter(code='cmprf').exists():
                usertasks.add_point_to_user.delay(request.user.id, "cmprf")

        return redirect("/profile")

    template = loader.get_template('cobalt/profile.html')
    profile_image_processing = True if request.GET.get("profile-img-proc") == "True" else False
    context = {
        "profile_image_processing": profile_image_processing,
    }
    return render(request, 'cobalt/profile.html', context)

def userprofileimage(request, userid):
    """
    :returns: A user's public profile image
    """
    user = get_object_or_404(models.User, pk=userid)
    # Reutrn the profile image for user
    if user.profileimage:
        image_filename = user.profileimage.relativepath
    else:
        image_filename = "cobalt/static/cobalt/img/noprofileimage.png"
        image_filename = os.path.join(settings.BASE_DIR, image_filename)

    with open(image_filename, "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")

@login_required(login_url="/")
def profileimage(request):
    if request.method == "POST":
        request_file = request.FILES['profile-image']

        # Build profile image name
        filename, ext = os.path.splitext(request_file.name)
        filename = "profile_image_" + request.user.username + ext
        fq_filename = os.path.join(PROFILE_IMAGE_PATH, filename)

        # Save file to disk
        handle_uploaded_image(request_file, fq_filename)

        # If successful then create an Image and assign to user
        if request.user.profileimage:
            profile_image = request.user.profileimage
        else:
            profile_image = models.Image()

        profile_image.imagetype = PROFILE_IMAGE_TYPE
        profile_image.relativepath = fq_filename
        profile_image.filename = filename

        profile_image.save()

        # Assign to user
        request.user.profileimage = profile_image
        request.user.save()

        imagetasks.resize_profile_image.delay(request.user.id)

        return redirect("/profile?profile-img-proc=True")
    else:
        # Reutrn the profile image for user
        if request.user.profileimage:
            image_filename = request.user.profileimage.relativepath
        else:
            image_filename = "cobalt/static/cobalt/img/noprofileimage.png"
            image_filename = os.path.join(settings.BASE_DIR, image_filename)

        with open(image_filename, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")

def userpublicprofile(request, username):
    user = get_object_or_404(models.User, username=username)
    user_art = models.Art.objects.filter(user=user).all()

    columns = divide_into_columns(4, user_art)

    context = {
        'user': user,
        'user_art': user_art,
        "col_1": columns[0],
        "col_2": columns[1],
        "col_3": columns[2],
        "col_4": columns[3],
    }
    return render(request, 'cobalt/userpublicprofile.html', context)

def verifyemail(request):
    context = {
        "success": False,
    }
    code = request.GET.get("code")
    if code:
        user = models.User.objects.filter(emailconfirmationcode=code).first()
    
        if user:
            user.emailconfirmed = True
            user.emailconfirmationcode = None
            user.save()

            context['success'] = True

    return render(request, 'cobalt/verifyemail.html', context)

@login_required(login_url="/")
def resendemailverification(request):
    emailtasks.send_user_verification_email.delay(request.user.id)
    
    if request.user.emailconfirmed:
        resp_data = err_resp("User email is already verified")
    else:
        resp_data = {
            "status": "OK",
        }
    return HttpResponse(json.dumps(resp_data),
                        content_type=json_mime)

def terms(request):
    return render(request, 'cobalt/terms.html', {})

def privacy(request):
    return render(request, 'cobalt/privacy.html', {})

def forgotpassword(request):
    return render(request, 'cobalt/forgotpassword.html', {})

def resetpassword(request):
    if request.method != "POST":
        return redirect("/forgotpassword")
    else:
        # Try finding by user
        user = models.User.objects.filter(email=request.POST.get("identifier")).first()
        if not user:
            user = models.User.objects.filter(username=request.POST.get("identifier")).first()
        # Right now we'll just have them think the username/email was valid to prevent
        # attempts to look for real usernames/emails
        if user:
            emailtasks.send_user_password_reset_email.delay(user.id)
        else:
            print("ERROR: Someone tried to reset password with identifier that did not map to username or email: %s" % request.POST.get("identifier"))

        return render(request, 'cobalt/resetpassword.html', {})

def changepassword(request):
    if request.method == "GET":
        code = request.GET.get("code")
        if code:
            user = models.User.objects.filter(passwordresetconfirmationcode=code).first()
            if user:
                context = { "code": code, }
                return render(request, 'cobalt/changepassword.html', context)
            else:
                return redirect("/")
        else:
            return redirect("/")
    elif request.method == "POST":
        code = request.POST.get("code")
        user = models.User.objects.filter(passwordresetconfirmationcode=code).first()
        if user:
            user.set_password(request.POST['password'])
            user.passwordresetconfirmationcode = None
            user.save()
            context = { "changed": True, }
            return render(request, "cobalt/changepassword.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")

@login_required(login_url='/')
def favorites(request):
    context = {}
    return render(request, 'cobalt/favorites.html', context)

@csrf_exempt
def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            validate_email(email)
            signup = models.UserSignup(email=email)
            signup.save()
            return json_response({"status": OK})
    else:
        return HttpResponseNotAllowed('Method not allowed')

def sitemap(request):

    genres = models.Genre.objects.all()
    books = models.Book.objects.all()
    scenes = models.Scene.objects.all()
    art = models.Art.objects.all()

    context = RequestContext(request, {
        "date": str(date.today()),
        "baseurl": "https://www.foxleaf.io/",
        "genres": genres,
        "books": books,
        "scenes": scenes,
        "art": art,
    })

    template = loader.get_template('cobalt/sitemap.xml')
    return HttpResponse(template.render(context),
                        content_type="application/xml")

