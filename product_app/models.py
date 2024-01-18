from django.db import models
from django.contrib.auth.models import User
# Create your models here.
SIZE_CHOICES = (('sm', 'sm'), ('md', 'md'), ('lg', 'lg'),
                ('xl', 'xl'), ('xxl', 'xxl'))

COLOR_CHOICES = (('red', 'red'),
                 ('yellow', 'yellow'),
                 ('green', 'green'),
                 ('black', 'black'),
                 ('off-white', 'off-white'),
                 ('blue', 'blue'),
                 ('violet', 'violet'),
                 ('orange', 'orange'),
                 ('sky-blue', 'sky-blue'),)

RATING_CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.category}"


class Clothes(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='media/clothes')
    price = models.DecimalField(decimal_places=2, max_digits=12)
    stock_quantity = models.IntegerField()
    description = models.TextField(max_length=400)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.CharField(choices=SIZE_CHOICES, max_length=6)
    color = models.CharField(choices=COLOR_CHOICES, max_length=20)
    pro_rating = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return f"{self.title}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Clothes, on_delete=models.CASCADE)


class Review(models.Model):
    product = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    review = models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product}'s review"


class Rating(models.Model):
    product = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product}'s rating"


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Clothes, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username}'s wishes product"
