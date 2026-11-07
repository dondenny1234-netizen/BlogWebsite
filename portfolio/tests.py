from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Resume


@override_settings(
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {"base_url": "/media/"},
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
)
class ResumeDisplayTests(TestCase):
    def test_homepage_shows_admin_uploaded_resume_link(self):
        resume = Resume.objects.create(
            title="Current Resume",
            file="resume/current-resume.pdf",
        )

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Download Resume")
        self.assertContains(response, resume.file.url)
        self.assertNotContains(response, "Resume Coming Soon")

    def test_homepage_shows_coming_soon_when_no_resume_exists(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Resume Coming Soon")

    def test_cloudinary_debug_endpoint_is_not_exposed(self):
        response = self.client.get("/debug/")
        self.assertEqual(response.status_code, 404)

    def test_contact_page_uses_uploaded_resume(self):
        resume = Resume.objects.create(
            title="Current Resume",
            file="resume/current-resume.pdf",
        )

        response = self.client.get(reverse("contact"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, resume.file.url)
        self.assertContains(response, "Download Resume")
