from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    SongModel, CustomUser, Profile, Follow, Reaction, Comment, SavedPost,
    Notebook, Folder, ListItem, Artist, Composer, Lyricist, Tag, Language, Urls
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class ComposerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composer
        fields = '__all__'

class LyricistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lyricist
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class UrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Urls
        fields = '__all__'

class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(many=True, read_only=True)
    composer = ComposerSerializer(many=True, read_only=True)
    lyricist = LyricistSerializer(many=True, read_only=True)
    language = LanguageSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    urls = UrlsSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = SongModel
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    followed = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = '__all__'

class ReactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = SongSerializer(read_only=True)

    class Meta:
        model = Reaction
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = SongSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class SavedPostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = SongSerializer(read_only=True)

    class Meta:
        model = SavedPost
        fields = '__all__'

class NotebookSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notebook
        fields = '__all__'

class FolderSerializer(serializers.ModelSerializer):
    notebook = NotebookSerializer(read_only=True)

    class Meta:
        model = Folder
        fields = '__all__'

class ListItemSerializer(serializers.ModelSerializer):
    folder = FolderSerializer(read_only=True)
    post = SongSerializer(read_only=True)

    class Meta:
        model = ListItem
        fields = '__all__'
