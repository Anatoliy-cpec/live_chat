from django import forms
import os
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Author, Chat

image_extension = ['.jpg', '.png', '.bmp', '.gif', '.jpeg', '.svg', '.ico']


class AuthorEditForm(forms.ModelForm):
    class Meta:
       model = Author
       fields = ['profile_photo', 'nickname',]
       widgets = {'profile_photo': forms.FileInput,}

    def clean(self):
            
            cleaned_data = super().clean()

            nickname = cleaned_data.get("nickname")
            if nickname is not None and len(nickname) > 10:
                raise ValidationError({
                    "nickname": f"The nickname cannot be more than 10 characters long. {len(nickname) - 10} char more than 10"
                })
            if len(nickname) < 6:
                 raise ValidationError({
                    "nickname": f"The nickname cannot be less than 6 characters long. {(len(nickname) - 6)*(-1)} char left"
                 })

            cover = cleaned_data.get("profile_photo")
            if cover is not None:
                  file = str(cover)
                  file_ext = os.path.splitext(file)[1]
                  if file_ext not in image_extension:
                        raise ValidationError({
                            "nprofile_photo": "Invalid image format. Please use JPG, PNG, GIF, BMP, JPEG, SVG or ICO."
                        })

            if cover is not None and cover.size > 5242880:
                 raise ValidationError({
                    "profile_photo": "Image size should not be more than 5MB."
                 })
            
            
            
            
            
            return cleaned_data  

