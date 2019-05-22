import requests
from .models import *
from api.serializers import *
from rest_framework.parsers import JSONParser

base_url="http://localhost:80/api"


# Basic API
def get_gallery(requsername=None,id=None,username=None):
    params={}
    url = base_url+'/basic/gallery'
    if id is not None:
        url += "/" + str(id)
    if username is not None:
        params["username"]=username
    if requsername is not None:
        params["requsername"] = requsername

    r = requests.get(url,params=params)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = GalleryDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_gallery_reaction(requsername=None,id=None,galleryid=None):
    params={}
    url = base_url+'/basic/gallery_reactions'
    if id is not None:
        url += "/" + str(id)
    if galleryid is not None:
        params["galleryid"]=galleryid
    if requsername is not None:
        params["requsername"] = requsername

    r = requests.get(url,params=params)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = GalleryReactionSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_photo(requsername=None,id=None,galleryid=None):
    params={}
    url = base_url+'/basic/photos'
    if id is not None:
        url += "/" + str(id)
    if galleryid is not None:
        params["username"]=galleryid
    if requsername is not None:
        params["requsername"] = requsername

    r = requests.get(url,params=params)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = PhotoDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_photo_reaction(requsername=None, id=None, photoid=None):
    params={}
    url = base_url+'/basic/photo_reactions'
    if id is not None:
        url += "/" + str(id)
    if photoid is not None:
        params["photoid"]=photoid
    if requsername is not None:
        params["requsername"] = requsername

    r = requests.get(url,params=params)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = PhotoReactionSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_gallery_comment(requsername=None,id=None,galleryid=None):
    params={}
    url = base_url+'/basic/gallery_comments'
    if id is not None:
        url += "/" + str(id)
    if galleryid is not None:
        params["galleryid"]=galleryid
    if requsername is not None:
        params["requsername"] = requsername

    r = requests.get(url,params=params)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = GalleryCommentSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_photo_comment(requsername=None, id=None, photoid=None):
    params={}
    url = base_url+'/basic/photo_comments'
    if id is not None:
        url += "/" + str(id)
    if photoid is not None:
        params["photoid"]=photoid
    if requsername is not None:
        params["requsername"] = requsername

    r = requests.get(url,params=params)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = PhotoReactionSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_follow(id=None,requsername=None):
    params={}
    url = base_url+'/basic/follows'
    if id is not None:
        url += "/" + str(id)
    if requsername is not None:
        params["requsername"] = requsername

    r = requests.get(url,params=params)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = FollowSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_profile(id=None,username=None):
    params={}
    url = base_url+'/basic/profiles'
    if id is not None:
        url += "/" + str(id)
    if username is not None:
        params["username"] = username

    r = requests.get(url)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    # print("\n\nDATA_PROFILES"+"="*40+"\n"+str(data)+"\n\n")
    for dt in data:
        serializer = ProfileDeserializer(data=dt)
        serializer.is_valid()
        # print("\n\nIS_VALID" + "=" * 40 + "\n" + str(serializer.errors) + "\n\n")
        obj = serializer.create()
        objects.append(obj)

    return objects

def get_user(id=None,username=None):
    params={}
    url = base_url+'/basic/users'
    if id is not None:
        url += "/" + str(id)
    if username is not None:
        params["username"] = username

    r = requests.get(url)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = UserSerializer(data=dt)
        serializer.is_valid()
        # print(serializer.errors)
        obj = serializer.create()
        objects.append(obj)
    return objects

#Advance API

def get_shared_galleries(requsername):
    params={}
    url = base_url+'/advanced/shared_galleries'
    params["requsername"] = requsername

    r = requests.get(url,params=params)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = GalleryDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_followers(username):
    params={}
    url = base_url+'/advanced/followers'

    params["username"] = username

    r = requests.get(url,params=params)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = UserSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_followers_profiles(username):
    params={}
    url = base_url+'/advanced/followers_profiles'

    params["username"] = username

    r = requests.get(url,params=params)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = ProfileDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_following(username):
    params={}
    url = base_url+'/advanced/following'

    params["username"] = username

    r = requests.get(url,params=params)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = UserSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_following_profiles(username):
    params={}
    url = base_url+'/advanced/following'

    params["username"] = username

    r = requests.get(url,params=params)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = ProfileDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_search_profiles(query):
    params={}
    url = base_url+'/advanced/profile_search'

    params["query"] = query

    r = requests.get(url,params=params)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = ProfileDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

