from django.shortcuts import render,HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request,'home/home.html')
def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        roll=request.POST['roll']
        content=request.POST['content']
        print(name,email,roll,content)

        if len(name)<2 or len(roll)<5 or len(email)<3:
            messages.error(request,'Please Fill The Form Correctly')
        else:
            contact= Contact(name=name,email=email,roll=roll,content=content)
            contact.save()
            messages.success(request,'Your Response Recorded, wait for admin verification.')
    
    return render(request,'home/contact.html')
def about(request):
    messages.success(request,"About Us")
    
    return render(request,'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsAuthor)
    if allPosts.count() == 0:
        messages.warning(request,"Opps ! Nothing found ")    
    params = {'allPosts':allPosts ,'query':query}
    return render(request, 'home/search.html', params)
def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username)>15:
            messages.error(request, "Your iLearn must be under 15 characters")
            return redirect('home')
        #username should only contain letters and numbers
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers")
            return redirect('home')
        #password 1 and password 2 need to match
        if pass1 != pass2:
            messages.success(request, "confirm password does no match")
            return redirect('home')

        #create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iLearn account has been successfully created !!")
        return redirect('home')
    else:
        return HttpResponse("404 - Not Found")

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username = loginusername, password = loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged in ")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials, please try again ")
            return redirect('home')
    
    return HttpResponse('404 - Not Found')

def handleLogout(request):
    #if request.method == 'POST':
        logout(request)
        messages.success(request, "Successfully Logged Out")
        return redirect('home')
    
    