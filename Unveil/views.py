from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from .models import User, Blog, SessionList

def WhoIsLoggedIn(request) :
	if not request.session.session_key :
		request.session.save()

	ses_key = request.session.session_key
	user = None

	ses = SessionList.objects.filter(key = ses_key)

	if ses.exists() :
		user = User.objects.get(username = ses[0].username)
		#user = ses[:1].get().username

	return user

def getFullName(uname) :
	userobjects = User.objects.filter(username = uname)

	if userobjects.exists() :
		return userobjects[0].firstname + ' ' + userobjects[0].lastname

	return None

def homepage(request) :
	if not request.session.session_key :
		request.session.save()

	blogDetails = []

	for elem in Blog.objects.all() :
		blogDetails.append({"title" : elem.title, "author" : getFullName(elem.username), "date" : elem.date, "blogid" : elem.blogID, "username" : elem.username})

	return render(request, 'home.html', {'user' : WhoIsLoggedIn(request), "blogDetails" : blogDetails[::-1]})

def login(request) :
	if WhoIsLoggedIn(request) is not None :
		return redirect(homepage)

	return render(request, 'login.html')

def logout(request) :
	if not request.session.session_key:
		request.session.save()

	SessionList.objects.filter(key = request.session.session_key).delete()
	return redirect(homepage)

def signup(request) :
	if WhoIsLoggedIn(request) is not None :
		return redirect(homepage)

	return render(request, 'signup.html')

def loginrequest(request) :

	if not request.session.session_key:
		request.session.save()

	usern = request.POST.get("username", "")
	pwd = request.POST.get("password", "")

	users = User.objects.all()
	for u in users :
		if u.username == usern :
			if u.password == pwd :
				SessionList.objects.create(key = request.session.session_key, username = usern)
				return redirect(homepage)
			break
	return redirect(login)

def signuprequest(request) :

	if not request.session.session_key :
		request.session.save()

	fname = request.POST.get("fname", "")
	lname = request.POST.get("lname", "")
	usern = request.POST.get("username", "")
	pwd = request.POST.get("password", "")

	users = User.objects.all()
	for u in users :
		if u.username == usern :
			return redirect(signup)

	User.objects.create(username = usern, password = pwd, firstname = fname, lastname = lname)
	SessionList.objects.create(key = request.session.session_key, username = usern)

	return redirect(homepage)

def showBlog(request, blogid) :
	b = Blog.objects.filter(blogID = blogid)
	params = {'user' : WhoIsLoggedIn(request)}

	if b.exists() :
		print(b)
		b = b[0]
		params.update({'blogFound' : True, 'title' : b.title, 'body' : b.body, 'date' : b.date, 'author_username' : b.username, 'author_fullname' : getFullName(b.username), 'blogid' : b.blogID})
		return render(request, 'showblog.html', params)

	params.update({'blogFound' : False})

	return render(request, 'showblog.html', params)

def createBlog(request) :
	usr = WhoIsLoggedIn(request)
	if usr is not None :
		return render(request, 'createBlog.html', {'user': usr})

	return redirect(login);

def createBlogRequest(request) :
	tt = request.POST.get('title', '')
	bd = request.POST.get('body', '')
	us = request.POST.get('username', '')
	dt = request.POST.get('date', '')
	bid = 1
	if Blog.objects.all().exists() :
		bid = Blog.objects.last().blogID + 1

	Blog.objects.create(blogID = bid, username = us, title = tt, body = bd, date = dt)

	data = {'url' : reverse('blogs', kwargs={'blogid':bid})}
	return JsonResponse(data)

def editBlog(request, blogid) :
	usr = WhoIsLoggedIn(request)
	if usr is not None :
		b = Blog.objects.filter(blogID = blogid)
		if b.exists() :
			if usr.username == b[0].username :
				return render(request, 'editBlog.html', {'user': usr, 'blogDetails' : b[0]})

	return redirect(login);

def editBlogRequest(request) :
	tt = request.POST.get('title', '')
	bd = request.POST.get('body', '')
	bid = request.POST.get('blogid', None)

	if bid is not None :
		blog = Blog.objects.get(blogID = bid)
		blog.title = tt
		blog.body = bd
		blog.save()

	data = {'url' : reverse('blogs', kwargs={'blogid':bid})}
	return JsonResponse(data)

def deleteBlogRequest(request) :
	bid = request.POST.get('blogid', None)

	if bid is not None :
		Blog.objects.filter(blogID = bid).delete()

	data = {'url' : reverse('home')}
	return JsonResponse(data)
