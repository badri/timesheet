from piston.handler import BaseHandler
from demo.demoprofile.models import Chunk
from piston.utils import rc

class ChunkUploadHandler(BaseHandler):
    model = Chunk
    fields = ('application', 'timestamp')

    def create(self, request):
        if request.content_type:
            data = request.POST
            chunk = self.model(application=data['application'], timestamp=data['timestamp'], person=request.user)
            chunk.save()
            return rc.CREATED



        



