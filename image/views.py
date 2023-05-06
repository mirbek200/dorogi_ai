import tempfile
from django.core.files import File
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RoadImage
from .serializers import RoadImageSerializer
import firebase_admin
from firebase_admin import storage


class RoadImageAPIView(APIView):
    serializer_class = RoadImageSerializer

    def post(self, request):
        serializer = RoadImageSerializer(data=request.data)
        if serializer.is_valid():
            road_image = serializer.save()
            if road_image.has_road():
                bucket = storage.bucket()
                filename = f"{road_image.pk}_{road_image.image.name}"
                blob = bucket.blob(filename)
                with tempfile.NamedTemporaryFile(delete=False) as temp:
                    temp.write(road_image.image.read())
                    temp.flush()
                    with open(temp.name, 'rb') as f:
                        blob.upload_from_file(f)
                road_image.image_url = blob.public_url
                road_image.save()
                message = 'На изображении есть дорога, изображение сохранено в Firebase Storage'
            else:
                road_image.image.delete()
                message = 'На изображении нет дороги, изображение удалено'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=400)
