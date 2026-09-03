from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15
    )

    department = models.CharField(
        max_length=100
    )

    role = models.CharField(
        max_length=100
    )

    joining_date = models.DateField()

    def __str__(self):
        return f"{self.employee_id} - {self.name}"


class Asset(models.Model):

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Assigned", "Assigned"),
        ("Repair", "Repair"),
    ]

    ASSET_TYPES = [
        ("Laptop", "Laptop"),
        ("Desktop", "Desktop"),
        ("Monitor", "Monitor"),
        ("Printer", "Printer"),
        ("Phone", "Phone"),
        ("Other", "Other"),
        ("Server", "Server"),
        ("Tablet", "Tablet"),
        ("Keyboard", "Keyboard"),
        ("Mouse", "Mouse"),
    ]

    asset_name = models.CharField(
        max_length=100
    )

    asset_id = models.CharField(
        max_length=30,
        unique=True
    )

    asset_tag = models.CharField(
        max_length=30,
        unique=True
    )

    asset_type = models.CharField(
        max_length=30,
        choices=ASSET_TYPES
    )

    brand = models.CharField(
        max_length=100
    )

    model = models.CharField(
        max_length=100
    )

    serial_number = models.CharField(
        max_length=100,
        unique=True
    )

    purchase_date = models.DateField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Available"
    )

    assigned_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assets"
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.asset_id} - {self.asset_name}"


class Activity(models.Model):

    ACTION_CHOICES = [
        ("Employee Added", "Employee Added"),
        ("Employee Updated", "Employee Updated"),

        ("Asset Added", "Asset Added"),
        ("Asset Assigned", "Asset Assigned"),
        ("Asset Returned", "Asset Returned"),
        ("Sent for Repair", "Sent for Repair"),
        ("Repair Completed", "Repair Completed"),
        ("Asset Updated", "Asset Updated"),
        ("Asset Deleted", "Asset Deleted"),

        ("Login", "Login"),
        ("Logout", "Logout"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activities"
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activities"
    )

    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES
    )

    description = models.TextField(
        blank=True
    )

    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="performed_activities"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        if self.employee:
            target = self.employee.employee_id

        elif self.asset:
            target = self.asset.asset_id

        else:
            target = "System"

        return f"{self.action} - {target}"