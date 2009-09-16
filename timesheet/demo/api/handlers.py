from piston.handler import BaseHandler
from demo.demoprofile.models import Chunk
from piston.utils import rc

class ChunkUploadHandler(BaseHandler):
    model = Chunk
    fields = ('upload')

    def create(self, request):
        if request.content_type:
            data = request.POST
            for i in data['upload'].split("\n")[:-1]:
                print i
                app_timestamp, app = i.split(":::")            
                print app_timestamp.strip()
                chunk = self.model(application=app.strip(), timestamp=app_timestamp.strip(), person=request.user)
                chunk.save()
            return rc.CREATED



        



