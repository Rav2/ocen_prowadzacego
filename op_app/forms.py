__author__ = 'rafal'
from django.forms import Form
from likert_field.forms import LikertFormField

class CommentStars(Form):
    teaching_rate = LikertFormField()