from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from django.shortcuts import render
from django.http import HttpResponse
from .models import Project, Certificate, Education


from .models import (
    Project, Certificate, Experience, Education,
    Skill, Interest, SocialLink
)

def home(request):
    featured_projects = Project.objects.filter(featured=True)[:3]

    featured_certificates = Certificate.objects.order_by(
        "-date_issued"
    )[:3]

    latest_education = Education.objects.order_by(
        "-start_year"
    )[:1]

    latest_experience = Experience.objects.order_by(
        "-start_date"
    )[:2]

    skills = Skill.objects.all()
    interests = Interest.objects.all()

    return render(request, 'portfolio/home.html', {
        'featured_projects': featured_projects,
        'featured_certificates': featured_certificates,
        'latest_education': latest_education,
        'latest_experience': latest_experience,
        'skills': skills,
        'interests': interests,
    })

def about(request):
    experiences = Experience.objects.all()
    educations = Education.objects.all()
    skills = Skill.objects.all()
    interests = Interest.objects.all()
    return render(request, 'portfolio/about.html', {
        'experiences': experiences,
        'educations': educations,
        'skills': skills,
        'interests': interests,
    })

def projects(request):
    category = request.GET.get('category', 'all')
    all_projects = Project.objects.all().order_by('-date')
    if category != 'all':
        filtered = all_projects.filter(category=category)
    else:
        filtered = all_projects
    return render(request, 'portfolio/projects.html', {
        'projects': filtered,
        'active_category': category,
    })

def certificates(request):
    certificates = Certificate.objects.all().order_by('-date_issued')
    return render(request, 'portfolio/certificates.html', {
        'certificates': certificates,
    })

def education(request):
    educations = Education.objects.all()
    experiences = Experience.objects.all()
    return render(request, 'portfolio/education.html', {
        'educations': educations,
        'experiences': experiences,
    })

def contact(request):
    social_links = SocialLink.objects.all()
    return render(request, 'portfolio/contact.html', {
        'social_links': social_links,
    })
