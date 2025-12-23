from tortoise import Model, fields

class Review(Model):
    id = fields.IntField(pk=True)
    game = fields.ForeignKeyField(
        "models.Game", 
        related_name="reviews", 
        on_delete=fields.CASCADE
    )
    ip_address = fields.CharField(max_length=45)
    rating = fields.IntField(min_value=1, max_value=5)
    text = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "reviews"
        unique_together = (("game", "ip_address"),)
        ordering = ["-created_at"]
