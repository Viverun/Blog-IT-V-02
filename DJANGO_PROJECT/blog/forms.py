from django import forms
from .models import Comment, Post, Tag
from django_summernote.widgets import SummernoteWidget


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 4,
                'style': 'border-radius: 16px; background-color: #f8f9fa; padding: 15px;'
            }
        )
    )

    class Meta:
        model = Comment
        fields = ['content']


class PostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title...',
            }
        )
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter an enticing description...',
                'rows': 3,
            }
        ),
        help_text="A brief description to attract readers. If left empty, a generic description will be displayed."
    )

    # Using Summernote for rich content editing
    content = forms.CharField(
        widget=SummernoteWidget(
            attrs={
                'placeholder': 'Write your post content here...',
                'class': 'form-control',
            }
        )
    )

    # Multi-select for tags with custom styling
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'tag-checkbox-list',
            }
        ),
        required=False,
        help_text="Select relevant tags for your post or create new ones below."
    )

    # Field for adding new tags
    new_tags = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Add new tags (comma separated)...',
            }
        ),
        help_text="Enter new tags separated by commas (e.g., 'python, django, web development')"
    )

    class Meta:
        model = Post
        fields = ['title', 'description', 'content', 'tags']

    def save(self, commit=True):
        post = super().save(commit=False)

        if commit:
            post.save()

            # Clear existing tags if form has tags field
            if 'tags' in self.cleaned_data:
                post.tags.set(self.cleaned_data['tags'])

            # Process any new tags
            if self.cleaned_data['new_tags']:
                tag_names = [tag.strip() for tag in self.cleaned_data['new_tags'].split(',') if tag.strip()]

                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)
        return post # Ensure the post instance is returned


class SearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control me-2",
                "type": "search",
                "placeholder": "Search posts...",
                "aria-label": "Search",
                "style": "border-radius: 20px 0 0 20px; background-color: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: #ffffff !important; padding-left: 1rem;" 
            }
        ),
        label=""
    )