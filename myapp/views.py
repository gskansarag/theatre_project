from django.shortcuts import render,redirect
from django.http import HttpResponse
from myapp.models import  *
from django.shortcuts import render, get_object_or_404
from .models import Booking, BookedSeat, Seat
#from theatre.models import Show
from .forms import SeatForm, BookingForm
from django.urls import reverse_lazy
import datetime
from django.views.generic import ListView,DetailView,DeleteView
from django.shortcuts import redirect
from django.http.response import Http404
from django.views.generic import View, CreateView, FormView, ListView

import datetime
# Create your views here.

#movie view
class MovieListView(ListView):
    def get_queryset(self):
        return Movie.objects.all().order_by('language')
       
       
    def get_context_data(self,*args, **kwargs):
        context = super(MovieListView,self).get_context_data(*args,**kwargs)
        #context = "user/movie/movie_list.html"
        movies = Movie.objects.all().order_by('language')
        movie_list = []
        movie_by_lang = []
        lang = movies[0].language
        for i in range(0, len(movies)):
            if lang != movies[i].language:
                lang = movies[i].language
                movie_list.append(movie_by_lang)
                movie_by_lang = []
            movie_by_lang.append(movies[i])
        movie_list.append(movie_by_lang)
        context['movie_list'] = movie_list
        return context


def movie_details(request, movie_id):
    try:
        movie_info = Movie.objects.get(pk=movie_id)
        shows = Show.objects.filter(movie=movie_id, 
            date=datetime.date.today()).order_by('theatre')
        show_list = []

        if shows:
            show_by_theatre = []
            theatre = shows[0].theatre
            for i in range(0, len(shows)):
                if theatre != shows[i].theatre:
                    theatre = shows[i].theatre
                    show_list.append(show_by_theatre)
                    show_by_theatre = []
                show_by_theatre.append(shows[i])
    
            show_list.append(show_by_theatre)

    except Movie.DoesNotExist:
        raise Http404("Page does not exist")
    return render(request, 'user/movie/movie_detail.html', 
        {'movie_info': movie_info, 'show_list': show_list})
      
    
    
    






def reserve_seat(request, show_id):
    try:
        show_info = Show.objects.get(pk=show_id)
    except Theatre.DoesNotExist:
        raise Http404("Page does not exist")
    form = SeatForm()
    return render(request, 'reserve_seat.html', 
        {'show_info': show_info, 'form': form})


def payment_gateway(request):
    if request.POST:
        seats = request.POST.get('selected_seat')
        seat_type = request.POST.get('seat_type')
        show_id = request.POST.get('show_id')

        show = Show.objects.get(pk=show_id)
        seats = seats.split(',')
        book_seat = []
        for each in seats:
            if Seat.objects.filter(no=each, show=show).exists():
                return render(request, 'reserve_seat.html', 
                    {'show_info': show, 'form': SeatForm()})
            s = Seat(no=each, seat_type=seat_type, show=show)
            book_seat.append(s)
        Seat.objects.bulk_create(book_seat)

        form = BookingForm()

        price_dict = {'Platinum': 300, 'Gold': 200, 'Silver': 100}
        ticket_price = price_dict[seat_type]*len(book_seat)

        seat_str = ""
        for i in range(0, len(seats)):
            if i == len(seats)-1:
                seat_str += seats[i]
            else:
                seat_str += seats[i] + ','

        return render(request, 'payment_gateway.html', 
            {'seats': seat_str, 'seat_type': seat_type, 
            'show': show, 'form': form, 'ticket_price': ticket_price})
    else:
        return redirect('theatre.views.theatre_list')


