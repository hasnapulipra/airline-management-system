from django.shortcuts import render,redirect

from airline_project import settings

# from airline_project import settings
from .  models import *
from asyncio.windows_events import NULL
from email import message
from django.contrib import messages
import os
from django.core.mail import send_mail


# Create your views here.
def base_page(request):
    return render(request,'base.html')

def home_page(request):
    return render(request,'home.html')

def about_page(request):
    return render(request,'about_us.html')

def contact_page(request):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        # feedback_details=Feedback.objects.get(id=a_id)
        
        message=""
        if request.method == 'POST':
            feedback_details = Feedback()
            feedback_details.name = request.POST['Name']
            feedback_details.email = request.POST['Email']
            feedback_details.date = request.POST['Date']
            feedback_details.message = request.POST['Message']
            feedback_details.save()
            message="Message sent successfully"
            return render(request,'contact_us.html',{'msg':message})
        return render(request,'contact_us.html',{'msg':message})   
            
    return redirect('loginpage')

    

def login(request):
    if request.method == 'POST':
        user_name = request.POST['Username']
        pass_word = request.POST['Password']
        # customer_details = Customer.objects.filter(username=user_name,password=pass_word).exists()
        # airlines_details = Airlines.objects.filter(username=user_name,password=pass_word).exists()

        if Admin.objects.filter(username=user_name,password=pass_word).exists():
            try:
                admin_details = Admin.objects.get(username=user_name,password=pass_word)
                request.session['user_id']=admin_details.id
                return redirect('adminhomepage')
            except Admin.DoesNotExist:
                
                return render(request,'login.html',{'message':'Login Failed'})

        elif Customer.objects.filter(username=user_name,password=pass_word).exists():
            try:
                customer_details = Customer.objects.get(username=user_name,password=pass_word)
                request.session['user_id']=customer_details.id
                return redirect('customerhomepage')
            except Customer.DoesNotExist:
                return render(request,'login_latest.html',{'message':'Login Failed'})


            # customer_details = Customer.objects.get(username=user_name,password=pass_word)
            # request.session['user_id_customer']=customer_details.id
            # return redirect('customerhomepage')
        elif Airlines.objects.filter(username=user_name,password=pass_word).exists():
            try:
                airlines_details = Airlines.objects.get(username=user_name,password=pass_word)
                request.session['user_id']=airlines_details.id
                return redirect('airlineshomepage')
            except Airlines.DoesNotExist:
                return render(request,'login_latest.html',{'message':'Login Failed'})




            # airlines_details = Airlines.objects.get(username=user_name,password=pass_word)
            # request.session['user_id_airlines']=airlines_details.id
            # return redirect('airlineshomepage')
        else:
            return render(request,'login_latest.html',{'message':'Login Failed'})

    return render(request,'login_latest.html')



def logout(request):
    del request.session['user_id']
    
    return redirect('loginpage')


def customer_home_page(request):
    if 'user_id' in request.session:
        c_id = request.session['user_id']
        customer_details=Customer.objects.get(id=c_id)
        return render(request,'customer_home_page.html',{'cust':customer_details})
    return redirect('loginpage')




    # if 'user_id_customer' in request.session:
    #     cust_id = request.session['user_id_customer']
    #     customer_details=Customer.objects.get(id=cust_id)
    #     return render(request,'customer_home_page.html',{'cust':customer_details})
    # return redirect('loginpage')


def admin_home_page(request):
    if 'user_id' in request.session:
        ad_id = request.session['user_id']
        admin_details=Admin.objects.get(id=ad_id)
        return render(request,'admin_home_page.html',{'ad':admin_details})
    return redirect('loginpage')
    

