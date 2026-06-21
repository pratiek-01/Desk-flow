from django.db import models
from django.contrib.auth.models import User


# Choices reused in both models
ASSET_TYPE_CHOICES = [
    ('Laptop', 'Laptop'),
    ('Mouse', 'Mouse'),
    ('Keyboard', 'Keyboard'),
    ('Monitor', 'Monitor'),
    ('Chair', 'Chair'),
    ('Mobile', 'Mobile'),
    ('Software License', 'Software License'),
    ('Other', 'Other'),
]


class Asset(models.Model):
    """
    Represents one physical/software item in the company.
    Example: 'Lenovo ThinkPad #12' -> Laptop -> Assigned to 'Rahul'
    """
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Assigned', 'Assigned'),
    ]

    name = models.CharField(max_length=100)  # e.g. "Lenovo ThinkPad #12"
    asset_type = models.CharField(max_length=30, choices=ASSET_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    assigned_to = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='assigned_assets'
    )

    def __str__(self):
        return f"{self.name} ({self.asset_type})"


class RequestTicket(models.Model):
    """
    An employee raises this when they need a new asset.
    Admin then approves or rejects it.
    """
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    asset_type = models.CharField(max_length=30, choices=ASSET_TYPE_CHOICES)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest tickets first

    def __str__(self):
        return f"{self.user.username} - {self.asset_type} - {self.status}"
