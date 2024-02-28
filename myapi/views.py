import logging
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .forms import SongModelForm, ArtistForm, ComposerForm, LyricistForm, LanguageForm, TagForm
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .permissions import IsOwnerOrReadOnly


from .models import (
    SongModel, Profile,
    Follow, Reaction, Comment, SavedPost, Notebook, Folder, ListItem, Artist, Composer, Lyricist, Language, Tag
)
from .serializers import (
    SongSerializer, FollowSerializer, ReactionSerializer, CommentSerializer, SavedPostSerializer, 
    NotebookSerializer, FolderSerializer, ListItemSerializer, UserSerializer
)
from .forms import ProfileForm, SongModelForm
logger = logging.getLogger(__name__)
# Apply login_required as a method decorator to class-based views
def login_required_class_decorator(cls):
    decorator = method_decorator(login_required)
    cls.dispatch = decorator(cls.dispatch)
    return cls

def catch_all(request, request_path):
    print(f"Caught unmapped path: {request_path}")
    return HttpResponse(f"Path does not match any pattern: {request_path}", status=404)


@login_required_class_decorator
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Adjust permissions as needed

    def perform_create(self, serializer):
        # Ensure password is set correctly
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        
        





# Song-related viewsets
@login_required_class_decorator
class SongViewSet(viewsets.ModelViewSet):
    queryset = SongModel.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsOwnerOrReadOnly]  # Adjust permissions as needed
    def get_queryset(self):
        """
        This view should return a list of all the posts
        for the currently authenticated user.
        """
        user = self.request.user
        return SongModel.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Social feature viewsets
@login_required_class_decorator
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

@login_required_class_decorator
class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

@login_required_class_decorator
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

@login_required_class_decorator
class SavedPostViewSet(viewsets.ModelViewSet):
    queryset = SavedPost.objects.all()
    serializer_class = SavedPostSerializer

@login_required_class_decorator
class NotebookViewSet(viewsets.ModelViewSet):
    queryset = Notebook.objects.all()
    serializer_class = NotebookSerializer

@login_required_class_decorator
class FolderViewSet(viewsets.ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

@login_required_class_decorator
class ListItemViewSet(viewsets.ModelViewSet):
    queryset = ListItem.objects.all()
    serializer_class = ListItemSerializer

# Function-based views
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            return redirect('login')
        else:
            logger.error("Error creating user")
            return HttpResponse("An error occurred during user registration. Please try again.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'pages/profile.html', {'form': form})

def homePage(request):
    return render(request, 'pages/homepage.html')

class SongCreateView(CreateView):
    model = SongModel
    form_class = SongModelForm
    template_name = 'pages/song_form.html'
    success_url = reverse_lazy('song_list')  # Adjust to your named URL for listing songs

    def get_form_kwargs(self):
        kwargs = super(SongCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user in form kwargs
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(SongCreateView, self).form_valid(form)

@login_required
def create_or_edit_song(request, song_id=None):
    # If song_id is provided, we are editing an existing song, otherwise creating a new one
    if song_id:
        song = SongModel.objects.get(pk=song_id)
        if request.user != song.song_created_by:
            # Redirect or return an error if the current user is not the creator of the song
            return redirect('error_view_or_home')
    else:
        song = None

    if request.method == 'POST':
        form = SongModelForm(request.POST, instance=song, user=request.user)  # Pass the current user and the song instance if editing
        if form.is_valid():
            form.save()
            print("Song saved from create_or_edit_song view.")
            # Redirect to the song detail view or some other page
            return redirect('songs', song_id=form.instance.pk)
    else:
        print("Song not saved from create_or_edit_song view.")
        form = SongModelForm(instance=song, user=request.user)  # Pass the current user and the song instance if editing

    context = {
        'form': form,
        'editing': song_id is not None  # Pass to template to adjust heading or text accordingly
    }
    return render(request, 'pages/songlist.html', context)


class ArtistCreateView(CreateView):
    model = Artist
    form_class = ArtistForm
    template_name = 'pages/artist_form.html'
    success_url = reverse_lazy('artist_list')  # Adjust with your actual listing URL

class ArtistUpdateView(UpdateView):
    model = Artist
    form_class = ArtistForm
    template_name = 'pages/artist_form.html'
    success_url = reverse_lazy('artist_list')  # Adjust with your actual listing URL


class ComposerCreateView(CreateView):
    model = Composer
    form_class = ComposerForm
    template_name = 'pages/composer_form.html'
    success_url = reverse_lazy('composer_list')  # Adjust with your actual listing URL

class ComposerUpdateView(UpdateView):
    model = Composer
    form_class = ComposerForm
    template_name = 'pages/composer_form.html'
    success_url = reverse_lazy('composer_list')  # Adjust with your actual listing URL


class LyricistCreateView(CreateView):
    model = Lyricist
    form_class = LyricistForm
    template_name = 'pages/lyricist_form.html'
    success_url = reverse_lazy('lyricist_list')  # Adjust with your actual listing URL

class LyricistUpdateView(UpdateView):
    model = Lyricist
    form_class = LyricistForm
    template_name = 'pages/lyricist_form.html'
    success_url = reverse_lazy('lyricist_list')  # Adjust with your actual listing URL


class TagCreateView(CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'pages/tag_form.html'
    success_url = reverse_lazy('tag_list')  # Adjust with your actual listing URL

class TagUpdateView(UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'pages/tag_form.html'
    success_url = reverse_lazy('tag_list')  # Adjust with your actual listing URL


class LanguageCreateView(CreateView):
    model = Language
    form_class = LanguageForm
    template_name = 'pages/language_form.html'
    success_url = reverse_lazy('language_list')  # Adjust with your actual listing URL

class LanguageUpdateView(UpdateView):
    model = Language
    form_class = LanguageForm
    template_name = 'pages/language_form.html'
    success_url = reverse_lazy('language_list')  # Adjust with your actual listing URL