def airlines_home_page(request):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        airlines_details=Airlines.objects.get(id=a_id)
        return render(request,'airlines_home_page.html',{'air':airlines_details})
    return redirect('loginpage')




    # if 'user_id_airlines' in request.session:
    #     air_id = request.session['user_id_airlines']
    #     airlines_details=Airlines.objects.get(id=air_id)
    #     return render(request,'airlines_home_page.html',{'air':airlines_details})
    # return redirect('loginpage')
    

def change_password_page(request):
    
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        customer_details = Customer.objects.get(id=a_id)
        if request.method =='POST':
            if customer_details.password == request.POST['OldPassword']:
                customer_details.password = request.POST['Password']
                customer_details.save()
                return render(request,'change_password.html',{'message':'Password updated successfully'})
            else:
                return render(request,'change_password.html',{'message':'Please enter your old password correctly'})
        else:
            return render(request,'change_password.html')

    return redirect('loginpage')
    


def registration_customer_page(request):
    message=""
    if request.method == 'POST':
        customer_details = Customer()
        if Customer.objects.filter(username=request.POST['Username']).exists():
            # messages.info(request,'Username is already taken')
            message="Username is already taken"
        elif Customer.objects.filter(email=request.POST['Email']).exists():
            # messages.info(request,'Email already taken')
            message="Email is already taken"
        else:
            customer_details.fullname = request.POST['Fullname']
            customer_details.username = request.POST['Username']
            customer_details.email = request.POST['Email']
            customer_details.contact = request.POST['Contact']
            customer_details.password = request.POST['Password']
            customer_details.city = request.POST['City']
            customer_details.date_of_birth = request.POST['Date']
            customer_details.gender = request.POST['Gender']
            
            
            if len(request.FILES) != 0:
                customer_details.image = request.FILES['image'] 
            
            customer_details.save()
            message="Data inserted successfully"
            return render(request,'registration_customer.html',{'msg':message})
            
            
    return render(request,'registration_customer.html',{'msg':message})



def registration_airlines_page(request):
    message=""
    if request.method == 'POST':
        request_details = Request()
        airlines_details = Airlines()
        if Request.objects.filter(username=request.POST['Username']).exists() or Airlines.objects.filter(username=request.POST['Username']).exists():
            # messages.info(request,'Username is already taken')
            message="Username is already taken"
        elif Request.objects.filter(email=request.POST['Email']).exists() or Airlines.objects.filter(email=request.POST['Email']).exists():
            # messages.info(request,'Email already taken')
            message="Email is already taken"
        else:
            request_details.name = request.POST['Name']
            request_details.username = request.POST['Username']
            request_details.email = request.POST['Email']
            request_details.contact = request.POST['Contact']
            request_details.password = request.POST['Password']
            request_details.country = request.POST['Country']
            
            
            
            if len(request.FILES) != 0:
                request_details.image = request.FILES['image'] 
            
            request_details.save()
            message="Data inserted successfully"
            return render(request,'registration_airlines.html',{'msg':message})
            
            
    return render(request,'registration_airlines.html',{'msg':message})


def registration_admin_page(request):
    message=""
    if request.method == 'POST':
        admin_details = Admin()
        if Admin.objects.filter(username=request.POST['Username']).exists():
            message="Username is already taken"
        
        else:
            admin_details.username = request.POST['Username']
            admin_details.password = request.POST['Password']
            admin_details.save()
            message="Data inserted successfully"
            return render(request,'registration_admin.html',{'msg':message})
            
    return render(request,'registration_admin.html',{'msg':message})




def insert_registrationairlines_page(request,airlines_Id):
    request_details=Request.objects.get(id=airlines_Id)
    airlines_details=Airlines()
    airlines_details.name = request_details.name
    airlines_details.username = request_details.username
    airlines_details.email = request_details.email
    airlines_details.contact = request_details.contact
    airlines_details.password = request_details.password
    airlines_details.country = request_details.country
    airlines_details.image = request_details.image
    airlines_details.save()
    Request.objects.get(id=airlines_Id).delete()
    return redirect('view_requestadminpage')


