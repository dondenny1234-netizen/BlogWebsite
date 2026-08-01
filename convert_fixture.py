import json

files = {
    "Education.json": "portfolio.education",
    "Project.json": "portfolio.project",
    "Certificate.json": "portfolio.certificate",
    "Experience.json": "portfolio.experience",
    "Skill.json": "portfolio.skill",
    "Interest.json": "portfolio.interest",
    "SocialLink.json": "portfolio.sociallink",
}

for filename, model in files.items():

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        fixture = []

        for item in data:
            pk = item.pop("id")

            fixture.append({
                "model": model,
                "pk": int(pk),
                "fields": item
            })

        output = filename.replace(".json", "_fixture.json")

        with open(output, "w", encoding="utf-8") as f:
            json.dump(fixture, f, indent=2)

        print("Created:", output)

    except FileNotFoundError:
        print("Skipped:", filename)