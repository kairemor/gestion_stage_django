from django.db import models


CONVENTION_STATE = (
    ('R', 'Convention en cours'),
    ('S', 'Convention suspendue'),
    ('E', 'Convention expiree')
)


class Enterprise(models.Model):
    name = models.CharField(max_length=50, default="")
    field = models.CharField(max_length=100, default="")
    email = models.EmailField(max_length=50, default="")
    website = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=100, default="")
    logo = models.ImageField(upload_to="logo_enterprise", null=True)
    phone = models.IntegerField()
    leader_name = models.CharField(max_length=50, default="")
    is_partner = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    add_date = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.name


class Convention(models.Model):
    title = models.CharField(max_length=60, default="")
    enterprise = models.OneToOneField(
        Enterprise, on_delete=models.CASCADE)
    life_time = models.IntegerField(default=0)
    state = models.CharField(max_length=50, choices=CONVENTION_STATE)
    starting_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
