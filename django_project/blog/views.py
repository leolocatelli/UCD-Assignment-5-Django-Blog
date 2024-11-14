from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required  # Importação correta
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

# View da página inicial
def home(request):
    context = {
       'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

# Lista de postagens na página inicial com paginação
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

# Detalhe de uma postagem individual
class PostDetailView(DetailView):
    model = Post  

# Criação de postagem
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
     
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Atualização de uma postagem
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
     
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# Exclusão de uma postagem
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# View da página 'Sobre'
def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

# Lista de postagens por usuário específico
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

# Nova função para like
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Remove o like se o usuário já curtiu
    else:
        post.likes.add(request.user)  # Adiciona o like se o usuário ainda não curtiu
    return redirect('post-detail', pk=post.id)  # Corrigido para usar 'pk'