def delete_request_airlines_page(request,airlines_Id):
    Request.objects.get(id=airlines_Id).delete()
    return redirect('view_requestadminpage')


def searchhome_page(request):
    if request.method == 'POST':
        from_city = request.POST['From_country']
        to_country = request.POST['To_country']
            
        if Flight.objects.filter(departure_city=from_city,arrival_city=to_country).exists():
            try:
                flight_details = Flight.objects.filter(departure_city=from_city,arrival_city=to_country)
                return render(request,'search_result_home.html',{'fl':flight_details})
            except:
                return render(request,'search_flight_home.html',{'msg':'No flights are available'})
        else:
            return render(request,'search_flight_home.html',{'msg':'No flights are available'})
    return render(request,'search_flight_home.html')
    
   

def searchcustomer_page(request):
    if 'user_id' in request.session:
        c_id = request.session['user_id']
        if request.method == 'POST':
            from_city = request.POST['From_country']
            to_country = request.POST['To_country']
            
            if Flight.objects.filter(departure_city=from_city,arrival_city=to_country).exists():
                
                flight_details = Flight.objects.filter(departure_city=from_city,arrival_city=to_country)
                return render(request,'search_result_customer.html',{'fl':flight_details})
                
                    
            else:
                return render(request,'search_flight_customer.html',{'msg':'No flights are available'})
        return render(request,'search_flight_customer.html')
    
    return redirect('loginpage')


def addflight_page(request):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        airlines_details=Airlines.objects.get(id=a_id)
        
        message=""
        if request.method == 'POST':
            flight_details = Flight()
            flight_details.airline_name = request.POST['Airline_name']
            flight_details.flight_no = request.POST['Flight_no']
            flight_details.departure_city = request.POST['Departure_city']
            flight_details.arrival_city = request.POST['Arrival_city']
            flight_details.departure_datetime = request.POST['Departure_datatime']
            flight_details.arrival_datetime = request.POST['Arrival_datatime']
            flight_details.no_of_seats = request.POST['Number_of_Seats']
            flight_details.price = request.POST['Price']

                
                
            if len(request.FILES) != 0:
                flight_details.image = request.FILES['Image'] 
                
            flight_details.save()
            message="Data inserted successfully"
            return render(request,'add_flight.html',{'msg':message,'air':airlines_details})
        return render(request,'add_flight.html',{'msg':message,'air':airlines_details})   
            
    return redirect('loginpage')

    

def mybookings_page(request):
    return render(request,'mybookings.html')

def viewbookings_admin_page(request):
    return render(request,'view_bookings_admin.html')


def viewbookings_airlines_page(request):
    return render(request,'view_bookings_airlines.html')

def viewbookings_admin_details_page(request):
    return render(request,'view_bookings_admin_details.html')

def viewbookings_airlines_details_page(request):
    return render(request,'view_bookings_airlines_details.html')

def viewfeedback_page(request):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        feedback_details = Feedback.objects.all()
        return render(request,'view_feedback.html',{'fd':feedback_details})
    
    return redirect('loginpage')
    

def viewusers_page(request):
    customer_details=Customer.objects.all()
    return render(request,'view_users.html',{'cust':customer_details})

def deleteuser_page(request,cust_Id):
    Customer.objects.get(id=cust_Id).delete()
    return redirect('viewuserspage')

def viewprofile_customer_page(request):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        customer_details=Customer.objects.get(id=a_id)
        return render(request,'view_profile_customer.html',{'cust':customer_details})
    return redirect('loginpage')

    
