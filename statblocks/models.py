from django.db import models
from django.forms import ModelForm

from base.models import BaseModel


class Monster(BaseModel):
    pass


class MonsterForm(ModelForm):
    class Meta:
        model = Monster
        fields = '__all__'
