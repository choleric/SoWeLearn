# -*- coding: utf-8 -*-
# Create your views here.
import json

from django.http import HttpResponse
from django.core import signals
from django.contrib import comments
from django.contrib.comments import signals
from django.utils.html import escape
from django.views.generic.edit import View
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.contrib.comments.forms import CommentForm

from mylearn.apps.baseviews import UserRelatedFormView,LoginRequriedView
from mylearn.apps.response import JsonResponse
from mylearn.apps import errcode
from .forms import TopicourseDiscussionForm
from .models import TopicourseDiscussion

class TopicourseDiscussiongView(UserRelatedFormView):
    def get(self):
        return JsonResponse(errcode.topicourseDiscussionQueryInvalid,"Invalid call")
    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        if not request.user.is_authenticated():
           return JsonResponse(errcode.topicourseDiscussionQueryInvalid,"Invalid call")

        discussion = TopicourseDiscussionForm(data)
        if not discussion.is_valid():
            return JsonResponse(errcode.topicourseDiscussionFormInvalid)

        discussion.instance.topicourseId = data.get('topicourseId', 0)
        discussion.instance.userId = request.user.pk
        if not discussion.instance.topicourseId:
            return JsonResponse(errcode.topicourseDiscussionFormInvalid)

        discussion.save()
        return JsonResponse(errcode.SUCCESS)

discussion_create=TopicourseDiscussiongView.as_view()

class TopicourseDiscussiongCommentView(LoginRequriedView):
    def get(self,request , *args, **kwargs):
        return JsonResponse(errcode.topicourseDiscussionQueryInvalid,"Invalid call")

    def post(self, request, using=None):
        """
        Post a comment, via an Ajax call.
        """
        if not request.is_ajax():
            return JsonResponse(errcode.topicourseDiscussionQueryInvalid, "Expecting Ajax call")

        # This is copied from django.contrib.comments.
        # Basically that view does too much, and doesn't offer a hook to change the rendering.
        # The request object is not passed to next_redirect for example.
        #
        # This is a separate view to integrate both features. Previously this used django-ajaxcomments
        # which is unfortunately not thread-safe (it it changes the comment view per request).


        # Fill out some initial data fields from an authenticated user, if present
        data = request.POST.copy()
        if request.user.is_authenticated():
            #TODO 如果用户已登录，用另一个名字评论，允许吧
            if not data.get('name', ''):
                data["name"] = request.user.get_full_name() or request.user.username
            if not data.get('email', ''):
                data["email"] = request.user.email
        else:
            #FIXME 直接redirect了。。。
            return JsonResponse(errcode.topicourseDiscussionQueryInvalid,
                                "Required to login.")

        # Look up the object we're trying to comment about
        ctype = data.get("content_type")
        object_pk = data.get("object_pk")
        if ctype is None or object_pk is None:
            return JsonResponse(errcode.topicourseDiscussionQueryInvalid,
                                "Missing content_type or object_pk field.")
        try:
            object_pk = long(object_pk)
            model = models.get_model(*ctype.split(".", 1))
            target = model._default_manager.using(using).get(pk=object_pk)
        except ValueError:
            return JsonResponse(errcode.topicourseDiscussionQueryInvalid,
                                "Invalid object_pk value: {0}".format(escape(object_pk)))
        except TypeError:
            return JsonResponse(errcode.topicourseDiscussionQueryInvalid,
                                "Invalid content_type value: {0}".format(escape(ctype)))
        except AttributeError:
            return JsonResponse(errcode.topicourseDiscussionQueryInvalid,
                                "The given content-type {0} does not resolve to a valid model."\
                                    .format(escape(ctype)))
        except ObjectDoesNotExist:
            return JsonResponse(errcode.topicourseDiscussionQueryInvalid,
                                "No object matching content-type {0} and object PK {1} exists."\
                                    .format(escape(ctype), escape(object_pk)))
        except (ValueError, ValidationError) as e:
            return JsonResponse(errcode.topicourseDiscussionQueryInvalid,
                                "Attempting go get content-type {0!r} and object PK {1!r} exists raised {2}"\
                                .format(escape(ctype), escape(object_pk), e.__class__.__name__))

        # Do we want to preview the comment?
        preview = "preview" in data

        # Construct the comment form
        form = comments.get_form()(target, data=data)

        # Check security information
        #if form.security_errors():
        #    return JsonResponse(errcode.topicourseDiscussionQueryInvalid,
        #                        "The comment form failed security verification: {0}".format)

        #TODO 需要确定要返回哪些信息
        resp_data = {}
        resp_data['object_id'] = object_pk

        # If there are errors or if we requested a preview show the comment
        comment = form.get_comment_object() if not form.errors else None
        if comment:
            resp_data['comment'] = comment.comment
            resp_data['name'] = comment.name
        if preview:
            resp_data['preview'] = 'preview'
            return JsonResponse(errcode.SUCCESS, resp_data)
        if form.errors:
            #把错误信息编号...
            form_err = dict(form.errors.items())
            return JsonResponse(errcode.topicourseDiscussionFormInvalid, form_err)

        # Otherwise create the comment
        comment.ip_address = request.META.get("REMOTE_ADDR", None)
        if request.user.is_authenticated():
            comment.user = request.user

        # Signal that the comment is about to be saved
        responses = signals.comment_will_be_posted.send(
            sender  = comment.__class__,
            comment = comment,
            request = request
        )

        for (receiver, response) in responses:
            if response is False:
                return JsonResponse(errcode.topicourseDiscussionQueryInvalid,
                                    "comment_will_be_posted receiver {0} killed the comment".format(receiver.__name__))

        # Save the comment and signal that it was saved
        comment.save()
        #
        signals.comment_was_posted.send(
            sender  = comment.__class__,
            comment = comment,
            request = request
        )

        return JsonResponse(errcode.SUCCESS, resp_data)

comment_create = TopicourseDiscussiongCommentView.as_view()

class TopicourseDiscussiongCommentSecurityView(LoginRequriedView):
    def get(self, request , discussion_id):
        discussion = TopicourseDiscussion.objects.get(pk=discussion_id)
        comment_form = CommentForm(discussion, {'object_pk':discussion_id, 'content_type': 'topicourse_comment.topicoursediscussion' })
        security = comment_form.generate_security_data()
        return JsonResponse(errcode.SUCCESS, security)

comment_security = TopicourseDiscussiongCommentSecurityView.as_view()