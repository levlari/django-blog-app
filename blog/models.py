from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import time


def user_media_path(instance, filename):
    """
    Returns the path to where a user uploaded file is saved.
    Has the form: user_<id>/YYYY/MMM/filename
    """
    return 'user_{0}/{1}/{2}/{3}'.format(instance.author.id,
                                        time.strftime('%Y'),
                                        time.strftime('%b'),
                                        filename)


@python_2_unicode_compatible
class Article(models.Model):
    # Editable fields:
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to=user_media_path, null=True, blank=True)

    # Non-editable fields:
    slug = models.SlugField(max_length=50, unique=True)
    published_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    word_count = models.PositiveIntegerField()
    # readtimes- slow: 100 wpm, avg: 130 wpm, fast: 160wpm
    read_time_in_mins = models.PositiveIntegerField()

    # # `word_count` and `read_time_in_mins` will be (re)assigned
    # # everytime the article is saved.
    # def save(self, *args, **kwargs):
    #     self.word_count = len(self.content.split())
    #     self.read_time_in_mins = self.word_count / 130  # assuming avg reading speed.
    #     return super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:read_post', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-published_on']
