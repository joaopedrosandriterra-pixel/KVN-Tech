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
from .models import CaseStudy, Contact, Project


def home(request):
    projects = (
        Project.objects.filter(visible=True)
        .prefetch_related('technologies')
        .order_by('-featured', '-updated_at', 'title')[:6]
    )

    services = [
        'Sites institucionais e landing pages',
        'Sistemas web e APIs',
        'Aplicativos mobile com Kotlin',
        'Automações, Docker e infraestrutura',
    ]

    return render(request, 'index.html', {'projects': projects, 'services': services})


def about(request):
    return render(request, 'about.html')


def faq(request):
    faqs = [
        {
            'question': 'Quanto custa um site?',
            'answer': 'O valor depende do tipo de projeto, das funcionalidades desejadas e da complexidade. Após uma conversa inicial, elaboramos um orçamento personalizado, sem compromisso.',
        },
        {
            'question': 'Quanto tempo leva para desenvolver um site?',
            'answer': 'O prazo varia conforme o projeto. Sites institucionais geralmente levam de 2 a 4 semanas, enquanto sistemas mais complexos podem exigir mais tempo.',
        },
        {
            'question': 'Vocês desenvolvem sistemas personalizados?',
            'answer': 'Sim. Desenvolvemos sistemas sob medida para atender às necessidades específicas de cada empresa, utilizando tecnologias modernas e escaláveis.',
        },
        {
            'question': 'Meu site funcionará em celulares?',
            'answer': 'Sim. Todos os projetos são desenvolvidos para funcionar corretamente em computadores, tablets e smartphones.',
        },
        {
            'question': 'O site será seguro?',
            'answer': 'Sim. Adotamos boas práticas de desenvolvimento, autenticação segura, proteção contra vulnerabilidades comuns e utilização de conexões HTTPS.',
        },
        {
            'question': 'Posso solicitar alterações após a entrega?',
            'answer': 'Sim. É possível solicitar ajustes e novas funcionalidades conforme a necessidade do projeto.',
        },
        {
            'question': 'Vocês fazem manutenção?',
            'answer': 'Sim. Oferecemos suporte e manutenção para manter o sistema atualizado e funcionando corretamente.',
        },
        {
            'question': 'O domínio e a hospedagem estão inclusos?',
            'answer': 'Podemos orientar na contratação ou cuidar da configuração, conforme o acordo realizado no projeto.',
        },
        {
            'question': 'Quais tecnologias vocês utilizam?',
            'answer': 'Trabalhamos principalmente com Python, Django, PostgreSQL, Docker, Tailwind CSS, HTML, CSS e JavaScript. Sempre escolhemos a tecnologia mais adequada para cada projeto.',
        },
        {
            'question': 'Como solicito um orçamento?',
            'answer': 'Basta acessar a página Contato, preencher o formulário com as informações do projeto e entraremos em contato o mais breve possível.',
        },
    ]
    return render(request, 'faq.html', {'faqs': faqs})


def cases(request):
    case_studies = CaseStudy.objects.filter(visible=True).prefetch_related('technologies').order_by('-featured', '-updated_at', 'title')
    return render(request, 'cases.html', {'case_studies': case_studies})


def case_detail(request, slug):
    case_study = get_object_or_404(
        CaseStudy.objects.prefetch_related('technologies'),
        slug=slug,
        visible=True,
    )
    return render(request, 'case_detail.html', {'case_study': case_study})


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
    contacts = Contact.objects.all()
    return render(request, 'panel.html', {'projects': projects, 'contacts': contacts})


@staff_member_required
@require_POST
def delete_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    contact.delete()
    messages.success(request, 'Solicitação excluída com sucesso.')
    return redirect('panel')


def contact_view(request):
    if request.method == 'POST':
        if not (request.user.is_authenticated and request.user.is_active):
            messages.error(request, 'Você precisa estar cadastrado, logado e verificado para enviar uma solicitação.')
            return redirect('login')

        name = request.POST.get('name', '').strip()
        company = request.POST.get('company', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        service = request.POST.get('service', '').strip()
        budget = request.POST.get('budget', '').strip()
        deadline = request.POST.get('deadline', '').strip()
        message = request.POST.get('message', '').strip()
        accept_contact = request.POST.get('accept_contact')

        if not name or not email or not service or not budget or not deadline or not message or not accept_contact:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios e aceite ser contatado.')
            return render(request, 'contact.html', {'posted_data': request.POST})

        dynamic_data = {}
        if service == 'Desenvolvimento Web':
            dynamic_data['Quantas páginas?'] = request.POST.get('web_pages', '').strip()
            dynamic_data['Já possui domínio?'] = request.POST.get('web_domain', 'Não').strip()
            dynamic_data['Tem identidade visual?'] = request.POST.get('web_visual_identity', 'Não').strip()
        elif service == 'Sistema':
            dynamic_data['Login?'] = request.POST.get('sys_login', 'Não').strip()
            dynamic_data['Banco de dados?'] = request.POST.get('sys_db', 'Não').strip()
            dynamic_data['Quantos usuários?'] = request.POST.get('sys_users', '').strip()
        elif service == 'Roblox':
            dynamic_data['Tipo do jogo?'] = request.POST.get('roblox_game_type', '').strip()
            dynamic_data['Scripts?'] = request.POST.get('roblox_scripts', 'Não').strip()
            dynamic_data['Modelagem?'] = request.POST.get('roblox_modeling', 'Não').strip()
            dynamic_data['Interface?'] = request.POST.get('roblox_ui', 'Não').strip()

        Contact.objects.create(
            name=name,
            company=company,
            email=email,
            phone=phone,
            service=service,
            budget=budget,
            deadline=deadline,
            message=message,
            dynamic_data=dynamic_data
        )

        messages.success(request, 'Sua solicitação de orçamento foi enviada com sucesso! Entraremos em contato em breve.')
        return redirect('contact')

    return render(request, 'contact.html')



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
        login(request, user)
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
