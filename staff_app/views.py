from django.shortcuts import render,redirect

from accounts.forms import *
from accounts.models import *
from customer_app.models import *
from staff_app.forms import *
from django.contrib.auth.decorators import login_required
# Create your views here.
def staff_home(request):
    return render(request,'stafftemp/index.html')

@login_required(login_url='sign-in')
def profile_view(request):
    data = Userprofile.objects.filter(user=request.user)
    return render(request,'stafftemp/profile.html',{'data':data})

@login_required(login_url='sign-in')
def update_profile(request):
    staff = Userprofile.objects.get(user=request.user)
    form = StaffRegistrationForm(instance=staff)
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST or None, instance=staff or None)
        if form.is_valid():
            form.save()
            return redirect('profile-view')
    return render(request, 'stafftemp/update_profile.html', {'form': form })

@login_required(login_url='sign-in')
def boarding_assigned(request):
    staff=User.objects.get(username=request.user)
    data=Boarding.objects.all().filter(staff=staff)
    return render(request,'stafftemp/boarding_assigned.html',{'data':data})

@login_required(login_url='sign-in')
def boarding_assigned_update(request,pk):
    if request.method=='POST':
        form=StaffUpdateBoardingForm(request.POST)
        if form.is_valid():
            boarding_x=Boarding.objects.get(id=pk)
            boarding_x.status=form.cleaned_data['status']
            boarding_x.save()
            return redirect('boarding-assigned')
    else:
        form=StaffUpdateBoardingForm()
    return render(request,'stafftemp/boarding_assigned_update.html',{'form':form})

@login_required(login_url='sign-in')
def dog_view_staff(request):
    data = Dog.objects.all()
    return render(request,'stafftemp/dog_view.html',{'data':data})

@login_required(login_url='sign-in')
def feedback_view_staff(request):
    data = Feedback.objects.all()
    return render(request,'stafftemp/feedback_view.html',{'data':data})

@login_required(login_url='sign-in')
def report_add(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.instance.staff_id = request.user.id
            form.save()
            return redirect('list-reports')
    else:
        form = ReportForm()
    return render(request, 'stafftemp/report.html', {'form': form})

@login_required(login_url='sign-in')
def list_reports(request):
    data = Report.objects.filter(staff=request.user)
    return render(request, 'stafftemp/report_detials.html',{'data':data})