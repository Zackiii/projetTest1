from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Post
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import PostForm
from django.shortcuts import render, get_object_or_404



def accueil(request):

    search_query = request.GET.get('search')
    print('333333333333333333333333333')
    print(search_query)
    posts = Post.objects.all()
    # if search_query:
    #     posts_search = Post.objects.filter(Q(title__incontains = search_query)|Q(title__areaHash__incontains = search_query))
    context = {
        'posts': posts,
        # 'posts':posts_search,
    }
    return render(request, 'userTests/accueil.html', context)

# login

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not email or not password:
            messages.error(
                request, 'Veuillez fournir un e-mail et un mot de passe valides.')
            return redirect('user_login')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('accueil')
        else:
            messages.error(
                request, 'Les informations d\'identification fournies ne sont pas valides.')
            return redirect('user_login')

    return render(request, 'userTests/user_login.html', {})


# register

def sing_up(request):
    error = False
    message = ""
    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        # Email
        try:
            validate_email(email)
        except:
            error = True
            message = "Enter un email valide svp!"
        # password
        if error == False:
            if password != repassword:
                error = True
                message = "Les deux mot de passe ne correspondent pas!"
        # Exist
        user = User.objects.filter(Q(email=email) | Q(username=name)).first()
        if user:
            error = True
            message = f"Un utilisateur avec email {email} ou le nom d'utilisateur {name} exist déjà'!"

        # register
        if error == False:
            user = User(
                username=name,
                email=email,
            )
            user.save()

            user.password = password
            user.set_password(user.password)
            user.save()

            return redirect('user_login')

            #print("=="*5, " NEW POST: ",name,email, password, repassword, "=="*5)

    context = {
        'error': error,
        'message': message
    }
    return render(request, 'userTests/register.html', context)


# deconnexion

def log_out(request):
    logout(request)
    return redirect('accueil')


# Affichage actualite
def news(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,

    }
    return render(request, 'userTests/news.html', {})


# Ajouter actualite

@login_required(login_url='/user_login')
def getNews(request):
    author = request.user
    # print('authorauthorauthorauthorauthorauthor')
    # print(author.name)
    # print('authorauthorauthorauthorauthor')
    posts = Post
    if request.method == "POST":
        title = request.POST['titre']
        text = request.POST['text']
        thumbnail = request.POST['thumbnail']

        posts = Post.objects.create(
            title=title, text=text, thumbnail=thumbnail, author=author)

        posts.save()

    return redirect('/')


# supprimer actualite @login_required(login_url='/login')
@login_required(login_url='/user_login')
def actu_delete(request, posts_id):
    posts_id = int(posts_id)
    try:
        posts = Post.objects.get(id=posts_id)
    except Post.DoesNotExist:
        return redirect('accueil')
    posts.delete()
    return redirect('deleteConfirm', post_id=posts_id)



@login_required(login_url='/user_login')
def deleteConfirm(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {'post': post}
    if request.method == "POST":
        post.delete()
        return redirect('accueil')
    return render(request, 'delete_confirm.html', context)



# @login_required(login_url='/login')
# def updateActu(request,post_id):
#       posts = Post.objects.get(id = post_id)
#       return render(request,'updateActu.html',{'posts':posts})


@login_required(login_url='/user_login')
def update(request, post_id):
    posts = Post.objects.get(id=post_id)
    context = {
        'posts': posts, }

    return render(request, 'userTests/updateActu.html', context)
    # form=detailsform(request.POST,instance=posts)


@login_required(login_url='/user_login')
def updateActu(request, post_id):
    post_id = int(post_id)
    posts = Post.objects.get(id=post_id)

    if request.method == 'POST':
        title = request.POST['titre']
        text = request.POST['text']
        posts.title = title
        posts.text = text
        posts.save()
        return redirect('accueil')

    context = {
        'posts': posts,
    }
    return render(request, 'userTests/accueil.html', context)
