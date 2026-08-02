from portfolio.models import Project, Certificate, Education


def fix_images(model):
    for obj in model.objects.all():
        if obj.image and obj.image.name.startswith("media/"):
            obj.image.name = obj.image.name.replace("media/", "", 1)
            obj.save()
            print("Fixed:", obj.image.name)


fix_images(Certificate)
fix_images(Education)
fix_images(Project)

print("DONE")