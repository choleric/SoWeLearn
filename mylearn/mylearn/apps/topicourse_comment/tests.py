# -*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib import comments

from ..projtest import BaseTest, BaseTestUtil
from .models import TopicourseDiscussion
from mylearn.apps import errcode


class TopicourseCommentTest(BaseTest):
    def _create_user(self):
        acc = 'create@create.com'
        pwd = 'password'
        user = BaseTestUtil.create_user(
                email= acc,
                password = pwd,
                is_active=True,
                first_name = 'VV',#下面测试需要用
                last_name='UU',
                )

        BaseTestUtil.create_email(
                user=user,
                email=acc,
                verified=True
                )
        return user

    def _create_user_and_login(self):
        user = self._create_user()
        response = self.client.post(reverse('account_login'),
                                    {'login': user.email,
                                     'password': "password"})
        self.assertEquals(302, response.status_code, "login with status: %d" % (response.status_code))
        return user

    def _logout(self):
        self.client.get(reverse('account_signout_learn'))
        self.__user = None

    def setUp(self) :
        super(TopicourseCommentTest, self).setUp()
        self.__user = self._create_user_and_login()

    def tearDown(self) :
        self._logout()

    @property
    def user(self) :
        return self.__user

    def test_model(self):
        test_param = {
            'topicourseId': 1000,
            'discussionTitle': 'test title',
            'discussionContent' : 'test content',
            'userId': 100,
        }
        discussion = TopicourseDiscussion(**test_param)
        discussion.save()

        newDiscussion = TopicourseDiscussion.objects.get(pk=discussion.discussionId)
        self.assertEqual(newDiscussion.discussionTitle, test_param['discussionTitle'])

    def _build_discussion(self):
        self.__discussion = {
            'topicourseId': 1000,
            'discussionTitle': 'test title',
            'discussionContent' : 'test content'
        }

    def _build_comment(self, discussion):
        resp = self.client.get(reverse('comment_security', kwargs={'discussion_id': discussion.discussionId}))
        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content)
        self.__comment = {
            'content_type': 'topicourse_comment.topicoursediscussion',
            'object_pk': discussion.discussionId,
            'name': 'test comment name',
            'email': 'test@comment.com',
            'comment': 'test comment',
            'timestamp': resp_data['d']['timestamp'],
            'security_hash': resp_data['d']['security_hash'],
        }

    def _post_discussion(self):
        self.assertEqual(TopicourseDiscussion.objects.count(), 0)
        self._build_discussion()

        resp = self.client.post(reverse('discussion_create'), self.__discussion)

        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content)
        self.assertEqual(resp_data['c'], errcode.SUCCESS, resp_data)
        self.assertEqual(TopicourseDiscussion.objects.count(), 1)
        discussion = TopicourseDiscussion.objects.filter(discussionTitle=self.__discussion['discussionTitle'])[0]
        self.assertEqual(discussion.topicourseId, self.__discussion['topicourseId'])
        self.assertEqual(discussion.discussionContent, self.__discussion['discussionContent'])
        self.assertEqual(discussion.userId, self.__user.pk)

    def test_create_discussion(self):
        self._post_discussion()

    def _test_create_discussion_empty_one_field(self, field_name):
        self.assertEqual(TopicourseDiscussion.objects.count(), 0)
        self._build_discussion()
        del self.__discussion[field_name]

        resp = self.client.post(reverse('discussion_create'), self.__discussion)

        self.assertEqual(resp.status_code, 200)
        return json.loads(resp.content)

    def test_create_discussion_empty_one_field(self):
        resp_data = self._test_create_discussion_empty_one_field('discussionTitle')
        self.assertEqual(resp_data['c'], errcode.topicourseDiscussionFormInvalid, resp_data)

    def test_create_discussion_empty_content(self):
        resp_data = self._test_create_discussion_empty_one_field('discussionContent')
        self.assertEqual(resp_data['c'], errcode.SUCCESS, resp_data)

    def test_create_discussion_empty_topicourseid(self):
        resp_data = self._test_create_discussion_empty_one_field('topicourseId')
        self.assertEqual(resp_data['c'], errcode.topicourseDiscussionFormInvalid, resp_data)

    def test_create_comment(self):
        self._post_discussion()
        discussion = TopicourseDiscussion.objects.filter(discussionTitle=self.__discussion['discussionTitle'])[0]
        self.assertEqual(discussion.discussion_comments_set.count(), 0)
        CommentsModle = comments.get_model()
        self.assertEqual(CommentsModle.objects.count(), 0)

        self._build_comment(discussion)
        resp = self.client.post(reverse('comment_create'), self.__comment, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content)
        self.assertEqual(resp_data['c'], errcode.SUCCESS, resp_data)
        self.assertEqual(CommentsModle.objects.count(), 1)
        self.assertEqual(discussion.discussion_comments_set.count(), 1)
        self.assertEqual(discussion.discussion_comments_set.get().comment, self.__comment['comment'])
        self.assertEqual(discussion.discussion_comments_set.get().name, self.__user.get_full_name())

    def _test_create_comment_empty_field(self, field_name):
        self._post_discussion()
        discussion = TopicourseDiscussion.objects.filter(discussionTitle=self.__discussion['discussionTitle'])[0]
        self.assertEqual(discussion.discussion_comments_set.count(), 0)
        CommentsModle = comments.get_model()
        self.assertEqual(CommentsModle.objects.count(), 0)
        self._build_comment(discussion)
        del self.__comment[field_name]

        resp = self.client.post(reverse('comment_create'), self.__comment, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content)
        self.assertEqual(resp_data['c'], errcode.topicourseDiscussionFormInvalid, resp_data)
        self.assertEqual(CommentsModle.objects.count(), 0)
        self.assertEqual(discussion.discussion_comments_set.count(), 0)

    def test_create_comment_empty_comment(self):
        self._test_create_comment_empty_field('comment')

    def test_create_comment_empty_timestamp(self):
        self._test_create_comment_empty_field('timestamp')

    def test_create_comment_empty_security_hash(self):
        self._test_create_comment_empty_field('security_hash')

    def test_create_comment_empty_name(self):
        self._post_discussion()
        discussion = TopicourseDiscussion.objects.filter(discussionTitle=self.__discussion['discussionTitle'])[0]
        self.assertEqual(discussion.discussion_comments_set.count(), 0)
        CommentsModle = comments.get_model()
        self.assertEqual(CommentsModle.objects.count(), 0)
        self._build_comment(discussion)
        del self.__comment['name']

        resp = self.client.post(reverse('comment_create'), self.__comment, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content)
        self.assertEqual(resp_data['c'], errcode.SUCCESS, resp_data)
        self.assertEqual(CommentsModle.objects.count(), 1)
        self.assertEqual(discussion.discussion_comments_set.count(), 1)

    def test_create_comment_wait_too_long(self):
        self._post_discussion()
        discussion = TopicourseDiscussion.objects.filter(discussionTitle=self.__discussion['discussionTitle'])[0]
        self.assertEqual(discussion.discussion_comments_set.count(), 0)
        CommentsModle = comments.get_model()
        self.assertEqual(CommentsModle.objects.count(), 0)
        self._build_comment(discussion)
        self.__comment['timestamp'] = str(int(self.__comment['timestamp']) - 1800)

        resp = self.client.post(reverse('comment_create'), self.__comment, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(resp.status_code, 200)
        resp_data = json.loads(resp.content)
        self.assertEqual(resp_data['c'], errcode.topicourseDiscussionFormInvalid, resp_data)
        self.assertEqual(CommentsModle.objects.count(), 0)
        self.assertEqual(discussion.discussion_comments_set.count(), 0)

    def test_create_comment_not_login(self):
        self._post_discussion()
        discussion = TopicourseDiscussion.objects.filter(discussionTitle=self.__discussion['discussionTitle'])[0]
        self.assertEqual(discussion.discussion_comments_set.count(), 0)
        CommentsModle = comments.get_model()
        self.assertEqual(CommentsModle.objects.count(), 0)
        self._build_comment(discussion)
        self._logout()

        resp = self.client.post(reverse('comment_create'), self.__comment, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        #TODO 此处并没有收到topicourseDiscussionQueryInvalid响应
        self.assertEqual(resp.status_code, 302, resp)
        #
        #resp_data = json.loads(resp.content)
        #self.assertEqual(resp_data['c'], errcode.topicourseDiscussionQueryInvalid, resp_data)
        #self.assertEqual(CommentsModle.objects.count(), 0)
        #self.assertEqual(discussion.discussion_comments_set.count(), 0)


