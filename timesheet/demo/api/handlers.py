from piston.handler import BaseHandler
from demo.demoprofile.models import Chunk
from piston.utils import rc

class ChunkUploadHandler(BaseHandler):
    model = Chunk
    fields = ('upload')

    def create(self, request):
        if request.content_type:
            data = request.POST

            minute = [] 
            for i in data['upload'].split("\n")[:-1]:
                minute.append(i)

            for i in minute:
                app_timestamp, app = i.split(":::")
                chunk = self.model(application=app.strip(), timestamp=app_timestamp.strip(), person=request.user)
                chunk.save()
            return rc.CREATED
