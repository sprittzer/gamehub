from tortoise import Model, fields


class Game(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255, unique=True, index=True)
    description = fields.TextField(null=True)
    genre = fields.CharField(max_length=100, index=True)
    developer = fields.CharField(max_length=255, null=True, index=True)
    publisher = fields.CharField(max_length=255, null=True, index=True)
    release_year = fields.IntField()
    cover_image_path = fields.CharField(max_length=512, null=True)
    
    reviews = fields.ReverseRelation["Review"]

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "games"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Game({self.id}): {self.title}"
