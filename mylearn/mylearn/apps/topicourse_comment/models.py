from django.db import models

from fluent_comments.moderation import moderate_model, comments_are_open, comments_are_moderated
from fluent_comments.models import get_comments_for_model, CommentsRelation

# Create your models here.

class TopicourseDiscussion(models.Model):
    discussionId = models.AutoField(primary_key = True)
    topicourseId = models.IntegerField('Topicourse ID')
    userId = models.IntegerField('User ID')
    discussionTitle = models.CharField("Title",
                             max_length=255)
    discussionContent = models.TextField("Content",
                              blank=True )
    discussionCreatedDate = models.DateTimeField("Publication date",
                                                 auto_now_add=True)
    discussionEnableComments = models.BooleanField("Enable comments", default=True)
    discussionCommentsCount = models.PositiveIntegerField("Comments total count", default=0)

    # Optional reverse relation, allow ORM querying:
    discussion_comments_set = CommentsRelation()

    class Meta:
        verbose_name = "TopicourseDiscussion"
        verbose_name_plural = "TopicourseDiscussions"

    def __unicode__(self):
        return self.discussionTitle

    # Optional, give direct access to moderation info via the model:
    comments = property(get_comments_for_model)
    comments_are_open = property(comments_are_open)
    comments_are_moderated = property(comments_are_moderated)

# Give the generic app support for moderation by django-fluent-comments:
moderate_model(
    TopicourseDiscussion,
    publication_date_field='discussionCreatedDate',
    enable_comments_field='discussionEnableComments'
)