def generate_resume(request):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    from django.http import HttpResponse
    from collections import defaultdict

    educations  = Education.objects.all()
    experiences = Experience.objects.all()
    skills      = Skill.objects.all()
    certs       = Certificate.objects.all().order_by('-date_issued')[:8]
    projects    = Project.objects.all().order_by('-date')[:3]

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Don_Denny_Mathew_Resume.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # ── COLORS ──────────────────────────────────
    BLACK   = (0.10, 0.10, 0.10)
    BLUE    = (0.10, 0.40, 0.70)
    MUTED   = (0.35, 0.35, 0.35)
    WHITE   = (1.00, 1.00, 1.00)

    def fc(*rgb):
        p.setFillColorRGB(*rgb)

    def sc(*rgb):
        p.setStrokeColorRGB(*rgb)

    # white background
    fc(*WHITE)
    p.rect(0, 0, width, height, fill=1, stroke=0)

    y = height - 14*mm

    def check(y, need=12*mm):
        return y if y > need else need

    def wrap(text, font, size, max_w):
        words = text.split()
        lines, line = [], ""
        for w in words:
            test = f"{line} {w}".strip()
            if p.stringWidth(test, font, size) <= max_w:
                line = test
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)
        return lines

    def section(title, y):
        y -= 3*mm
        p.setFont("Helvetica-Bold", 9)
        fc(*BLUE)
        p.drawString(15*mm, y, title.upper())
        sc(*BLUE)
        p.setLineWidth(0.6)
        p.line(15*mm, y - 2, width - 15*mm, y - 2)
        fc(*BLACK)
        return y - 7*mm

    # ── HEADER ──────────────────────────────────
    p.setFont("Helvetica-Bold", 20)
    fc(*BLACK)
    p.drawCentredString(width/2, y, "Don Denny Mathew")
    y -= 7*mm

    p.setFont("Helvetica", 9)
    fc(*MUTED)
    p.drawCentredString(width/2, y,
        "Full Stack Developer  |  B.Tech Student, RSET Kakkanad")
    y -= 5*mm

    p.setFont("Helvetica", 8.5)
    fc(*BLUE)
    p.drawCentredString(width/2, y,
        "don.denny@gmail.com   ·   Vazhakulam, Ernakulam   ·   Open for Internships")
    y -= 5*mm

    # thin divider under header
    sc(*MUTED)
    p.setLineWidth(0.4)
    p.line(15*mm, y, width - 15*mm, y)
    y -= 3*mm

    # ── WORK EXPERIENCE ─────────────────────────
    y = section("Work Experience", y)

    if experiences:
        for exp in experiences:
            y = check(y)
            p.setFont("Helvetica-Bold", 9.5)
            fc(*BLACK)
            p.drawString(15*mm, y, exp.company)

            p.setFont("Helvetica", 8.5)
            fc(*MUTED)
            end = "Present" if exp.is_current else (exp.end_date.strftime("%b %Y") if exp.end_date else "")
            p.drawRightString(width - 15*mm, y,
                f"{exp.start_date.strftime('%b %Y')} - {end}")
            y -= 5*mm

            p.setFont("Helvetica-Oblique", 8.5)
            fc(*MUTED)
            loc = f"  |  {exp.location}" if exp.location else ""
            p.drawString(15*mm, y, f"{exp.role}{loc}")
            y -= 5*mm

            p.setFont("Helvetica", 8.5)
            fc(*MUTED)
            for line in wrap(exp.description, "Helvetica", 8.5, width - 38*mm):
                y = check(y)
                p.drawString(18*mm, y, f"• {line}")
                y -= 4.5*mm
            y -= 3*mm
    else:
        p.setFont("Helvetica", 8.5)
        fc(*MUTED)
        p.drawString(15*mm, y, "Add experience in Django admin.")
        y -= 8*mm

    # ── EDUCATION ───────────────────────────────
    y = section("Education", y)

    for edu in educations:
        y = check(y)
        p.setFont("Helvetica-Bold", 9.5)
        fc(*BLACK)
        p.drawString(15*mm, y, edu.institution)

        p.setFont("Helvetica", 8.5)
        fc(*MUTED)
        end = "Present" if edu.is_current else str(edu.end_year or "")
        p.drawRightString(width - 15*mm, y, f"{edu.start_year} - {end}")
        y -= 5*mm

        p.setFont("Helvetica-Oblique", 8.5)
        fc(*MUTED)
        degree = f"{edu.degree}{' in ' + edu.field if edu.field else ''}"
        p.drawString(15*mm, y, degree)
        y -= 7*mm

    # ── PROJECTS ────────────────────────────────
    y = section("Projects", y)

    if projects:
        for proj in projects:
            y = check(y)

            p.setFont("Helvetica-Bold", 9.5)
            fc(*BLUE)
            p.drawString(15*mm, y, proj.title)

            p.setFont("Helvetica", 8)
            fc(*MUTED)
            p.drawRightString(width - 15*mm, y, proj.date.strftime("%Y"))
            y -= 5*mm

            p.setFont("Helvetica", 8.5)
            fc(*MUTED)
            # single clean paragraph
            for line in wrap(proj.description, "Helvetica", 8.5, width - 38*mm):
                y = check(y)
                p.drawString(15*mm, y, line)
                y -= 4.5*mm

            # tech stack line
            y -= 1*mm
            p.setFont("Helvetica-Oblique", 8)
            fc(*BLUE)
            p.drawString(15*mm, y, f"Tech: {proj.tech}")
            y -= 6*mm
    else:
        p.setFont("Helvetica", 8.5)
        fc(*MUTED)
        p.drawString(15*mm, y, "Add projects in Django admin.")
        y -= 8*mm

    # ── SKILLS ──────────────────────────────────
    y = section("Skills", y)

    grouped = defaultdict(list)
    for s in skills:
        grouped[s.get_category_display()].append(s.name)

    cat_labels = {
        'Programming Language': 'Languages',
        'Framework / Library':  'Frameworks',
        'Tool / Software':      'Tools',
        'Design':               'Design',
        'Other':                'Other',
    }

    for cat, names in grouped.items():
        y = check(y)
        p.setFont("Helvetica-Bold", 8.5)
        fc(*BLACK)
        label = cat_labels.get(cat, cat)
        p.drawString(15*mm, y, f"{label}:")

        p.setFont("Helvetica", 8.5)
        fc(*MUTED)
        p.drawString(42*mm, y, ", ".join(names))
        y -= 5.5*mm

    y -= 2*mm

    # ── CERTIFICATIONS ──────────────────────────
    y = section("Certifications", y)

    if certs:
        for cert in certs:
            y = check(y)
            p.setFont("Helvetica-Bold", 8.5)
            fc(*BLACK)
            p.drawString(15*mm, y, cert.name)

            p.setFont("Helvetica", 8)
            fc(*MUTED)
            p.drawRightString(width - 15*mm, y,
                cert.date_issued.strftime("%b %Y"))
            y -= 4.5*mm

            p.setFont("Helvetica-Oblique", 8)
            fc(*BLUE)
            p.drawString(15*mm, y, cert.organization)
            y -= 6*mm
    else:
        p.setFont("Helvetica", 8.5)
        fc(*MUTED)
        p.drawString(15*mm, y, "Add certificates in Django admin.")
        y -= 8*mm

    p.save()
    return response