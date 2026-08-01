from portfolio.models import Project

print("Checking Project images...")

for p in Project.objects.all():
    print(
        p.title,
        "NAME:",
        p.image.name,
        "URL:",
        p.image.url
    )