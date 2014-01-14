import logging, os
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django_youtube.api import Api, ApiError, AccessControl
from gdata.service import RequestError

from .forms import YoutubeMetadataForm
from .models import VideoTopicourse, video_created
from mylearn.apps.topicourse.models import Topicourse

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
        title = "%s's video on %s" % (request.user.username, request.get_host())
        description = ""
        keywords = "SoWeLearn"
        access_control = form.cleaned_data.get("access_control", 0)

        try:
            api = Api()

            # upload method needs authentication
            api.authenticate()

            # Customize following line to your needs, you can add description, keywords or developer_keys
            # I prefer to update video information after upload finishes
            APIResponse = api.upload(title, description, keywords, access_control)
        except ApiError:
            # An api error happened
            return JsonResponse(errcode.YoutubeAPIError)
        except:
            # An error happened
            return JsonResponse(errcode.YoutubeUploadMetaError)

        protocol = 'https' if request.is_secure() else 'http'
        next_url = "".join([protocol, ":", os.sep, os.sep, request.get_host(),
                            reverse("youtube_upload_return"), os.sep])
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
            video = VideoTopicourse()
            video.userID = request.user.pk
            video.video_id = video_id
            # Todo: would Bad request really happen?
            try:
                video.save()
            except RequestError:
                return JsonResponse(errcode.YoutubeUploadVideoError)

            # send a signal
            video_created.send(sender=video, video=video)

            # create topicourse entry
            topicourse = Topicourse()
            topicourse.topicourseCreatorUserID = request.user.pk
            topicourse.topicourseVideoID = video_id
            topicourse.save()

            current_topicourse = Topicourse.objects.get(topicourseVideoID=video_id)

            # Redirect to the page to input topicourse information
            # Should be an html with video id.
            next_url = reverse('create_topicourse',
                               kwargs= {"topicourseID": current_topicourse.topicourseID})
            return HttpResponseRedirect(next_url)
        else:
            # upload failed, redirect to upload page
            return JsonResponse(errcode.YoutubeUploadVideoError)

upload_return = UploadReturnView.as_view()


class VideoView(LoginRequriedView):

    def get(self,request, video_id):
        api = Api()
        api.authenticate()
        availability = api.check_upload_status(video_id)

        if availability is not True:
            # Video is not available
            if VideoTopicourse.objects.filter(video_id=video_id).exist():

                state = availability["upload_state"]

                # Add additional states here. I'm not sure what states are available
                if state == "failed" or state == "rejected":
                    return JsonResponse(errcode.YoutubeInvalidVideo, availability)
                else:
                    return JsonResponse(errcode.YoutubeVideoProcessed, availability)

            else:
                return JsonResponse(errcode.YoutubeVideoNotExist)

        width = request.GET.get("width", "70%")
        height = request.GET.get("height", "350")
        origin = request.get_host()
        video_src = "http://www.youtube.com/embed/%s?autoplay=0&origin=%s&modestbranding=0&showinfo=0" \
                    %(video_id, origin)

        video_params = {"video_src": video_src, "width": width, "height": height}

        return JsonResponse(errcode.SUCCESS, video_params)

video = VideoView.as_view()