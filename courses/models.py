from django.db import models

# Create your models here.
#SCHOOL_TITLE	COFFER_COURSE_ID	COFFERED_WITH	SECTION	CREDIT_HOUR	CAPACITY	ENROLLED	ROOM_ID	ROOM_CAPACITY	BLOCKED	COURSE_NAME	FACULTY_FULL_NAME	STRAT_TIME	END_TIME	ST_MW

class Room(models.Model):
    room_id = models.IntegerField(unique=True)
    room_capacity = models.IntegerField()

    def __str__(self):
        return self.room_id


class Faculty(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class School(models.Model):
    school_title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.school_title

class Department(models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School)
    
    def __str__(self):
        return self.name
 
class Course(models.Model):
    school = models.ForeignKey(School)
    department = models.ForeignKey(Department)
    course_id = models.CharField(max_length=100)
    section = models.IntegerField()
    credit_hour = models.IntegerField(max_length=100)
    capacity = models.IntegerField(max_length=100)
    enrolled = models.IntegerField(max_length=100)
    room = models.ForeignKey(Room)
    course_name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty)
    start_time = models.TimeField()
    end_time = models.TimeField()
    st_mw = models.CharField(max_length=2)
    year = models.IntegerField()
    semester = models.CharField(max_length=100)
    
    # course_id + section = unique
    class Meta:
        unique_together = ('course_id', 'section', 'year', 'semester')
    
    
    def __str__(self):
        return self.course_id + ' ' + self.section + ' ' + self.semester + ' ' + self.year
    
    