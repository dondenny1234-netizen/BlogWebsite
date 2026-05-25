from django.db import models

class Certificate(models.Model):
    name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    date_issued = models.DateField()
    details = models.TextField(blank=True, null=True)

    image = models.ImageField(
        upload_to='certificates/',
        blank=True,
        null=True
    )

    credential_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Experience(models.Model):
    role         = models.CharField(max_length=200)
    company      = models.CharField(max_length=200)
    location     = models.CharField(max_length=100, blank=True)
    start_date   = models.DateField()
    end_date     = models.DateField(null=True, blank=True)
    is_current   = models.BooleanField(default=False)
    description  = models.TextField()

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.role} at {self.company}"


class Education(models.Model):
    institution  = models.CharField(max_length=200)
    degree       = models.CharField(max_length=200)
    field        = models.CharField(max_length=200, blank=True)
    start_year   = models.IntegerField()
    end_year     = models.IntegerField(null=True, blank=True)
    is_current   = models.BooleanField(default=False)
    description  = models.TextField(blank=True)
    image        = models.ImageField(upload_to='education/', blank=True, null=True)  # ← ADD THIS

    class Meta:
        ordering = ['-start_year']

    def __str__(self):
        return f"{self.degree} — {self.institution}"

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('language',  'Programming Language'),
        ('framework', 'Framework / Library'),
        ('tool',      'Tool / Software'),
        ('design',    'Design'),
        ('other',     'Other'),
    ]
    name     = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    level    = models.IntegerField(default=80, help_text="Proficiency 0–100")
    order    = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    tech = models.CharField(max_length=200)

    # ADD THESE:
    date = models.DateField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Interest(models.Model):
    name  = models.CharField(max_length=100)
    icon  = models.CharField(max_length=10, blank=True, help_text="Emoji icon")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('github',   'GitHub'),
        ('linkedin', 'LinkedIn'),
        ('behance',  'Behance'),
        ('twitter',  'Twitter / X'),
        ('instagram','Instagram'),
        ('youtube',  'YouTube'),
        ('website',  'Personal Website'),
        ('other',    'Other'),
    ]
    platform    = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url         = models.URLField()
    display_name = models.CharField(max_length=100, blank=True)
    order       = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.platform}: {self.url}"