# Post API
def post_gallery(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = GallerySerializer(object)
    return requests.post('/basic/gallery', data=serializer.data, params=params)

def post_gallery_reaction(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = GalleryReactionSerializer(object)
    return requests.post('/basic/gallery_reactions', data=serializer.data ,params=params)

def post_photo(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = PhotoSerializer(object)
    return requests.post('/basic/photos', data=serializer.data, params=params)

def post_photo_reaction(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = PhotoReactionSerializer(object)
    return requests.post('/basic/photo_reactions', data=serializer.data, params=params)

def post_gallery_comment(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = GalleryCommentSerializer(object)
    return requests.post('/basic/gallery_comments', data=serializer.data, params=params)

def post_photo_comment(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = PhotoCommentSerializer(object)
    return requests.post('/basic/photo_comments', data=serializer.data, params=params)

def post_follow(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = FollowSerializer(object)
    return requests.post('/basic/follows', data=serializer.data, params=params)

def post_profile(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = ProfileSerializer(object)
    return requests.post('/basic/profiles', data=serializer.data, params=params)

def post_user(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = UserSerializer(object)
    return requests.post('/basic/users', data=serializer.data, params=params)

# Put API
def put_gallery(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = GallerySerializer(object)
    return requests.put('/basic/gallery', data=serializer.data, params=params)

def put_gallery_reaction(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = GalleryReactionSerializer(object)
    return requests.put('/basic/gallery_reactions', data=serializer.data, params=params)

def put_photo(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = PhotoSerializer(object)
    return requests.put('/basic/photos', data=serializer.data, params=params)

def put_photo_reaction(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = PhotoReactionSerializer(object)
    return requests.put('/basic/photo_reactions', data=serializer.data, params=params)

def put_gallery_comment(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = GalleryCommentSerializer(object)
    return requests.put('/basic/gallery_comments', data=serializer.data, params=params)

def put_photo_comment(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = PhotoCommentSerializer(object)
    return requests.put('/basic/photo_comments', data=serializer.data, params=params)

def put_follow(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = FollowSerializer(object)
    return requests.put('/basic/follows', data=serializer.data, params=params)

def put_profile(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = ProfileSerializer(object)
    return requests.put('/basic/profiles', data=serializer.data, params=params)

def put_user(object,requsername):
    params = {}
    params["requsername"] = requsername
    serializer = UserSerializer(object)
    return requests.post('/basic/users', data=serializer.data, params=params)

# Delete API
def delete_gallery(id,requsername):
    params = {}
    params["requsername"] = requsername
    return requests.delete('/basic/gallery/' + str(id), params=params)

def delete_gallery_reaction(id,requsername):
    params = {}
    params["requsername"] = requsername
    return requests.delete('/basic/gallery_reactions/' + str(id), params=params)

def delete_photo(id,requsername):
    params = {}
    params["requsername"] = requsername
    return requests.delete('/basic/photos/' + str(id), params=params)

def delete_photo_reaction(id,requsername):
    params = {}
    params["requsername"] = requsername
    return requests.delete('/basic/photo_reactions/' + str(id), params=params)

def delete_gallery_comment(id,requsername):
    params = {}
    params["requsername"] = requsername
    return requests.delete('/basic/gallery_comments/' + str(id), params=params)

def delete_photo_comment(id,requsername):
    params = {}
    params["requsername"] = requsername
    return requests.delete('/basic/photo_comments/' + str(id), params=params)

def delete_follow(id,requsername):
    params = {}
    params["requsername"] = requsername
    return requests.delete('/basic/follows/' + str(id), params=params)

def delete_profile(id,requsername):
    params = {}
    params["requsername"] = requsername
    return requests.delete('/basic/profiles/' + str(id), params=params)

def delete_user(id,requsername):
    params = {}
    params["requsername"] = requsername
    return requests.post('/basic/users/' + str(id), params=params)