from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import *
from customer_app.forms import *
from staff_app.models import Report
from django.contrib.auth.decorators import login_required
# Create your views here.
def customer_home(request):
    return render(request,'customertemp/index.html')

@login_required(login_url='sign-in')
def boarding_view(request):
    if request.method == 'POST':
        form = BoardingForm(request.POST)
        if form.is_valid():
            form.instance.customer_id = request.user.id
            form.save()
            return redirect('boarding-details')
    else:
        form = BoardingForm()
    return render(request, 'customertemp/boarding.html', {'form': form})

def cancel_boarding(request, boarding_id):
    boarding = get_object_or_404(Boarding, id=boarding_id)
    if request.user == boarding.customer:
        boarding.delete()
        return redirect('boarding_view')
    else:
        return render(request, 'customertemp/error.html', {'message': 'You are not authorized to cancel this boarding.'})

@login_required(login_url='sign-in')
def list_boarding_details(request):
    data = Boarding.objects.filter(customer=request.user,status="upcoming")
    return render(request, 'customertemp/boarding_detials.html',{'data':data})

@login_required(login_url='sign-in')
def updated_boarding_details(request):
    data = Boarding.objects.filter(customer=request.user).exclude(status="upcoming")
    return render(request, 'customertemp/boarding_detials_updated.html',{'data':data})

@login_required(login_url='sign-in')
def dog_add(request):
    if request.method == 'POST':
        form = DogForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.customer_id = request.user.id
            form.save()
            return redirect('dog-view-customer')
    else:
        form = DogForm()
    return render(request, 'customertemp/dog_add.html', {'form': form})

@login_required(login_url='sign-in')
def dog_view_customer(request):
    data = Dog.objects.filter(customer=request.user)
    return render(request,'customertemp/dog_view.html',{'data':data})

@login_required(login_url='sign-in')
def feeds_add(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.instance.customer_id = request.user.id
            form.save()
            return redirect('feeds-view-customer')
    else:
        form = FeedbackForm()
    return render(request, 'customertemp/feedback_add.html', {'form': form})

@login_required(login_url='sign-in')
def feeds_view_customer(request):
    data = Feedback.objects.filter(customer=request.user)
    return render(request,'customertemp/feedback_view.html',{'data':data})

@login_required(login_url='sign-in')
def staff_view_customer(request):
    staff = User.objects.filter(role=2)
    data = Userprofile.objects.filter(user__in=staff)
    return render(request, 'customertemp/staff_view.html',{'data':data})

@login_required(login_url='sign-in')
def list_reports_customer(request):
    data = Report.objects.filter(customer=request.user)
    return render(request, 'customertemp/report_detials.html',{'data':data})

def room_list(request):
    rooms = Room.objects.all().order_by('id')
    return render(request, 'customertemp/room_cards.html', {'rooms': rooms})

def view_bill_user(request):
    u = User.objects.get(username=request.user)
    print(u)
    bill = Bill.objects.filter(name=u)
    print(bill)
    return render(request, 'customertemp/view_bill_user.html', {'bills': bill})

def pay_bill(request, id):
    bi = Bill.objects.get(id=id)
    if request.method == 'POST':
        card = request.POST.get('card')
        c = request.POST.get('cvv')
        da = request.POST.get('exp')
        CreditCard(card_no=card, card_cvv=c, expiry_date=da).save()
        bi.status = 1
        bi.save()
        return redirect('bill_history')
    return render(request, 'customertemp/pay_bill.html')

def pay_in_direct(request, id):
    bi = Bill.objects.get(id=id)
    bi.status = 2
    bi.save()
    return redirect('bill_history')

def bill_history(request):
    u = User.objects.get(username=request.user)
    bill = Bill.objects.filter(name=u, status__in=[1, 2])
    return render(request, 'customertemp/view_bill_history.html', {'bills': bill})

def sell_dog(request):
    if request.method == 'POST':
        form = SellForm(request.POST, request.FILES)
        if form.is_valid():
            sell = form.save(commit=False)
            sell.seller = request.user
            sell.save()
            return redirect('sell_list')
    else:
        form = SellForm()
    return render(request, 'customertemp/sell_dog.html', {'form': form})

def sell_list(request):
    dogs = Sell.objects.filter(available=True)
    return render(request, 'customertemp/sell_list.html', {'dogs': dogs})


def request_adoption(request, sell_id):
    sell = get_object_or_404(Sell, pk=sell_id)
    if request.method == 'POST':
        if sell.seller == request.user:
            messages.error(request, "You can't adopt your own dog.")
        elif sell.adopted:
            messages.error(request, "This dog has already been adopted.")
        else:
            sell.adopted = True
            sell.save()
            messages.success(request, "Adoption request sent successfully.")
        return redirect('sell_list')
    return render(request, 'customertemp/request_adoption.html', {'sell': sell})


def adopt(request):
    form = Adopt_Pet()
    if request.method == 'POST':
        form = Adopt_Pet(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.To_which_date = form.cleaned_data.get('To_which_date')
            book.booking_date = form.cleaned_data.get('booking_date')
            book.booked_by = request.user
            book.save()
            messages.info(request, 'Successfully sent adopt request ')
            return redirect('adopt_status')
    return render(request, 'customertemp/adopt.html', {'form': form})

def adopt_status(request):
    customer = User.objects.get(username=request.user)
    status = Adopt.objects.filter(booked_by=customer)
    return render(request, 'customertemp/adopt_status.html', {'statuss': status})


