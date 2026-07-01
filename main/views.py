from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.http import require_POST

from .forms import SignUpForm
from .models import Project


def home(request):
    projects = [
        {
            'title': 'Sistema Web com Django',
            'summary': 'Painel administrativo, autenticação e fluxo de dados organizado.',
            'tech': ['Django', 'PostgreSQL', 'Docker'],
        },
        {
            'title': 'Automação de processos',
            'summary': 'Scripts e integrações para reduzir esforço manual e ganhar agilidade.',
            'tech': ['Python', 'APIs', 'Linux'],
        },
        {
            'title': 'Experiência em Roblox',
            'summary': 'Sistemas, NPCs, combate e UI com foco em gameplay e performance.',
            'tech': ['Roblox', 'Lua', 'UI'],
        },
    ]

    services = [
        'Sites institucionais e landing pages',
        'Sistemas web e APIs',
        'Aplicativos mobile com Kotlin',
        'Automações, Docker e infraestrutura',
    ]

    return render(request, 'index.html', {'projects': projects, 'services': services})


def about(request):
    return render(request, 'about.html')


def laboratory(request):
    projects = (
        Project.objects.filter(visible=True)
        .prefetch_related('technologies', 'roadmap_items', 'updates')
    )
    return render(request, 'laboratory.html', {'projects': projects})


def project_detail(request, slug):
    project = get_object_or_404(
        Project.objects.prefetch_related('technologies', 'roadmap_items', 'updates', 'images'),
        slug=slug,
        visible=True,
    )
    stats = {
        'roadmap_total': project.total_roadmap_count,
        'roadmap_done': project.completed_roadmap_count,
        'updates': project.updates.count(),
        'technologies': project.technologies.count(),
        'images': project.images.count(),
    }
    return render(request, 'project_detail.html', {'project': project, 'stats': stats})


@staff_member_required
def panel(request):
    projects = Project.objects.all().prefetch_related('technologies')
    return render(request, 'panel.html', {'projects': projects})


def _apply_input_classes(form):
    for field in form.visible_fields():
        autocomplete = {
            'username': 'username',
            'email': 'email',
            'password': 'current-password',
            'password1': 'new-password',
            'password2': 'new-password',
            'full_name': 'name',
        }.get(field.name, 'off')
        field.field.widget.attrs.update({
            'class': 'mt-2 block w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none transition focus:border-cyan-400 focus:ring-2 focus:ring-cyan-500/20',
            'autocomplete': autocomplete,
        })


def _safe_next_url(request):
    next_url = request.POST.get('next') or request.GET.get('next')
    if url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return None


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Bem-vindo de volta!')
            return redirect(_safe_next_url(request) or 'home')
    else:
        form = AuthenticationForm(request)

    _apply_input_classes(form)
    return render(request, 'registration/login.html', {
        'form': form,
        'next': _safe_next_url(request) or '',
    })


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu com sucesso.')
    return redirect('home')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    _send_activation_email(request, user)
            except Exception:
                messages.error(request, 'Não foi possível enviar o e-mail de ativação agora. Tente novamente em instantes.')
            else:
                return render(request, 'registration/activation_sent.html', {'email': user.email})
    else:
        form = SignUpForm()

    _apply_input_classes(form)
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    user = None
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and user.is_active:
        return render(request, 'registration/activation_complete.html')

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=['is_active'])
        return render(request, 'registration/activation_complete.html')

    return render(request, 'registration/activation_invalid.html')


def _send_activation_email(request, user):
    context = {
        'user': user,
        'domain': request.get_host(),
        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    }
    subject = 'Ative sua conta no KVN Tech'
    message = render_to_string('registration/activation_email.html', context)
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.send(fail_silently=False)
