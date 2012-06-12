from django.db import models
from sorl.thumbnail import get_thumbnail

from armstrong.core.arm_content.mixins.images import ImageMixin
from armstrong.core.arm_content.mixins.images import SorlThumbnailMixin
from armstrong.apps.content.models import Content


class Image(Content, ImageMixin, SorlThumbnailMixin):
    def _admin_thumbnail(self):
        thumbnail = get_thumbnail(self.image, '250x250', crop='center', quality=80)
        d = {'thumbnail_url': thumbnail.url, 'alt': self.title, 'original_img_url': self.image.url}
        return """<div class="thumbnail" style="width: 250px;">
                      <img src="%(thumbnail_url)s" alt="%(alt)s" />
                      <div style="text-align: center"><a href="%(original_img_url)s" target="_blank">(View Origional Image)</a></div>
                  </div>""" % d
    _admin_thumbnail.short_description = "Thumbnail"
    _admin_thumbnail.allow_tags = True


class ImageSet(Content):
    def first_element(self):
        if self.imagesetelement_set.all().count() > 0:
            return self.imagesetelement_set.all()[0]

        return None


class ImageSetElement(models.Model):
    image = models.ForeignKey(Image)
    imageset = models.ForeignKey(ImageSet)
    caption = models.CharField(blank=True, null=True, max_length=255)
    order = models.IntegerField()

    def __unicode__(self):
        return '%d - %s' % (self.order, self.caption[:35])

    class Meta:
        ordering = ('order',)
