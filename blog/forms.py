from django import forms
from .models import UserReview

class UserReviewForm(forms.ModelForm):
    
    class Meta:
        model = UserReview
        exclude = ["post"]
        labels = {"username":"Your Name", "usercomment":"Your Comment", "email":"Your Email"}

