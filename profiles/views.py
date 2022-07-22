from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serialaziers import ProfileSerializer

class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serialaizer = ProfileSerializer(profiles, many=True)
        return Response(serialaizer.data)
