from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Technology(models.Model):
    name = models.CharField('nome', max_length=60, unique=True)
    color = models.CharField('cor', max_length=20, default='#22d3ee')

    class Meta:
        ordering = ['name']
        verbose_name = 'tecnologia'
        verbose_name_plural = 'tecnologias'

    def __str__(self):
        return self.name


class CaseStudy(models.Model):
    title = models.CharField('nome do case', max_length=140)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    client_name = models.CharField('cliente', max_length=140)
    segment = models.CharField('segmento', max_length=80, blank=True)
    challenge = models.TextField('desafio', blank=True)
    solution = models.TextField('solução', blank=True)
    results = models.TextField('resultado', blank=True)
    technologies = models.ManyToManyField(Technology, related_name='cases', blank=True)
    testimonial = models.TextField('avaliação do cliente', blank=True)
    testimonial_author = models.CharField('autor da avaliação', max_length=120, blank=True)
    gallery_description = models.TextField('descrição da galeria', blank=True)
    visible = models.BooleanField('visível', default=True)
    featured = models.BooleanField('destaque', default=False)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        ordering = ['-featured', '-updated_at', 'title']
        verbose_name = 'case'
        verbose_name_plural = 'cases'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 2
            while CaseStudy.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('case_detail', kwargs={'slug': self.slug})


class Project(models.Model):
    class Status(models.TextChoices):
        PLANNING = 'planning', 'Planejamento'
        DEVELOPMENT = 'development', 'Desenvolvimento'
        BETA = 'beta', 'Beta'
        FINISHED = 'finished', 'Finalizado'

    title = models.CharField('nome', max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    short_description = models.CharField('descricao curta', max_length=220)
    full_description = models.TextField('descricao completa')
    thumbnail = models.FileField('imagem de capa', upload_to='projects/covers/', blank=True)
    github = models.URLField('GitHub', blank=True)
    demo = models.URLField('demo', blank=True)
    status = models.CharField('status', max_length=20, choices=Status.choices, default=Status.PLANNING)
    progress = models.PositiveSmallIntegerField('progresso', default=0)
    visible = models.BooleanField('visivel', default=True)
    featured = models.BooleanField('destaque', default=False)
    technologies = models.ManyToManyField(Technology, related_name='projects', blank=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        ordering = ['-featured', '-updated_at', 'title']
        verbose_name = 'projeto'
        verbose_name_plural = 'projetos'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 2
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        self.progress = max(0, min(self.progress, 100))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

    @property
    def completed_roadmap_count(self):
        return self.roadmap_items.filter(status=RoadmapItem.Status.DONE).count()

    @property
    def total_roadmap_count(self):
        return self.roadmap_items.count()


class RoadmapItem(models.Model):
    class Status(models.TextChoices):
        DONE = 'done', 'Concluído'
        IN_PROGRESS = 'in_progress', 'Em andamento'
        PENDING = 'pending', 'Pendente'

    project = models.ForeignKey(Project, related_name='roadmap_items', on_delete=models.CASCADE)
    title = models.CharField('titulo', max_length=120)
    description = models.CharField('descricao', max_length=240, blank=True)
    status = models.CharField('status', max_length=20, choices=Status.choices, default=Status.PENDING)
    order = models.PositiveSmallIntegerField('ordem', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'etapa do roadmap'
        verbose_name_plural = 'etapas do roadmap'

    def __str__(self):
        return f'{self.project} - {self.title}'


class ProjectUpdate(models.Model):
    project = models.ForeignKey(Project, related_name='updates', on_delete=models.CASCADE)
    title = models.CharField('titulo', max_length=120)
    content = models.TextField('conteudo')
    image = models.FileField('imagem', upload_to='projects/updates/', blank=True)
    created_at = models.DateField('data')

    class Meta:
        ordering = ['-created_at', '-id']
        verbose_name = 'atualizacao'
        verbose_name_plural = 'atualizacoes'

    def __str__(self):
        return f'{self.project} - {self.title}'


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.FileField('imagem', upload_to='projects/gallery/')
    caption = models.CharField('legenda', max_length=160, blank=True)
    order = models.PositiveSmallIntegerField('ordem', default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'imagem do projeto'
        verbose_name_plural = 'imagens do projeto'

    def __str__(self):
        return self.caption or f'Imagem de {self.project}'


class Contact(models.Model):
    name = models.CharField('Nome', max_length=100)
    company = models.CharField('Empresa', max_length=100, blank=True)
    email = models.EmailField('E-mail')
    phone = models.CharField('Telefone', max_length=20, blank=True)
    service = models.CharField('Serviço', max_length=50)
    budget = models.CharField('Orçamento previsto', max_length=30)
    deadline = models.CharField('Prazo', max_length=30)
    message = models.TextField('Conte sobre seu projeto')
    dynamic_data = models.JSONField('Perguntas adicionais', default=dict, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Solicitação'
        verbose_name_plural = 'Solicitações'

    def __str__(self):
        return f"{self.name} - {self.service} ({self.created_at.strftime('%d/%m/%Y')})"

