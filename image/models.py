from django.db import models
from PIL import Image
import cv2
import numpy as np
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'dorogakg-e3c2a.appspot.com'})


class RoadImage(models.Model):
    image = models.ImageField(upload_to='road_images')

    def has_road(self):
        img = cv2.imread(self.image.path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
        if lines is not None:
            return True
        else:
            return False

