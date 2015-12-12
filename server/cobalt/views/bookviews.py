import json
import os

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, Http404, HttpResponseForbidden
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.utils import timezone

from cobalt import models
from cobalt import search
from cobalt.util import err_resp, OK, group_into_groups_of, json_response, string_to_url, random_string
from cobalt.counts import increment_view_count_for_art_id, increment_view_count_for_book_id, increment_view_count_for_scene_id
from cobalt.image import handle_uploaded_image, ART_IMAGE_PATH, ART_IMAGE_TYPE, image_type_valid, MAX_FILE_SIZE
from bluebutter import usertasks

json_mime = "application/json"

# Create your views here.

@csrf_exempt
def book(request, booktitle):
    # Data
    book = models.Book.objects.filter(title_url=booktitle).first()
    scenes = book.scene.exclude(
        scenetype__scenetypcd="char"
    ).exclude(
        scenetype__scenetypcd="misc"
    ).exclude(
        scenetype__scenetypcd="map"
    ).all()
    characters = book.scene.filter(scenetype__scenetypcd="char").all()
    maps = book.scene.filter(scenetype__scenetypcd="map").all()

    # Art that doesnt really belong to a particular scene
    general_art = models.Art.objects.filter(
        scene=None,
        book=book,
    ).all()

    # Top Level Comments
    book_comments = book.comments.filter(
        commentreply__isnull=True
    ).all()

    # Increment book counter
    try:
        increment_view_count_for_book_id(book.id)
    except Exception as e:
        print("Unable to increment count for bookid: %s" % book.id)
        print("Err: %s" % e)

    context = {
       "book": book,
       "scenes": scenes,
       "maps": maps,
       "characters": characters,
       "general_art": general_art,
       "book_comments": book_comments,
    }
    return render(request, 'cobalt/book.html', context)

def booksearch(request, q=None):
    q = request.GET.get("q")
    if not q:
        resp_data = err_resp("Please pass q")
    else:
        results = [book.dict for book in search.booksearch(q)]
        resp_data = {
            "status": OK,
            "results": results,
        }

    return HttpResponse(json.dumps(resp_data),
                        content_type=json_mime)

@csrf_exempt
def scene(request, booktitle):
    if request.method == "POST":
        book = models.Book.objects.filter(title_url=booktitle).first()

        title = request.POST['title'].strip()
        startpage = request.POST['startPage'].strip()
        endpage = request.POST['endPage'].strip()
        text = request.POST['text'].strip()
        nsfw = True if request.POST["nsfw"] == 'true' else False
        scene_type = get_object_or_404(models.SceneType, scenetypcd=request.POST['sceneType'])
        if bool(startpage) != bool(endpage):
            raise ValueError("If one page is passed so must the other")
        else:
            if startpage == "":
                startpage = None
            else:
                startpage = int(startpage)
            if endpage == "":
                endpage = None
            else:
                endpage = int(endpage)

        # Validate
        # Title required for all
        if not title:
            raise ValueError("Title cannot be null or empty")

        if scene_type.scenetypcd == "gnrc":
            if not text:
                raise ValueError("Text is required")
            elif not startpage:
                raise ValueError("StartPage is required")
            elif not endpage:
                raise ValueError("EndPage is required")
            
        # Since other scene types might have start/end pages check 
        if startpage and endpage and (startpage > endpage):
            raise ValueError("Start page must come before end page")

        new_scene = models.Scene(
            user=request.user,
            book=book,
            scenetype=scene_type,
            title=title,
            title_url=string_to_url(title),
            startpage=startpage,
            endpage=endpage,
            text=text,
            nsfw=nsfw,
        )
        new_scene.save()

        # Give user some points
        usertasks.add_point_to_user.delay(request.user.id, "adscn")

        new_scene_url = request.path + "/" + new_scene.title_url
        resp_data = {
            "status": OK,
            "newSceneUrl": new_scene_url,
            "sceneid": new_scene.id,
        }
        return json_response(resp_data)

    if request.method == "GET" and request.META.get("CONTENT_TYPE") == "application/json":
        book = models.Book.objects.filter(title_url=booktitle).first()
        if not book:
            resp_data = err_resp("Book not found")
        else:
            scenes = []
            scenetypcd = request.GET.get("scenetypcd")
            book_scenes = book.scene.filter(scenetype_id=scenetypcd).all()
            for scene in book_scenes:
                scenes.append(scene.dict)

            resp_data = { 
                "scenes": scenes, 
                "status": OK,
            }

        return json_response(resp_data)

    # Default
    return HttpResponse("Scene Page")

