from piston.handler import BaseHandler
from demo.demoprofile.models import Chunk
from piston.utils import rc

class ChunkUploadHandler(BaseHandler):
    model = Chunk
    fields = ('upload')

    def create(self, request):
        if request.content_type:
            data = request.POST
            print "data upload:---------"
            print data['upload']
            print "data upload split:-------------"
            print data['upload'].split("\n")
            
            for i in data['upload'].split("\n")[:-1]:
                print "each element:"
                print i
                app_timestamp, app = i.split(":::")
                chunk = self.model(application=app.strip(), timestamp=app_timestamp.strip(), person=request.user)
                chunk.save()
                print chunk.id()
            return rc.CREATED



        



