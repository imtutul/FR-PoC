from django.db import models

def employee_image_path(instance, filename):
    return f'employee_images/{instance.employee.id}/{filename}'

class Employee(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.designation}"

class EmployeeImage(models.Model):
    employee = models.ForeignKey(Employee, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=employee_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
