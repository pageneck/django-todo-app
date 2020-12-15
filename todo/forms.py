from django.forms import ModelForm, Textarea
from .models import Todo



class TodoForm(ModelForm):
  class Meta:
    model = Todo
    fields = ["title","memo","important"]
    widgets ={
      'memo': Textarea(attrs={'cols': 70, 'rows': 5}),
    }
    
    