def editprofile_customer_page(request):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        customer_details=Customer.objects.get(id=a_id)
        if request.method == "POST":
            if len(request.FILES) != 0:
                if len(customer_details.image) > 0:
                    os.remove(customer_details.image.path)
                customer_details.image = request.FILES['Image']
            customer_details.fullname = request.POST['Full_name']
            customer_details.email = request.POST['Email']
            customer_details.contact = request.POST['Contact']
            customer_details.city = request.POST['City']
            customer_details.date_of_birth = request.POST['Date']
            
            customer_details.save()
            return redirect('viewprofile_customerpage')
        else:
            customer_details=Customer.objects.get(id=a_id)
            return render(request,'edit_profile_customer.html',{'cust':customer_details})

    return redirect('loginpage')



def viewprofile_airlines_page(request):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        airlines_details=Airlines.objects.get(id=a_id)
        return render(request,'view_profile_airlines.html',{'air':airlines_details})
    return redirect('loginpage')



def editprofile_airlines_page(request):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        airlines_details=Airlines.objects.get(id=a_id)
        if request.method == "POST":
            if len(request.FILES) != 0:
                if len(airlines_details.image) > 0:
                    os.remove(airlines_details.image.path)
                airlines_details.image = request.FILES['Image']
            airlines_details.name = request.POST['Airline_name']
            airlines_details.email = request.POST['Email']
            airlines_details.contact = request.POST['Contact']
            airlines_details.country = request.POST['Country']
            
            airlines_details.save()
            return redirect('viewprofile_airlinespage')
        else:
            airlines_details=Airlines.objects.get(id=a_id)
            return render(request,'edit_profile_airlines.html',{'air':airlines_details})

    return redirect('loginpage')


    



def searchresult_home_page(request):
    return render(request,'search_result_home.html')

def searchresult_customer_page(request):
    if 'user.id' in request.session:
        c_id = request.session['user.id']
        return render(request,'add_passenger.html')
    return redirect('loginpage')

def searchresult_detail_home_page(request,fl_Id):
    flight_details = Flight.objects.get(id=fl_Id)
    return render(request,'search_result_detail_home.html',{'fl':flight_details})
    
    


def searchresult_detail_customer_page(request,fl_Id):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        flight_details = Flight.objects.get(id=fl_Id)
        fl_no = flight_details.flight_no
        image_details = ImageUpload.objects.filter(flight_no=fl_no)
        return render(request,'search_result_detail_customer.html',{'fl':flight_details,'im':image_details})
    return redirect('loginpage')


def view_flightdetail_admin_page(request):
    return render(request,'view_flight_detail_admin.html')


def view_flight_airlines_page(request):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        airlines_details=Airlines.objects.get(id=a_id)
        air_name = airlines_details.name
        # name = Flight.airline_name
        flight_details = Flight.objects.filter(airline_name=air_name)
        return render(request,'view_flight_airlines.html',{'fl':flight_details})   
            
    return redirect('loginpage')
    
    


def view_airlines_admin_page(request):
    airlines_details = Airlines.objects.all()
    return render(request,'view_airlines_admin.html',{'al':airlines_details})


def delete_airlines_page(request,airlines_Id):
    Airlines.objects.get(id=airlines_Id).delete()
    return redirect('viewairlines_adminpage')


def view_flightdetail_airlines_page(request,fl_Id):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        airlines_details=Airlines.objects.get(id=a_id)
        
        flight_details = Flight.objects.get(id=fl_Id)
        fl_no = flight_details.flight_no
        image_details = ImageUpload.objects.filter(flight_no=fl_no)
        return render(request,'view_flight_detail_airlines.html',{'fl':flight_details,'im':image_details})   
            
    return redirect('loginpage')


def delete_view_flight_page(request,fl_Id):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        Flight.objects.get(id=fl_Id).delete()
        return redirect('viewflight_airlinepage')   
            
    return redirect('loginpage')

    
def ok_button_page(request):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        airlines_details=Airlines.objects.get(id=a_id)
        air_name = airlines_details.name
        # name = Flight.airline_name
        flight_details = Flight.objects.filter(airline_name=air_name)
        return render(request,'view_flight_airlines.html',{'fl':flight_details})   
            
    return redirect('loginpage')


