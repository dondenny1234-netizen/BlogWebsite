from portfolio.models import Project, Certificate, Education

print("PROJECTS")
for x in Project.objects.all():
    print(x.title, "=>", x.image.name, "=>", x.image.url)

print("CERTIFICATES")
for x in Certificate.objects.all():
    print(x.name, "=>", x.image.name, "=>", x.image.url)

print("EDUCATION")
for x in Education.objects.all():
    print(x.name, "=>", x.image.name, "=>", x.image.url)