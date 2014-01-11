import logging, os
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django_youtube.models import video_created, Video
from django_youtube.api import Api, ApiError, AccessControl
from gdata.service import RequestError

from .forms import YoutubeMetadataForm


from mylearn import settings
from mylearn.apps import errcode
from mylearn.apps import JsonResponse
from mylearn.apps.baseviews import UserRelatedFormView, LoginRequriedView

logger = logging.getLogger(__name__)

class UploadVideoMetadata(UserRelatedFormView):
    form_class = YoutubeMetadataForm

    def post(self, request, *args, **kwargs):
        # The request should contain the form data including the access token
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if not form.is_valid():
            err = errcode.VideoMetadataError
            for field, v in form.errors.iteritems() :
                if 1 > len(v) :
                    continue
                err = form.Meta.err_maps[field]
                break

            return JsonResponse(err)

        #get data from form's cleaned_data
        title = form.cleaned_data.get("title", "%s's video on %s" % (request.user.username, request.get_host()))
        description = form.cleaned_data.get("description", "")
        keywords = form.cleaned_data.get("keywords", "")

        try:
            api = Api()

            # upload method needs authentication
            api.authenticate()

            # Customize following line to your needs, you can add description, keywords or developer_keys
            # I prefer to update video information after upload finishes
            APIResponse = api.upload(title, description, keywords)
        except ApiError:
            # An api error happened
            return JsonResponse(errcode.YoutubeAPIError)
        except:
            # An error happened
            return JsonResponse(errcode.YoutubeUploadMetaError)

        protocol = 'https' if request.is_secure() else 'http'
        next_url = "".join([protocol, ":", os.sep, os.sep, request.get_host(),
                            reverse("django_youtube.views.upload_return"), os.sep])
        extractedAPIResponse = {"token": APIResponse["youtube_token"],
                                "post_url": APIResponse["post_url"],
                                "next_url": next_url}
        return JsonResponse(errcode.SUCCESS, extractedAPIResponse)

upload_meta = UploadVideoMetadata.as_view()

class UploadReturnView(LoginRequriedView):
    def get(self, request):
        status = request.GET.get("status")
        video_id = request.GET.get("id")
        if status == "200" and video_id:
            # upload is successful

            # save the video entry
            video = Video()
            video.user = request.user
            video.video_id = video_id
            # Todo: would Reuqest really happen?
            try:
                video.save()
            except RequestError:
                return JsonResponse(errcode.YoutubeUploadVideoError)

            # send a signal
            video_created.send(sender=video, video=video)

            # Redirect to the video page or the specified page
            try:
                next_url = settings.YOUTUBE_UPLOAD_REDIRECT_URL
            except AttributeError:
                next_url = reverse(
                    "django_youtube.views.video", kwargs={"video_id": video_id})

            return HttpResponseRedirect(next_url)
        else:
            # upload failed, redirect to upload page
            return JsonResponse(errcode.YoutubeUploadVideoError)

upload_return = UploadReturnView.as_view()