from django.db import models

class Booking(models.Model):
    
    class StudentDepartment(models.TextChoices):
        CYBERSECURITY = 'CYB', 'Cybersecurity'
        SOFTWARE_ENGINEERING = 'SWE', 'Software Engineering'
        COMPUTER_SCIENCE = 'CSC', 'Computer Science'
        
    class StudentLevel(models.TextChoices):
        FIRST_YEAR = '100', '100'
        SECOND_YEAR = '200', '200'
        THIRD_YEAR = '300', '300'
        FOURTH_YEAR = '400', '400'
    
    name = models.CharField(max_length=100, help_text='The name of the student')
    mat_number = models.CharField(max_length=100, help_text="The student's matric number")
    department = models.CharField(max_length=30, choices=StudentDepartment.choices, help_text="The student's department")
    level = models.CharField(max_length=30, choices=StudentLevel.choices, help_text="The student's level")
    amount = models.IntegerField(default=5000)
    has_paid = models.BooleanField(default=False, help_text="Whether this student has paid")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="The date and time this booking was created")
    paid_when = models.DateTimeField(null=True, blank=True, help_text="The date and time this booking was paid for")
    
    def __str__(self):
        return self.name