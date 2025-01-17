from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from users.models import Company, Customer

#Rating model

# Rating model
class Rating(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='service_ratings') 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_ratings') 
    rating_value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating value between 1 and 5"
    )
    review = models.TextField(null=True, blank=True, help_text="Write an optional review")
    date_rated = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['service', 'customer']

    def __str__(self):
        return f"Rating for {self.service.name} by {self.customer.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update service's average rating
        self.service.update_average_rating()

# Service model 
class Service(models.Model):
    FIELD_CHOICES = [
        ('Air Conditioner', 'Air Conditioner'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('House Keeping', 'House Keeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=10)
    rating = models.IntegerField(default=0)
    field = models.CharField(max_length=30, choices=FIELD_CHOICES)
    date = models.DateTimeField(default=timezone.now)  # Correct field name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure the service field matches the company's field of work
        if self.company.field != 'All in One' and self.company.field != self.field:
            raise ValueError(f"This company can only provide {self.company.field} services.")
        super().save(*args, **kwargs)

#method to get average rating
    @property
    def average_rating(self):
        ratings = self.service_ratings.all()
        total_ratings = ratings.count()
        if total_ratings == 0:
            return 0
        total_score = sum([rating.rating_value for rating in ratings])
        return total_score / total_ratings

#method to update avrage rating
    def update_average_rating(self):
        self.rating = self.average_rating
        self.save()

class ServiceRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='requests')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    address = models.CharField(max_length=200)
    service_time = models.IntegerField(help_text="Time in hours")
    date_requested = models.DateTimeField(auto_now_add=True)
    rating= models.ForeignKey(Rating, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_requests')

    @property
    def total_cost(self):
        return self.service.price_hour * self.service_time

    def __str__(self):
        return f"{self.customer.user.username} - {self.service.name}"