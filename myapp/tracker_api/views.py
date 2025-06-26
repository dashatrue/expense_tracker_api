from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from .forms import SignUpForm, LoginForm
from .models import CustomUser, Category, Expense
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.is_superuser

admin_required = user_passes_test(lambda user: user.is_superuser)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'todolist/signup.html', {'form': form})

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

    return render(request, 'tracker_api/login.html', {'form': form})

@login_required
def expenses_list(request):
    expenses = request.user.expenses.all()
    return render(request, 'tracker_api/expenses_list.html', {'expenses':expenses})

@login_required
@admin_required
def new_expense(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        assigned_to_id = request.POST.get('assigned_to')
        past_date = request.POST.get('past_date')
        description = request.POST.get('description')
        expense = Expense.objects.create(
            name=name,
            category=category,
            assigned_to_id=int(assigned_to_id),
            past_date=past_date,
            description=description,
        )

        return redirect('home')

    else:
        categories = Category.objects.all()
        users = CustomUser.objects.all()
        return render(request, 'tracker_api/create_expense.html', {'categories': categories, 'users': users})

@login_required
@admin_required
def delete_expense(request, expense_id):
    if request.method == 'POST':
        expense = Expense.objects.get(id=expense_id)
        expense.delete()
    return redirect(reverse('home'))

@login_required
@admin_required
def update_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    if request.method == 'POST':
        expense.name = request.POST.get('name')
        expense.category = request.POST.get('category')
        expense.assigned_to = request.POST.get('assigned_to')
        expense.past_date = request.POST.get('past_date')
        expense.description = request.POST.get('description')
        expense.save()
        return redirect('home')
    else:
        return render(request, 'tracker_api/update_expense.html', {'expense':expense})

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'tracker_api/category_list.html', {'categories':categories})

@login_required
@admin_required
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('home')
    return render(request, 'tracker_api/create_category.html')

