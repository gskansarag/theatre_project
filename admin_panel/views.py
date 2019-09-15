from django.shortcuts import render,redirect
from myapp.models import add_movies, Movie ,feedback,Show
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def admin_dashboard(request):
	"""about page"""
	user_id=request.session['user_id']
	#user_name=admin.objects.get(name=)
	context = {'user':request.user,'user_id':user_id}
	template = 'admin/index.html'
	return render(request,template,context)

def logout_page(request):
	context = {'user':request.user}
	template = 'admin/logout_admin.html'
	return render(request,template,context)

# def logout_admin(request):
# 	if request.method == "GET":
# 		if 'action' in request.GET:
# 			action.request.GET.get('action')
# 			if action == 'logout':
# 				if request.session.has_key('user_id'):
# 					request.session.flush()
# 				return redirect("/adminlogin")
def logout_admin(request):
	logout(request)
	return redirect('/adminloginfunc') 

def Feedback(request):
	"""about page"""
	ins = feedback.objects.all()
	#context = {'user':request.user,'ins':ins}
	template = 'admin/feedback.html'
	#ins = Movie.objects.all()
    #return render(request,template,{'ins':ins})
	#return render(request,template,context)
	return render(request,'admin/feedback.html',{'ins':ins})


def add_show(request):
	"""about page"""
	context = {'user':request.user}
	items=Show.objects.all()
	template = 'admin/add_show.html'
	return render(request,template,{'items':items})

def add_theatre(request):
	"""about page"""
	context = {'user':request.user}
	template = 'admin/add_theatre.html'
	return render(request,template,context)

def update_show(request):
	"""about page"""
	context = {'user':request.user}
	template = 'admin/update_show.html'
	return render(request,template,context)


def ui(request):
	"""about page"""
	context = {'user':request.user}
	template = 'admin/ui.html'
	return render(request,template,context)



def update_movie(request,id):
	"""about page"""
	movie_id =  add_movies.objects.get(movie_id=id)
	context  =  {'user':request.user,'movie_id':movie_id}
	template =  'admin/update_movie.html'
	return render(request,template,context)




def show_movie(request):
	"""about page"""
	context = {'user':request.user}
	#template = 'admin/show_movie.html'
	#return render(request,template,context)
	ins = add_movies.objects.all()
	return render(request,'admin/show_movie.html',{'ins':ins})


def add_movie(request):
	"""about page"""
	context = {'user':request.user}
	template = 'admin/add_movie.html'
	return render(request,template,context)

def addmoviefunc(request):
	if request.method=='POST' and request.FILES['Movie_Image']:
		#movies_desc=request.POST.get('Movie_Description')
		movie_name=request.POST.get('Movie_Name')
		cast=request.POST.get('Movie_Cast')
		length=request.POST.get('Movie_Length')
		language=request.POST.get('Movie_Language')
		director=request.POST.get('Movie_Director')
		time=request.POST.get('Movie_Time')
		screen_id=request.POST.get('Movie_Screen_id')
		myfile = request.FILES.get('Movie_Image')
		trailer=request.POST.get('Movie_Trailer')
		insert=Movie(name=movie_name,cast=cast,director=director,language=language,run_length=length,screen_id=screen_id,trailer=trailer,image=myfile,time=time)
		insert.save()
		messages.success(request, 'Movie was Inserted successfully!')
		ins = Movie.objects.all()
		return render(request,'admin/show_movie.html',{'ins':ins})
	else:
		return render(request,'admin/add_movie.html')


def up_movie(request, id):
	#if request.POST=="POST" and request.FILES['MOVIE_IMAGE']:
	member = add_movies.objects.get(movie_id=id)
	member.movie_name = request.POST['Movie_Name']
	member.cast = request.POST['Movie_Cast']
	member.movie_desc = request.POST['Movie_Descrption']
	member.run_length= request.POST['Movie_Length']
	member.language= request.POST['Movie_Language']
	member.director= request.POST['Movie_Director']
	member.time= request.POST['Movie_Time']
	member.screen_id= request.POST['Movie_Screen_Id']
	member.trailer= request.POST['Movie_Trailer']
	member.image= request.FILES.get('Movie_Image')
	member.save()
	messages.success(request, 'Member was updated successfully!')
	return render(request,'admin/show_movie.html')
	

def delete_movie(request, id):
    member = add_movies.objects.get(movie_id=id)
    member.delete()
    messages.error(request, 'Member was deleted successfully!')
    return render(request,'admin/show_movie.html')

'''def view_movies(request):
	ins = add_movies.objects.all()
	return render(request,'admin/show_movie.html',{'ins':ins})

def create(request):
    if request.method == 'POST':
        member = Member(
        firstname=request.POST['firstname'],
        lastname=request.POST['lastname'],
        mobile_number=request.POST['mobile_number'],
        description=request.POST['description'],
        date=request.POST['date'],
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(), )
        try:
            member.full_clean()
        except ValidationError as e:
            pass
        member.save()
        messages.success(request, 'Member was created successfully!')
        return redirect('/list')
    else:
        return render(request, 'add.html')'''
