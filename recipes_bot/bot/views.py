from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import User
from .forms import AddRecipeForm


def users_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'users_list.html', context=context)


def add_recipe(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=True)
            return HttpResponseRedirect('/')
    else:
        form = AddRecipeForm()
    return render(request, 'add_recipe.html', {'form': form})
