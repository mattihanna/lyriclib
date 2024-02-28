from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .models import CustomUser, Profile, SongModel, Artist, Composer, Lyricist, Language, Tag, Urls


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date', 'username', 'first_name', 'last_name', 'email','following', 'followers', 'image', 'verified']  
        


# Define the SPEED_CHOICES if not imported from models
SPEED_CHOICES = [
    ('SLOW', '60-80 BPM'),
    ('MODERATE', '80-120 BPM'),
    ('FAST', '120-160 BPM'),
    ('VERY_FAST', '160-200 BPM'),
    ('EXTREMELY_FAST', '200+ BPM'),
]

class SongModelForm(forms.ModelForm):
    song_artist = forms.ModelMultipleChoiceField(
        queryset=Artist.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Adjust based on your requirements
    )
    song_composer = forms.ModelMultipleChoiceField(
        queryset=Composer.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Adjust based on your requirements
    )
    song_lyricist = forms.ModelMultipleChoiceField(
        queryset=Lyricist.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Adjust based on your requirements
    )
    song_language = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Adjust based on your requirements
    )
    song_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Adjust based on your requirements
    )
    song_urls = forms.ModelMultipleChoiceField(
        queryset=Urls.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Adjust based on your requirements
    )
    song_speed = forms.ChoiceField(
        choices=SPEED_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = SongModel
        fields = ['song_title', 'song_lyric', 'song_artist', 'song_composer', 'song_lyricist', 'song_language', 'song_tags', 'song_urls', 'song_speed', 'song_created_by']
        exclude = ['song_created_at', 'song_updated_at']  # Exclude auto-managed fields

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract user from kwargs and remove it
        super(SongModelForm, self).__init__(*args, **kwargs)
        # You can now use self.user in this form

    def save(self, commit=True):
        instance = super(SongModelForm, self).save(commit=False)
        if self.user:  # Check if user is provided
            instance.song_created_by = self.user  # Set the song_created_by field to the current user
        if commit:
            instance.save()
            self.save_m2m()  # Needed for saving ManyToMany relations
        return instance
    


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ['name', 'songs']
        widgets = {
            'songs': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(ArtistForm, self).__init__(*args, **kwargs)
        self.fields['songs'].required = False

class ComposerForm(forms.ModelForm):
    class Meta:
        model = Composer
        fields = ['name', 'songs']
        widgets = {
            'songs': forms.CheckboxSelectMultiple,
        }
    def __init__(self, *args, **kwargs):
        super(ComposerForm, self).__init__(*args, **kwargs)
        self.fields['songs'].required = False

class LyricistForm(forms.ModelForm):
    class Meta:
        model = Lyricist
        fields = ['name', 'songs']
        widgets = {
            'songs': forms.CheckboxSelectMultiple,
        }
    def __init__(self, *args, **kwargs):
        super(LyricistForm, self).__init__(*args, **kwargs)
        self.fields['songs'].required = False

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'songs']
        widgets = {
            'songs': forms.CheckboxSelectMultiple,
       
        }
    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.fields['songs'].required = False

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['name', 'songs']
        widgets = {
            'songs': forms.CheckboxSelectMultiple,
        }
    def __init__(self, *args, **kwargs):
        super(LanguageForm, self).__init__(*args, **kwargs)
        self.fields['songs'].required = False