@csrf_exempt
def specificscene(request, booktitle, scenetitle):
    scene = models.Scene.objects.filter(
        title_url=scenetitle
    ).filter(
        book__title_url=booktitle
    ).select_related(
        'book'
    ).first()

    if not scene:
        raise Http404("Scene not found")

    # Increment book counter
    try:
        increment_view_count_for_scene_id(scene.id)
    except Exception as e:
        print("Unable to increment count for sceneid: %s" % scene.id)
        print("Err: %s" % e)

    # Break art into groups
    scene_col_0 = []
    scene_col_1 = []
    scene_col_2 = []

    for idx, art in enumerate(scene.art.all()):
        col = idx % 3
        if col == 0:
            scene_col_0.append(art)
        elif col == 1:
            scene_col_1.append(art)
        else:
            scene_col_2.append(art)

    context = {
        "book": scene.book,
        "scene": scene,
        "scene_col_0": scene_col_0,
        "scene_col_1": scene_col_1,
        "scene_col_2": scene_col_2,
    }
    return render(request, 'cobalt/scene.html', context)

def scenetopart(request, scenetitle):
    scene = models.Scene.objects.filter(title_url=scenetitle).first()
    if not scene:
        raise Http404("Scene not found")

    # Just grab a random art for now
    try:
        art = scene.art.order_by('?')[0]
        request = artimage(request, art.title_url + "-" + str(art.id))
        return request
    except:
        return redirect('/static/cobalt/img/nophoto.jpg')

@csrf_exempt
def art(request, booktitle):
    if request.method == "POST":
        book = models.Book.objects.filter(title_url=booktitle).first()
        if not book:
            raise ValueError("Unable to find book with title: %s" % booktitle)
        request_file = request.FILES['art-image']
        art_title = request.POST.get("artTitle", "").strip()
        # Validate data
        if not image_type_valid(request_file.content_type):
            raise ValueError("Unsupported content type")
        elif len(art_title) == 0:
            raise ValueError("Title cannot be empty")
        elif request_file.size > MAX_FILE_SIZE:
            raise ValueError("File cannot be greater than 25MB")

        # Create art
        title_url = string_to_url(request.POST['artTitle'])
        filename, ext = os.path.splitext(request_file.name)
        for _ in range(50):
            # Try 50 times to find a filename
            filename = "art_image__" + random_string(length=80) + ext
            fq_filename = os.path.join(ART_IMAGE_PATH, filename)

            if os.path.exists(fq_filename):
                if _ == 49:
                    raise ValueError("Error saving image")
                else:
                    continue
            else:
                break

        # Save file to disk
        handle_uploaded_image(request_file, fq_filename)

        # If successful then create an Image and assign to user
        art_image = models.Image()
        art_image.imagetype = ART_IMAGE_TYPE
        art_image.relativepath = fq_filename
        art_image.filename = filename
        art_image.save()

        # Create Art model
        art = models.Art()
        art.user = request.user
        art.arttype_id = request.POST['artType']
        art.scene_id = request.POST.get("sceneid")
        art.book = book
        art.image = art_image
        art.title = art_title
        art.title_url = title_url
        art.description = request.POST['artText']
        art.nsfw = request.POST.get('nsfw', "f")[0]
        art.save() 

        #
        # TODO: Need to resize and standardize the iamge with a job
        #

        usertasks.add_point_to_user.delay(request.user.id, "adart")

        art_url = "/book/" + book.title_url + "/art/" + art.title_url;
        data = {
           "status": OK,
           "artURL": art_url,
        }
        return json_response(data)
    else:
        return HttpResponse("Art Page")

@csrf_exempt
def specificart(request, booktitle, arttitle):
    art = models.Art.objects.filter(
        title_url=arttitle
    ).filter(
        book__title_url=booktitle,
    ).select_related(
        'book'
    ).first()
    # Find top level comments, the template recursively displays all replies
    art_comments = art.comments.filter(
            commentreply__isnull=True
    ).all()

    more_by_user = models.Art.objects.filter(
        user=art.user
    ).exclude(
        id=art.id
    )[0:2]

    context = {
        "book": art.book,
        "scene": art.scene,
        "art": art,
        "art_comments": art_comments,
        "request_userid": request.user.id,
        "more_by_user": more_by_user,
    }
    return render(request, 'cobalt/art.html', context)

