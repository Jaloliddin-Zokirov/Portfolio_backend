import uuid

class SaveMediaFile(object):
    def sertificate_image(self, filename):
        return f"sertificate_images/{uuid.uuid4()}/{filename}"

    def skill_image(self, filename):
        return f"skill_images/{uuid.uuid4()}/{filename}"
    
    def portfolio_image(self, filename):
        return f"portfolio_images/{uuid.uuid4()}/{filename}"
        