from django.shortcuts import render
from rest_framework import viewsets
from webmain.models import *
from .serializers import *
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework import status

#checks if "requser" can view "user" data
def has_permission(user,requsername=None,requserid=None,cud=False):


    # permission flags
    is_owner = False
    has_view_rights = False

    # Get queryset of followers
    queryset = user.followed.all()
    s = queryset.values_list('FollowCond2', flat=True)
    followers = User.objects.filter(id__in=list(s))

    # print("\n\nFOLLOWERS"+"="*80+str(queryset))

    #  Populate flags
    if requserid is not None:
        is_owner = is_owner or user.id == int(requserid)
        has_view_rights = has_view_rights or followers.filter(id=int(requserid)).exists()
    if requsername is not None:
        is_owner = is_owner or user.username == requsername
        has_view_rights = has_view_rights or followers.filter(username=requsername).exists()

    has_view_rights = has_view_rights or is_owner

    # Check Permissions and return
    return (not cud and has_view_rights) or is_owner

#Basic API Views

class GalleryView(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

    def get_queryset(self):
        queryset = self.queryset
        # Requesting User
        requserid = self.request.query_params.get('requserid', None)
        requsername = self.request.query_params.get('requsername', None)
        # Owner of gallery
        userid = self.request.query_params.get('userid', None)
        username = self.request.query_params.get('username', None)

        user = None
        if userid is not None:
            queryset = queryset.filter(GalleryOwner__id=userid)
            user = User.objects.get(id=userid)
        if username is not None:
            queryset = queryset.filter(GalleryOwner__username=username)
            user = User.objects.get(username=username)
        # Check Permissions
        if user is not None and not has_permission(user, requsername, requserid, cud=False):
            queryset = queryset.none()

        return queryset

    def check_object_permissions(self, request, obj):
        #request parameters
        cud= request.method != 'GET'
        requserid = request.query_params.get('requserid', None)
        requsername = request.query_params.get('requsername', None)
        # Get gallery owner
        user = obj.GalleryOwner
        # Check Permissions
        if not has_permission(user, requsername, requserid, cud):
            print("\n\n\n\nNO PERMISSIONS" + "*" * 80 + str(has_permission) + "\n\n\n\n")
            raise AuthenticationFailed
        return

    def create(self, request, *args, **kwargs):

        data = request.data
        gallert_owner_data = data.pop("GalleryOwner")

        user = User.objects.get(username=gallert_owner_data[1])

        data["GalleryOwner"]=user.id
        serializer = GallerySerializerNoFk(data=data)


        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class GalleryReactionView(viewsets.ModelViewSet):
    queryset = GalleryReaction.objects.all()
    serializer_class = GalleryReactionSerializer

    def get_queryset(self):
        queryset = self.queryset

        # Filter by gallery
        galleryid = self.request.query_params.get('galleryid', None)
        if galleryid is not None:
            queryset = queryset.filter(Gallery__id=galleryid)

        # Requesting User
        requserid = self.request.query_params.get('requserid', None)
        requsername = self.request.query_params.get('requsername', None)
        # Owner of gallery
        userid = self.request.query_params.get('userid', None)
        username = self.request.query_params.get('username', None)

        user = None
        if userid is not None:
            queryset = queryset.filter(Gallery__GalleryOwner__id=userid)
            user = User.objects.get(id=userid)
        if username is not None:
            queryset = queryset.filter(Gallery__GalleryOwner__username=username)
            user = User.objects.get(id=username)

        # Check Permissions
        if user is not None and not has_permission(user, requsername, requserid, cud=False):
            queryset = queryset.none()
        return queryset

    def check_object_permissions(self, request, obj):
        #request parameters
        cud= request.method != 'GET'
        requserid = request.query_params.get('requserid', None)
        requsername = request.query_params.get('requsername', None)
        # Get gallery owner
        user = obj.Gallery.GalleryOwner
        # Check Permissions
        if not has_permission(user, requsername, requserid, cud):
            print("CHECKING PERMISSIONS"+"="*40+str(requsername)+" "+str(requserid)+"  cud=="+str(cud))
            raise AuthenticationFailed
        return

class PhotoView(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        queryset = self.queryset

        # Filter by gallery
        galleryid = self.request.query_params.get('galleryid', None)
        if galleryid is not None:
            queryset = queryset.filter(Gallery__id=galleryid)

        # Requesting User
        requserid = self.request.query_params.get('requserid', None)
        requsername = self.request.query_params.get('requsername', None)
        # Owner of gallery
        userid = self.request.query_params.get('userid', None)
        username = self.request.query_params.get('username', None)

        user = None
        if userid is not None:
            queryset = queryset.filter(Gallery__GalleryOwner__id=userid)
            user = User.objects.get(id=userid)
        if username is not None:
            queryset = queryset.filter(Gallery__GalleryOwner__username=username)
            user = User.objects.get(id=username)
        # Check Permissions
        if user is not None and not has_permission(user, requsername, requserid, cud=False):
            queryset = queryset.none()
        return queryset

    def check_object_permissions(self, request, obj):

        print("\n\n\n\nREQUEST" + "*" * 80 + str(request.method) + "\n\n\n\n")

        #request parameters
        cud= request.method != 'GET'
        requserid = request.query_params.get('requserid', None)
        requsername = request.query_params.get('requsername', None)
        # Get gallery owner
        user = obj.Gallery.GalleryOwner
        # Check Permissions
        if not has_permission(user, requsername, requserid, cud):
            print("\n\n\n\nNO PERMISSION" + "*" * 80 +  "\n\n\n\n")
            raise AuthenticationFailed
        return

class PhotoReactionView(viewsets.ModelViewSet):
    queryset = PhotoReaction.objects.all()
    serializer_class = PhotoReactionSerializer

    def get_queryset(self):
        queryset = self.queryset

        # Filter by photo
        photoid = self.request.query_params.get('photoid', None)
        if photoid is not None:
            queryset = queryset.filter(Photo__id=photoid)

        # Requesting User
        requserid = self.request.query_params.get('requserid', None)
        requsername = self.request.query_params.get('requsername', None)
        # Owner of gallery
        userid = self.request.query_params.get('userid', None)
        username = self.request.query_params.get('username', None)

        user = None
        if userid is not None:
            queryset = queryset.filter(Photo__Gallery__GalleryOwner__id=userid)
            user = User.objects.get(id=userid)
        if username is not None:
            queryset = queryset.filter(Photo__Gallery__GalleryOwner__username=username)
            user = User.objects.get(id=username)
        # Check Permissions
        if user is not None and not has_permission(user, requsername, requserid, cud=False):
            queryset = queryset.none()
        return queryset

    def check_object_permissions(self, request, obj):
        #request parameters
        cud= request.method != 'GET'
        requserid = request.query_params.get('requserid', None)
        requsername = request.query_params.get('requsername', None)
        # Get gallery owner
        user = obj.Photo.Gallery.GalleryOwner
        # Check Permissions
        if not has_permission(user, requsername, requserid, cud):
            raise AuthenticationFailed
        return

class GalleryCommentView(viewsets.ModelViewSet):
    queryset = GalleryComment.objects.all()
    serializer_class = GalleryCommentSerializer

    def get_queryset(self):
        queryset = self.queryset
        # Filter by gallery
        galleryid = self.request.query_params.get('galleryid', None)
        if galleryid is not None:
            queryset = queryset.filter(Gallery__id=galleryid)
        # Requesting User
        requserid = self.request.query_params.get('requserid', None)
        requsername = self.request.query_params.get('requsername', None)
        # Owner of gallery
        userid = self.request.query_params.get('userid', None)
        username = self.request.query_params.get('username', None)

        user = None
        if userid is not None:
            queryset = queryset.filter(Gallery__GalleryOwner__id=userid)
            user = User.objects.get(id=userid)
        if username is not None:
            queryset = queryset.filter(Gallery__GalleryOwner__username=username)
            user = User.objects.get(id=username)
        # Check Permissions
        if user is not None and not has_permission(user, requsername, requserid, cud=False):
            queryset = queryset.none()
        return queryset

    def check_object_permissions(self, request, obj):
        #request parameters
        cud= request.method != 'GET'

        print("\n\nCUD :"+"="*60+str(cud))

        requserid = request.query_params.get('requserid', None)
        requsername = request.query_params.get('requsername', None)
        # Get gallery owner
        user = obj.Gallery.GalleryOwner
        # Check Permissions
        if not has_permission(user, requsername, requserid, cud):
            raise AuthenticationFailed
        return

class PhotoCommentView(viewsets.ModelViewSet):
    queryset = PhotoComment.objects.all()
    serializer_class = PhotoCommentSerializer

    def get_queryset(self):
        queryset = self.queryset
        # Filter by photo
        photoid = self.request.query_params.get('photoid', None)
        if photoid is not None:
            queryset = queryset.filter(Photo__id=photoid)
        # Requesting User
        requserid = self.request.query_params.get('requserid', None)
        requsername = self.request.query_params.get('requsername', None)
        # Owner of gallery
        userid = self.request.query_params.get('userid', None)
        username = self.request.query_params.get('username', None)

        user = None
        if userid is not None:
            queryset = queryset.filter(Photo__Gallery__GalleryOwner__id=userid)
            user = User.objects.get(id=userid)
        if username is not None:
            queryset = queryset.filter(Photo__Gallery__GalleryOwner__username=username)
            user = User.objects.get(id=username)
        # Check Permissions
        if user is not None and not has_permission(user, requsername, requserid, cud=False):
            queryset = queryset.none()
        return queryset

    def check_object_permissions(self, request, obj):
        #request parameters
        cud= request.method != 'GET'
        requserid = request.query_params.get('requserid', None)
        requsername = request.query_params.get('requsername', None)
        # Get gallery owner
        user = obj.Photo.Gallery.GalleryOwner
        # Check Permissions
        if not has_permission(user, requsername, requserid, cud):
            raise AuthenticationFailed
        return

class FollowView(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_queryset(self):
        queryset = self.queryset

        FC1 = self.request.query_params.get('fc1username', None)
        FC2 = self.request.query_params.get('fc2username', None)

        if FC1 is not None:
            user = get_object_or_404(User,username=FC1)
            queryset = queryset.filter(FollowCond1__id=user.id )

        if FC2 is not None:
            user = get_object_or_404(User,username=FC2)
            queryset = queryset.filter(FollowCond2__id=user.id )

        return queryset

    def check_object_permissions(self, request, obj):
        #request parameters
        cud= request.method != 'GET'
        requserid = request.query_params.get('requserid', None)
        requsername = request.query_params.get('requsername', None)
        # Get gallery owner
        user = obj.FollowCond1
        # Check Permissions
        if not has_permission(user, requsername, requserid, cud):
            raise AuthenticationFailed
        return

class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = self.queryset

        userid = self.request.query_params.get('userid', None)
        if userid is not None:
            queryset = queryset.filter(user__id=userid)

        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user__username=username)
        return queryset

    def check_object_permissions(self, request, obj):
        # request parameters
        cud = request.method != 'GET'
        # Proceed with checks only on cud operations
        if not cud:
            return

        requserid = request.query_params.get('requserid', None)
        requsername = request.query_params.get('requsername', None)
        # Get Profile Owner
        user = obj.user
        # Check Permissions
        if not has_permission(user, requsername, requserid, cud):
            raise AuthenticationFailed
        return

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = self.queryset

        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)

        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)

        return queryset

