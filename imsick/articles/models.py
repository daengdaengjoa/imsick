from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=20, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles")

    def __self__(self):
        return self.title


class Like(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("account", "article")

    def __str__(self):
        return f"{self.account} likes {self.article}"

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, related_name="replies")
