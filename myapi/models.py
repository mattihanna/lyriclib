from datetime import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


SPEED_CHOICES = [
    ('SLOW', '60-80 BPM'),
    ('MODERATE', '80-120 BPM'),
    ('FAST', '120-160 BPM'),
    ('VERY_FAST', '160-200 BPM'),
    ('EXTREMELY_FAST', '200+ BPM'),
]

class SongModel(models.Model):
    song_title = models.CharField(max_length=100)
    song_lyric = models.TextField()
    song_artist = models.ManyToManyField('Artist', related_name='artist')
    song_composer = models.ManyToManyField('Composer', related_name='composer')
    song_lyricist = models.ManyToManyField('Lyricist', related_name='lyricist')
    song_language = models.ManyToManyField('Language', related_name='language')
    song_tags = models.ManyToManyField('Tag', related_name='song_tag')
    song_urls = models.ManyToManyField('Urls', related_name='song_url', blank=True) 
    song_speed = models.CharField(max_length=15, choices=SPEED_CHOICES, default='MODERATE')
    song_created_at = models.TimeField(auto_now_add=True)
    song_updated_at = models.DateTimeField(auto_now=True)
    song_created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_songs')


    def __str__(self):
    # Corrected to use the actual field name
        return f"Title: {self.song_title}, Speed: {self.get_speed_display()}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        ...

    def create_superuser(self, email, password=None, **extra_fields):
        ...

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    ...

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Change to a unique related name
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Change to a unique related name
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    following = models.ManyToManyField('self',symmetrical=False ,related_name='follower', blank=True)
    followers = models.ManyToManyField('self',symmetrical=False ,related_name='followed', blank=True)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    verified = models.BooleanField(default=False)
    

    def __str__(self):
        return f'{self.user.email} Profile'
    
 # social media like models
    
class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')


class Reaction(models.Model):
    POST_REACTIONS = [
        ('Like', 'Like'),
        ('Love', 'Love'),
        # Add more reactions as needed
    ]
    post = models.ForeignKey(SongModel, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=20, choices=POST_REACTIONS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user', 'reaction')


class Comment(models.Model):
    post = models.ForeignKey(SongModel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Save post model
class SavedPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(SongModel, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class Notebook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # Additional fields as needed

class Folder(models.Model):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='folders')
    name = models.CharField(max_length=100)
    # Additional fields as needed

class ListItem(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='items')
    post = models.ForeignKey(SongModel, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

class Artist(models.Model):
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(SongModel, related_name='artists')
    # Additional fields as needed

class Composer(models.Model):
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(SongModel, related_name='composers')
    # Additional fields as needed

class Lyricist(models.Model):
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(SongModel, related_name='lyricists')
    # Additional fields as needed

class Tag(models.Model):
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(SongModel, related_name='tags', blank=True)
    # Additional fields as needed

class Language(models.Model):
    name = models.CharField(max_length=100)
    songs = models.ManyToManyField(SongModel, related_name='languages')
    # Additional fields as needed

class Urls(models.Model):
    url = models.URLField()
    
