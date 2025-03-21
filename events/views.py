from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q, Prefetch
from django.utils import timezone
from django.http import HttpResponseServerError
from events.models import Event, Participant, Category
from events.forms import EventForm, ParticipantForm, CategoryForm

# Custom error handler
def error_500(request):
    return render(request, 'error.html', status=500)

def error(request):
    return render(request, 'error.html')

# Dashboard View
def dashboard(request):
    type = request.GET.get('type', 'all')
    today = timezone.now().date()

    base_events = Event.objects.select_related('category').prefetch_related('participants')

    filters = {
        'total_events': base_events,
        'upcoming_events': base_events.filter(date__gte=timezone.now()).order_by('date'),
        'past_events': base_events.filter(date__lt=timezone.now()).order_by('-date'),
    }
    events = filters.get(type, base_events.filter(date=today).order_by('date'))

    context = {
        'events': events,
        'total_events': base_events.count(),
        'total_participants': Participant.objects.count(),
        'upcoming_events': filters['upcoming_events'].count(),
        'past_events': filters['past_events'].count(),
        'type': type,
    }
    return render(request, 'dashboard.html', context)

# Home View
def home(request):
    events = Event.objects.select_related('category').prefetch_related('participants')
    
    event_name = request.GET.get('event_name', '')
    event_location = request.GET.get('event_location', '')

    if event_name or event_location:
        events = events.filter(Q(name__icontains=event_name) | Q(location=event_location))

    context = {
        'events': events.order_by('id'),
        'form': EventForm(),
        'location_choices': events.values_list('location', flat=True).distinct()
    }
    return render(request, 'home.html', context)

# Event Views
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('dashboard')
    return render(request, 'event_confirm_delete.html', {'event': event})

def event_details(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_details.html', {'event': event})

# Category Views
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form, 'category': category})

def category_list(request):
    categories = Category.objects.order_by('id')
    return render(request, 'category_list.html', {'categories': categories})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})

# Participant Views
def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'participant_form.html', {'form': form})

def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participant_form.html', {'form': form, 'participant': participant})

def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
    return render(request, 'participant_confirm_delete.html', {'participant': participant})

def participant_list(request):
    participants = Participant.objects.prefetch_related(
        Prefetch('events', queryset=Event.objects.only('id', 'name'))
    ).order_by('id')

    return render(request, 'participant_list.html', {'participants': participants})
