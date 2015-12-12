from django import template

from cobalt import models
register = template.Library()

@register.filter
def classname(obj):
    classname = obj.__class__.__name__
    return classname

@register.filter
def formatdate(date):
    return date.strftime("%m/%d/%Y")

@register.filter
def userlikedcomment(comment, user):
    # This is going to be so amazingly inefficent
    if user.is_anonymous():
        return False
    vote = models.CommentVote.objects.filter(user=user).filter(comment=comment).first()
    return vote and vote.votetype.votetypcd == "upvt"

@register.filter
def userdislikedcomment(comment, user):
    if user.is_anonymous():
        return False
    # This is going to be so amazingly inefficent
    vote = models.CommentVote.objects.filter(user=user).filter(comment=comment).first()
    return vote and vote.votetype.votetypcd == "dwnvt"

@register.filter
def userfavoritedbook(book, user):
    if user.is_anonymous():
        return False
    return user.bookfavorites.filter(id=book.id).exists()

@register.filter
def userfavoritedart(art, user):
    if user.is_anonymous():
        return False
    return user.artfavorites.filter(id=art.id).exists()

@register.filter
def userfavoritedscene(scene, user):
    if user.is_anonymous():
        return False
    return user.scenefavorites.filter(id=scene.id).exists()