# Advanced API views
class SharedGalleriesView(viewsets.ReadOnlyModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

    def get_queryset(self):
        queryset = self.queryset

        userid = self.request.query_params.get('requserid', None)
        username = self.request.query_params.get('requsername', None)

        if userid is None and username is None:
            return queryset.none()

        if userid is not None:
            friends = Follow.objects.filter(FollowCond2__id=userid).all().values_list('FollowCond1', flat=True)
            queryset = Gallery.objects.filter(GalleryOwner__in=friends).all().order_by('-UploadDateTime')

        if username is not None:
            friends = Follow.objects.filter(FollowCond2__username=username).all().values_list('FollowCond1', flat=True)
            queryset = Gallery.objects.filter(GalleryOwner__in=friends).all().order_by('-UploadDateTime')

        return queryset

class FollowersView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        #get user
        queryset = self.queryset

        userid = self.request.query_params.get('userid', None)
        username = self.request.query_params.get('username', None)

        if userid is None and username is None:
            return queryset.none()

        if userid is not None:
            user = User.objects.get(id=userid)

        if username is not None:
            user = User.objects.get(username=username)

        queryset = user.followed.all()
        s = queryset.values_list('FollowCond2',flat=True)

        queryset = User.objects.filter(id__in = list(s))

        return queryset

class FollowersProfileView(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        #get user
        queryset = self.queryset

        userid = self.request.query_params.get('userid', None)
        username = self.request.query_params.get('username', None)

        if userid is None and username is None:
            return queryset.none()

        if userid is not None:
            user = User.objects.get(id=userid)

        if username is not None:
            user = User.objects.get(username=username)

        queryset = user.followed.all()
        s = queryset.values_list('FollowCond2',flat=True)
        queryset = Profile.objects.filter(user__id__in = list(s))

        return queryset

class FollowingView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        #get user
        queryset = self.queryset

        userid = self.request.query_params.get('userid', None)
        username = self.request.query_params.get('username', None)

        if userid is None and username is None:
            return queryset.none()

        if userid is not None:
            user = User.objects.get(id=userid)

        if username is not None:
            user = User.objects.get(username=username)

        queryset = user.follower.all()
        s = queryset.values_list('FollowCond1',flat=True)

        queryset = User.objects.filter(id__in = list(s))

        if following_filter != None:
            queryset = queryset.filter(username=following_filter)

        return queryset

class FollowingProfileView(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        #get user
        queryset = self.queryset

        userid = self.request.query_params.get('userid', None)
        username = self.request.query_params.get('username', None)

        if userid is None and username is None:
            return queryset.none()

        if userid is not None:
            user = User.objects.get(id=userid)

        if username is not None:
            user = User.objects.get(username=username)

        queryset = user.follower.all()
        s = queryset.values_list('FollowCond1',flat=True)
        queryset = Profile.objects.filter(user__id__in = list(s))

        return queryset

class SearchProfileView(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    def get_queryset(self):
        #get user
        queryset = self.queryset
        query = self.request.query_params.get('query', None)
        if query is not None:
            queryset = queryset.filter(Q(user__username__icontains=query)).distinct()
        else:
            queryset = queryset.none()
        return queryset

# Reaction Toggle
class PhotoReactionToggle(APIView):

    def get(self, request):

        # Requesting User
        requserid = request.query_params.get('requserid', None)
        requsername = request.query_params.get('requsername', None)

        photoid = request.query_params.get('photoid', None)

        user = None
        try:
            if requserid is not None:
                user = User.objects.get(id=requserid)
            if requsername is not None:
                user = User.objects.get(username=requsername)

            photo = Photo.objects.get(id=int(photoid))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not has_permission(user, requsername, requserid, False):
            raise AuthenticationFailed

        instance, created = PhotoReaction.objects.get_or_create(User=user, Photo=photo)

        if not created:
            instance.delete()
            return Response(status=status.HTTP_302_FOUND)

        return Response(status=status.HTTP_201_CREATED)

class GalleryReactionToggle(APIView):
    def get(self, request):
        # Requesting User
        requserid = request.query_params.get('requserid', None)
        requsername = request.query_params.get('requsername', None)

        galleryid = request.query_params.get('galleryid', None)

        user = None
        try:
            if requserid is not None:
                user = User.objects.get(id=requserid)
            if requsername is not None:
                user = User.objects.get(username=requsername)

            gallery = Gallery.objects.get(id=int(galleryid))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not has_permission(user, requsername, requserid, False):
            raise AuthenticationFailed

        instance, created = GalleryReaction.objects.get_or_create(User=user, Gallery=gallery)

        if not created:
            instance.delete()
            return Response(status=status.HTTP_302_FOUND)

        return Response(status=status.HTTP_201_CREATED)