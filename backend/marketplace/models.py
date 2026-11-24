from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('pottery', 'Pottery & Ceramics'),
        ('textiles', 'Textiles & Handloom'),
        ('woodwork', 'Woodwork & Carving'),
        ('metalwork', 'Metalwork & Brass'),
        ('jewelry', 'Handcrafted Jewelry'),
        ('leather', 'Leather Craft'),
        ('painting', 'Paintings & Folk Art'),
        ('basketry', 'Basketry & Natural Fibers'),
        ('stonecraft', 'Stone & Marble Craft'),
        ('other', 'Other Handmade Crafts'),
    ]

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    location = models.CharField(max_length=150)
    image = models.ImageField(upload_to='products/%Y/%m/')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['seller', 'is_available']),
            models.Index(fields=['category', 'is_available']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return f"{self.name} by {self.seller.get_full_name()}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='additional_images',
    )
    image = models.ImageField(upload_to='products/gallery/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Gallery image for {self.product.name}"


class Enquiry(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
        COMPLETED = 'completed', 'Completed'

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_enquiries',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='enquiries',
    )
    message = models.TextField()
    seller_response = models.TextField(blank=True, default='')
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
    )
    responded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Enquiries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', 'status']),
            models.Index(fields=['buyer', 'created_at']),
        ]

    def __str__(self):
        return f"Enquiry #{self.id} on {self.product.name} ({self.status})"