def edit_flightdetail_airlines_page(request,fl_Id):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
        airlines_details=Airlines.objects.get(id=a_id)
        flight_details=Flight.objects.get(id=fl_Id)
        if request.method == "POST":
            if len(request.FILES) != 0:
                if len(flight_details.image) > 0:
                    os.remove(flight_details.image.path)
                flight_details.image = request.FILES['Image']
            flight_details.airline_name = request.POST['Airline_name']
            flight_details.flight_no = request.POST['Flight_no']
            flight_details.departure_city = request.POST['Departure_city']
            flight_details.arrival_city = request.POST['Arrival_city']
            # flight_details.departure_datetime = request.POST['Departure_datetime']
            # flight_details.arrival_datetime = request.POST['Arrival_datetime']
            flight_details.no_of_seats = request.POST['Seats']
            flight_details.price = request.POST['Price']
            flight_details.save()
            return redirect('viewflight_airlinepage')
        else:
            flight_details=Flight.objects.get(id=fl_Id)
            return render(request,'edit_flight_details_airlines.html',{'fl':flight_details})

    return redirect('loginpage')

       
            
    
    

def payment_page(request):
    return render(request,'payment.html')

def add_passenger_page(request,fl_Id):
    if 'user_id' in request.session:
        c_id = request.session['user_id']
        customer_details=Customer.objects.get(id=c_id)
        flight_details=Flight.objects.get(id=fl_Id)
        return render(request,'add_passenger.html',{'fl':flight_details})
    return redirect('loginpage')


def after_booking_page(request):
    return render(request,'after_booking.html')

def ticket_page(request):
    return render(request,'ticket.html')


def view_request_admin_page(request):
    request_details=Request.objects.all()
    
    return render(request,'view_request_admin.html',{'req':request_details})


def image_upload_page(request):
    if 'user_id' in request.session:
        a_id = request.session['user_id']
         
        message=""
        if request.method == 'POST':
            image_details = ImageUpload()
            image_details.airline_name = request.POST['Airline_name']

            image_details.flight_no = request.POST['Flight_no']
            if len(request.FILES) != 0:
                image_details.image = request.FILES['Image']
            
            
            image_details.save()
            message="Data inserted successfully"
            return render(request,'image_upload.html',{'msg':message})
        else:
            airline_details = Airlines.objects.get(id=a_id)        
            return render(request,'image_upload.html',{'msg':message,'air':airline_details})
    return redirect('loginpage')




def forgot_password_page(request):
    user_type = request.GET.get('user')
    msg=""
    if request.method=='POST':
        email=request.POST['email']

    if user_type=='customer':
        user = Customer.objects.filter(email=email)

    if user_type=='airlines':
        user = Airlines.objects.filter(email=email)

    print('999',user_type)

    if user.exists():
        print(user[0])
        print(user[0].id)
        uid=user[0].id
        message="password reset link http://127.0.0.1:8000/reset_pass?user=" + user_type + "&id=" + str(uid)
        print(message)
        send_mail(
        'password reset',
        message,
        settings.EMAIL_HOST_USER,
        ['hasnapulipra@gmail.com'],
        fail_silently=False
        )
        print('success')
    else:
        msg="user not exist"

    return render(request,'forgot_password.html',{'error':msg})

    

def reset_pass(request):
    msg=""
    user_type = request.GET.get('user')
    id=int(request.GET.get('id'))
    if request.method=='POST':
        password=request.POST['password']

    if user_type=='cust':
        user = Customer.objects.get(id=id)

    if user_type=='airlines':
        user = Airlines.objects.get(id=id)

    user.password = password
    user.save()
    msg="password reset successfull"

    return render(request,'reset_pass_final',{'msg':msg})
   





def reset_password_final_page(request):
    return render(request,'reset_password_final.html')

def reset_password_laststage(request):
    return render(request,'reset_password_laststage.html')