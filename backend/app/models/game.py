from tortoise import Model, fields


class Game(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255, unique=True, index=True)
    description = fields.TextField(null=True)
    genres = fields.JSONField(default=list)
    developer = fields.CharField(max_length=255, null=True, index=True)
    publisher = fields.CharField(max_length=255, null=True, index=True)
    release_year = fields.IntField()
    platforms = fields.JSONField(default=list)
    cover_image_path = fields.CharField(max_length=512, null=True)
    average_rating = fields.FloatField(default=0.0)

    reviews = fields.ReverseRelation["Review"]

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "games"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Game({self.id}): {self.title}"

    async def update_average_rating(self) -> None:
        reviews = await self.reviews.all()
        if reviews:
            total_rating = sum(review.rating for review in reviews)
            self.average_rating = round(total_rating / len(reviews), 1)
        else:
            self.average_rating = 0.0
        await self.save()

    class PydanticMeta:
        pass
