from django.db import models
from users.models import CustomUser

Status_Choices = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class Blog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=Status_Choices, default = 'pending')
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class SiteSettings(models.Model):
    logo = models.ImageField(upload_to='site_logo/', null= True, blank= True)

    def __str__(self):
        return "Site Settings"

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'blog')

    def __str__(self):
        return f"{self.user} liked {self.blog}"

# ✅ Add this Comment model
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name if self.user else 'Anonymous'} - {self.content[:20]}"