def artimage(request, arttitle):
    title_parts = arttitle.split("-")
    if title_parts:
        artid = title_parts[-1]
    else:
        artid = None

    if artid:
        art = models.Art.objects.filter(id=artid).first()
    else:
        art = None

    if art:
        try:
            increment_view_count_for_art_id(art.id)
        except Exception as e:
            #TODO: Log
            print("Unable to increment count for artid: %s" % art.id)
            print("Err: %s" % str(e))

        with open(art.image.relativepath, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    # Default
    return redirect('/static/cobalt/img/nophoto.jpg')

@csrf_exempt
def artcomment(request, artid):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    elif request.method == "POST":
        comment_text = request.POST.get("comment") 

        if not comment_text:
            raise ValueError("Comment cannot be empty")

        art = get_object_or_404(models.Art, pk=artid)

        # Create the comment 
        comment = models.Comment()
        comment.user = request.user
        comment.comment = comment_text
        comment.commentstatustype_id = "good"
        comment.save()

        # Assign comment to art

        art.comments.add(comment)
        art.save()

        context = {
            "comment": comment,
        }

        return render(request, 'cobalt/comment.html', context)
    else:
        # Return top 100 comments for art
        return HttpResponse("Art Comment")

@csrf_exempt
def commentreply(request, commentid):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    elif request.method != "POST":
        return HttpResponseNotAllowed("Method not allowed")
 
    comment_text = request.POST.get("comment") 
    if not comment_text:
        raise ValueError("Comment cannot be empty")

    comment = get_object_or_404(models.Comment, pk=commentid)

    # Create the comment 
    new_comment = models.Comment()
    new_comment.user = request.user
    new_comment.commentreply = comment
    new_comment.comment = comment_text
    new_comment.commentstatustype_id = "good"
    new_comment.save()

    context = {
        "comment": new_comment,
    }

    return render(request, 'cobalt/comment.html', context)

@csrf_exempt
def artcommentedit(request, commentid):
    if not request.user.is_authenticated():
        resp_data = {
            "status": "ERR",
            "message": "User not logged in",
        }
        return json_response(resp_data)
    elif request.method != "POST":
        return HttpResponseNotAllowed("Method not allowed")

    comment = get_object_or_404(models.Comment, pk=commentid)

    if comment.user != request.user:
        raise HttpResponseForbidden("User is not associated with comment")

    comment_text = request.POST.get("comment") 
    if not comment_text:
        raise ValueError("Comment cannot be empty")

    comment.comment = comment_text
    comment.save()

    return json_response({"status": "OK"})

@csrf_exempt
def comment(request, commentid):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    elif request.method != "DELETE":
        return HttpResponseNotAllowed("Method not allowed")

    comment = get_object_or_404(models.Comment, pk=commentid)

    if comment.user != request.user:
        raise HttpResponseForbidden("User is not associated with comment")

    comment.datedeleted = timezone.now()
    comment.save()

    return json_response({"status": "OK"})

@csrf_exempt
def commentvote(request, commentid):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    elif request.method != "POST":
        return HttpResponseNotAllowed("Method not allowed")

    comment = get_object_or_404(models.Comment, pk=commentid)

    # See if user has commented on art already
    vote = models.CommentVote.objects.filter(
        user_id=request.user.id
    ).filter(
        comment_id=comment.id
    ).first()

    if vote is None:
        vote = models.CommentVote()
        vote.user = request.user
        vote.comment = comment

    vote.votetype_id = request.POST['upvotetype']
    vote.save()

    return json_response({"status": "OK"})

@csrf_exempt
def bookcomment(request, bookid):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    if request.method == "POST":
        book = get_object_or_404(models.Book, pk=bookid)

        comment_text = request.POST.get("comment") 
        if not comment_text:
            raise ValueError("Comment cannot be empty")

        # Create the comment 
        comment = models.Comment()
        comment.user = request.user
        comment.comment = comment_text
        comment.commentstatustype_id = "good"
        comment.save()

        # Assign comment to art

        book.comments.add(comment)
        book.save()

        context = {
            "comment": comment,
        }

        return render(request, 'cobalt/comment.html', context)
    else:
        # Return top 100 comments for art
        return HttpResponse("Art Comment")

@csrf_exempt
def scenecomment(request, sceneid):
    pass


@csrf_exempt
def bookfavorite(request, bookid):
    """
    NOTE: Needs to be in API
    """
    # Not using login_required decorator because this is primarly used in an
    # API manner and I want a 403 returned instead of a redirect
    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    if request.method == "POST":
        book = get_object_or_404(models.Book, pk=bookid)
        request.user.bookfavorites.add(book)
        request.user.save() 
        return json_response({"status": "OK"})
    elif request.method == "DELETE":
        book = get_object_or_404(models.Book, pk=bookid)
        request.user.bookfavorites.remove(book)
        request.user.save() 
        return json_response({"status": "OK"})
    else:
        return HttpResponse("User book favorites")

@csrf_exempt
def artfavorite(request, artid):
    """
    NOTE: Needs to be in API
    """

    # Not using login_required decorator because this is primarly used in an
    # API manner and I want a 403 returned instead of a redirect
    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    if request.method == "POST":
        art = get_object_or_404(models.Art, pk=artid)
        request.user.artfavorites.add(art)
        request.user.save() 
        return json_response({"status": "OK"})
    elif request.method == "DELETE":
        art = get_object_or_404(models.Art, pk=artid)
        request.user.artfavorites.remove(art)
        request.user.save() 
        return json_response({"status": "OK"})
    else:
        return HttpResponse("User art favorites")

@csrf_exempt
def scenefavorite(request, sceneid):
    """
    NOTE: Needs to be in API
    """
    # Not using login_required decorator because this is primarly used in an
    # API manner and I want a 403 returned instead of a redirect
    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    if request.method == "POST":
        scene = get_object_or_404(models.Scene, pk=sceneid)
        request.user.scenefavorites.add(scene)
        request.user.save() 
        return json_response({"status": "OK"})
    elif request.method == "DELETE":
        scene = get_object_or_404(models.Scene, pk=sceneid)
        request.user.scenefavorites.remove(scene)
        request.user.save() 
        return json_response({"status": "OK"})
    else:
        return HttpResponse("User scene favorites")

@csrf_exempt
def alterartbyid(request, artid):
    art = get_object_or_404(models.Art, pk=artid)

    def _get():
        context = {
           'userart': art,
        }
        return render(request, 'cobalt/editart.html', context)

    def _delete():
        if art.user != request.user:
            return HttpResponseForbidden("User does not own art")
        else:
            try:
                fq_filename = os.path.join(ART_IMAGE_PATH, art.image.filename)
                os.remove(fq_filename)
            except Exception as e:
                # This is ok. There will be a batch job to remove files no longer
                # associated with anything
                print("Error deleting image file: %s" % e)
            art.delete()
            return json_response({"status": "OK"})

    def _edit():
        if art.user != request.user:
            return HttpResponseForbidden("User does not own art")

        # Update Fields
        art.arttype_id = request.POST['artType']
        
        # Check if title changed
        art_title = request.POST.get("artTitle", "").strip()
        if art_title != art.title:
            if len(art_title) == 0:
                context = {
                    "userart": art,
                    "error": "Art title cannot be empty",
                }
                return render(request, 'cobalt/editart.html', context)
            art.title = art_title
            art.title_url = string_to_url(art.title)

        # Description
        art.description = request.POST['artText']

        # NSFW
        if request.POST.get("nsfw"):
            art.nsfw = True
        else:
            art.nsfw = False

        # Image
        request_file = request.FILES.get('art-image')

        if request_file:
            if not image_type_valid(request_file.content_type):
                context = {
                    "userart": art,
                    "error": "Unsupported file type",
                }
                return render(request, 'cobalt/editart.html', context)

            # Save file to disk
            filename = art.image.filename
            fq_filename = os.path.join(ART_IMAGE_PATH, filename)
            handle_uploaded_image(request_file, fq_filename)

        art.save()
        return redirect('/art/%s' % art.id)

    if request.method == "DELETE":
        return _delete()
    elif request.method == "POST":
        return _edit()
    else:
        return _get()


@csrf_exempt
def alterscenebyid(request, sceneid):
    scene = get_object_or_404(models.Scene, pk=sceneid)

    def _get():
        context = {
           "userscene": scene,
        }
        return render(request, 'cobalt/editscene.html', context)

    def _delete():
        if scene.user != request.user:
            return HttpResponseForbidden("User does not own scene")
        else:
            scene.delete()
            return json_response({"status": "OK"})

    def _edit():
        if scene.user != request.user:
            return HttpResponseForbidden("User does not own scene")

        title = request.POST['title'].strip()
        startpage = request.POST['startPage'].strip()
        endpage = request.POST['endPage'].strip()
        text = request.POST['text'].strip()
        nsfw = True if request.POST.get("nsfw") == 'true' else False
        scene_type = get_object_or_404(models.SceneType, scenetypcd=request.POST['sceneType'])

        error = None
        if bool(startpage) != bool(endpage):
            error = "If one page is passed so must the other"
        else:
            if startpage == "":
                startpage = None
            else:
                startpage = int(startpage)
            if endpage == "":
                endpage = None
            else:
                endpage = int(endpage)

        # Validate
        # Title required for all
        if not title:
            error = "Title cannot be empty"

        if scene_type.scenetypcd == "gnrc":
            if not text:
                error = "Scene text is required"
            elif not startpage:
                error = "Scene start page is required"
            elif not endpage:
                error = "Scene end page is required"
            
        # Since other scene types might have start/end pages check 
        if startpage and endpage and (startpage > endpage):
            error = "Start page must come before end page"

        if error:
            context = {
               "userscene": scene,
               "error": error,
            }
            return render(request, 'cobalt/editscene.html', context)

        scene.title = title
        scene.title_url=string_to_url(title)
        scene.startpage = startpage
        scene.endpage = endpage
        scene.text = text
        scene.nsfw = nsfw
        scene.scenetype = scene_type
        scene.save()

        return redirect('/scene/%s' % scene.id)
    if request.method == "DELETE":
        return _delete()
    elif request.method == "POST":
        return _edit()
    else:
        return _get()
