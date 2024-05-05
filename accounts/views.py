from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from accounts.forms import *
from django.contrib import messages
from accounts.models import *
from customer_app.forms import AddBill
from customer_app.models import *
from staff_app.models import Report
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'index.html')

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        u_form = UserRegistrationForm(request.POST)
        if form.is_valid() and u_form.is_valid():
            user = u_form.save(commit=False)
            user.role = 3
            user.is_active = True
            user.save()
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('sign-in') 
    else:
        form = CustomerRegistrationForm()
        u_form = UserRegistrationForm()
    return render(request,'register.html',{'form':form,'u_form':u_form})

def login_view(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                if user.role == 1:
                    return redirect('admin-home')
                elif user.role == 2:
                    return redirect('staff_home')
                elif user.role == 3:
                    return redirect('customer-home')
            else:
                messages.info(request, 'Invalid Credentials or User is not active')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    return render(request, 'login.html')


def admin_home(request):
    return render(request,'admintemp/index.html')

@login_required(login_url='sign-in')
def dog_view(request):
    data = Dog.objects.all()
    return render(request,'admintemp/dog_view.html',{'data':data})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='sign-in')
def staff_register(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST,request.FILES)
        u_form = UserRegistrationForm(request.POST)
        if form.is_valid() and u_form.is_valid():
            user = u_form.save(commit=False)
            user.role = 2
            user.is_active = True
            user.save()
            staff = form.save(commit=False)
            staff.user = user
            staff.save()
            return redirect('staff-view') 
    else:
        form = StaffRegistrationForm()
        u_form = UserRegistrationForm()
    return render(request,'admintemp/staff_register.html',{'form':form,'u_form':u_form})

@login_required(login_url='sign-in')
def staff_view(request):
    staff = User.objects.filter(role=2)
    data = Userprofile.objects.filter(user__in=staff)
    return render(request, 'admintemp/staff_view.html',{'data':data})

@login_required(login_url='sign-in')
def customer_view(request):
    data = User.objects.filter(role=3)
    c_data = Userprofile.objects.filter(user__in=data)
    return render(request, 'admintemp/customer_view.html',{'c_data':c_data})

@login_required(login_url='sign-in')
def feedback_view_admin(request):
    data = Feedback.objects.all()
    return render(request,'admintemp/feedback_view.html',{'data':data})

@login_required(login_url='sign-in')
def boardings_view_admin(request):
    data=Boarding.objects.all().order_by('-id')
    return render(request,'admintemp/boarding_detials.html',{'data':data})

@login_required(login_url='sign-in')
def approve_boardings(request,pk):
    if request.method=='POST':
        form=AdminApproveBoardingForm(request.POST)
        if form.is_valid():
            boarding_x=Boarding.objects.get(id=pk)
            boarding_x.staff=form.cleaned_data['staff']
            boarding_x.status=form.cleaned_data['status']
            boarding_x.save()
            return redirect('boarding-view-admin')
    else:
        form=AdminApproveBoardingForm()
    return render(request,'admintemp/approve_boardings.html',{'form':form})

def list_reports_admin(request):
    data = Report.objects.all()
    return render(request, 'admintemp/report_detials.html',{'data':data})

def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room-view')
    else:
        form = RoomForm()
    return render(request,'admintemp/create_room.html',{'form':form})

def room_view(request):
    data = Room.objects.all()
    return render(request,'admintemp/rooms.html',{'data':data})

def bill(request):
    form = AddBill()
    if request.method == 'POST':
        form = AddBill(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view-bill')
    return render(request, 'admintemp/generate_bill.html', {'form': form})

def view_bill(request):
    bill = Bill.objects.all()
    print(bill)
    return render(request, 'admintemp/view_payment_details.html', {'bills': bill})

def Adoption_requests(request):
    book = Adopt.objects.all()
    for i in book:
        i.seen = True
        i.save()
    request.session['adopts'] = 0
    return render(request, 'admintemp/Adoption_requests.html', {'books': book})

@login_required(login_url='accounts:login_view')
def confirm_booking(request, id):
    details_qs = Sell.objects.all()
    if details_qs.exists():

        book = Adopt.objects.get(id=id)
        book.status = 1
        book.save()
        messages.info(request, 'Adoption Confirmed')
        return redirect('Adoption_requests')
    else:
        messages.info(request, 'Not Available')
        return HttpResponseRedirect(reverse('Adoption_requests'))

@login_required(login_url='accounts:login_view')
def reject_booking(request, id):
    book = Adopt.objects.get(id=id)
    if request.method == 'POST':
        book.status = 2
        book.save()
        messages.info(request, 'Adoption rejected')
        return redirect('Adoption_requests')
    return render(request, 'admintemp/reject_booking.html')