def payment_confirmation(request):
    if request.POST:
        show_id = request.POST.get('show_id')
        show = Show.objects.get(pk=show_id)
        seats = request.POST.get('selected_seat')
        seats = seats.split(',')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payment_type = request.POST.get('payment_type')
        paid_amount = request.POST.get('amount')
        paid_by = request.user
        id = str(show) + str(seats) + timestamp
        book = Booking(id=id, timestamp=timestamp, payment_type=payment_type, 
            paid_amount=paid_amount, paid_by=paid_by)
        book.save()

        booked_seat = []

        for seat in seats:
            print(seat)
            s = Seat.objects.get(no=seat, show=show)
            b = Booking.objects.get(pk=id)
            booked = BookedSeat(seat=s, booking=b)
            booked_seat.append(booked)

        BookedSeat.objects.bulk_create(booked_seat)

        return render(request, 'payment_confirmation.html')
    else:
        return redirect('theatre.views.theatre_list')


class BookingListView(ListView):
    def get_queryset(self):
        return Booking.objects.filter(paid_by=self.request.user)
    
class BookingDetailView(DetailView):
    def get_queryset(self):
        return Booking.objects.filter(paid_by=self.request.user)
    
    def get_object(self,*args,**kwargs):
        btid = self.kwargs.get('btid')
        obj = get_object_or_404(Booking,id=btid)
        return obj

class BookingDeleteView(DeleteView):
    model = Booking
    success_url = reverse_lazy('booking:list')    
    def get_object(self,*args,**kwargs):
        btid = self.kwargs.get('btid')
        obj = get_object_or_404(Booking,id=btid)
        return obj



def signup(request):

    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile_no=request.POST.get('mobile_no')
        password=request.POST.get('password')
        insert=user_table(name=name,email=email,mobile_no=mobile_no,password=password)
        insert.save()
    return render(request,'user/login.html')

lusername=""
lpassword=""


def login(request):
    if request.method=='POST':
        context={}
        lusername=request.POST.get('email')
        lpassword=request.POST.get('password')
        try:
            login_obj=user_table.objects.get(email=lusername,password=lpassword)
            request.session['user_id'] = lusername
            return redirect('user_home')
        except:
            return redirect('login')
    return render(request,'trailer')


def adminlogin(request):
    if request.method=='POST':
        context={}
        lusername=request.POST.get('email')
        lpassword=request.POST.get('password')
        try:
            login_obj=admin.objects.get(email=lusername,password=lpassword)
            request.session['user_id'] = lusername
            return redirect('admin_panel')
        except:
            return redirect('chooselogin')
    return render(request,'trailer')


def contactform(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        insert=feedback(name=name,email=email,subject=subject,message=message)
        insert.save()
    return render(request,'index.html')



def adminloginfunc(request):
    return render(request,"admin/admin_home.html")

def traileradminfunc(request):
    return render(request,"admin/admin_add_trailer.html")

def movieadminfunc(request):
    return render(request,"admin/movie_admin.html")




def userloginfunc(request):
    return render(request,"user/user_home.html")

def traileruserfunc(request):
    return render(request,"user/trailer_user.html")

def movieuserfunc(request):
    return render(request,"user/movie_user.html")

class ShowIndex(View):
    def get(self,request,*args,**kwargs):
        movie_list = Movie.objects.all().order_by('popularity_index')
        top_movie  = Movie.objects.all().order_by('popularity_index')[:3]
        context = {'movie_list':movie_list,'top_movie':top_movie}
        return render(request,'index.html',context)

def moviefunc(request):
    return render(request,"movie.html")

def contactfunc(request):
    return render(request,"contact.html")

def aboutfunc(request):
    return render(request,"about.html")

def trailerfunc(request):
    return render(request,"trailer.html")

def logout_page(request):
    return render(request,"user/logout_user.html")

def logout(request):
    try:
        del request.session['user_id']
        #return render(request,"index.html")
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

def chooseloginfunc(request):
    return render(request,"choose_login.html")

def adminlogin01(request):
    return render(request,"admin/admin_login.html")

def loginfunc(request):
    return render(request,"user/login.html")

def signupfunc(request):
    return render(request,"user/signup.html")
# Create your views here.
