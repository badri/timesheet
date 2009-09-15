from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication


auth = HttpBasicAuthentication(realm='TestApplication')

from demo.api.handlers import ChunkUploadHandler

chunkUpload = Resource(handler=ChunkUploadHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^upload\.(?P<emitter_format>.+)$', chunkUpload),
    )

