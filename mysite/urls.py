from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from myapp import views
from admin_panel import views as admin_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from myapp.views import movie_details,MovieListView,ShowIndex,payment_gateway,payment_confirmation,reserve_seat,BookingListView,BookingDetailView,BookingDeleteView
app_name = 'movie'

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('',homepage),


    
   #User Side
   #path('moviefunc',views.moviefunc, name='movie'),
   url(r'^$', ShowIndex.as_view(),name='index'),
   url(r'^movies/', include('movies.urls',namespace='movie'),name='movies'),
   url(r'^booking/', include('booking.urls',namespace='booking'),name='booking'),
   path('aboutfunc',views.aboutfunc,name='aboutus'),
   path('contactfunc',views.contactfunc,name='contactus'),
   path('chooseloginfunc',views.chooseloginfunc,name='chooselogin'),
   path('loginfunc',views.loginfunc,name='login'),
   path('signupfunc',views.signupfunc,name='signup'),
   path('signup',views.signup),
   path('loginform',views.login),
   path('contactform',views.contactform),
   path('logoutform',views.logout_page,name="logoutform"),
   path('after_user_login',views.userloginfunc,name='user_home'),
   path('loginform',views.userloginfunc,name='user_home1'),
   path('movie_book_user',views.movieuserfunc,name='movieuser'),
   path('trailer_show_user',views.traileruserfunc,name='traileruser'),





   #admin side
   path('adminloginfunc',views.adminlogin01,name='adminlogin1'),
   path('admin/', admin.site.urls),
   path('adminloginform',views.adminlogin),
   path('admin_panel',admin_views.admin_dashboard,name='admin_panel'),
   path('add_movie', admin_views.add_movie,name='add_movie'),
   path('addmoviefunc',admin_views.addmoviefunc,name="addmoviefunc"),
   path('update_show',admin_views.update_show,name="update_show"),
   path('add_show',admin_views.add_show,name="add_show"),
   path('add_theatre',admin_views.add_theatre,name="add_theatre"),
   path('feedback', admin_views.Feedback,name='Feedback'),
   path('update_movie/<int:id>', admin_views.update_movie,name='update_movie'),
   path('update_movie/up_movie/<int:id>',admin_views.up_movie,name='up_movie'),
   path('show_movie', admin_views.show_movie,name='show_movie'),
   path('ui', admin_views.ui,name='ui'),
   #path('up_movie/<int:id>',admin_views.up_movie,name='up_movie'),
   #url('delete_movie/(?P<id>\d+)$', admin_views.delete_movie,name='delete_movie'),
   path('delete_movie/<int:id>',admin_views.delete_movie,name='delete_movie'),
   path('after_admin_login',views.adminloginfunc,name='admin_home'),
   path('trailer_show_admin',views.traileradminfunc,name='traileradmin'),
   path('movie_show_admin',views.movieadminfunc,name='movieadmin'),
   path('logout_admin',admin_views.logout_admin,name='logout_admin'),
   path('logout_page',admin_views.logout_page,name='logout_page'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
