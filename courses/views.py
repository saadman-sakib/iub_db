from django.shortcuts import redirect, render
from .models import *
import csv
import datetime
from django.db.models import Sum, Max, Min

def check_time(time):
    # check HH:MM format 
    try:
        datetime.datetime.strptime(time, '%H:%M')
        return True
    except ValueError:
        return False


# upload an xl file and save data to database
def upload(request):
    if request.method == 'POST':
        myfile = request.FILES.get('myfile')
        data = myfile.read().decode('utf-8').splitlines()
        #skip the first line
        data = data[1:]
        reader = csv.reader(data)
        for line in reader:
            # SCHOOL_TITLE	COFFER_COURSE_ID	COFFERED_WITH	SECTION	CREDIT_HOUR	CAPACITY	ENROLLED	ROOM_ID	ROOM_CAPACITY	BLOCKED	COURSE_NAME	FACULTY_FULL_NAME	STRAT_TIME	END_TIME	ST_MW
            # SCHOOL_TITLE, COURSE_ID, COFFERED_WITH, SECTION, SECTION, CAPACITY, ENROLLED, ROOM_ID, ROOM_CAPACITY, BLOCKED, COURSE_NAME, FACULTY_FULL_NAME, STRAT_TIME, END_TIME, ST_MW = line        
            SCHOOL_TITLE, COURSE_ID, COFFERED_WITH, SECTION, CREDIT_HOUR, CAPACITY, ENROLLED,	ROOM_ID, ROOM_CAPACITY, BLOCKED,	COURSE_NAME, FACULTY_FULL_NAME,	START_TIME,	END_TIME,ST_MW,	Dept, ClassSize, stuCr, year, semester, Level, SemesterNo, _ = line	
            
            find = Course.objects.filter(course_id=COURSE_ID, section=SECTION, year=year, semester=semester)
            if find:
                continue
            
            
            faculty, faculty_created = Faculty.objects.get_or_create(id_no = FACULTY_FULL_NAME.split('-')[0], name = FACULTY_FULL_NAME.split('-')[1])
            faculty.save()
            
            school, school_created = School.objects.get_or_create(school_title = SCHOOL_TITLE)
            school.save()
            
            department, department_created = Department.objects.get_or_create(name = Dept, school = school)
            department.save()
            
            room, room_created = Room.objects.get_or_create(room_id = ROOM_ID, room_capacity = ROOM_CAPACITY)
            room.save()
            
            
            
            course, course_created = Course.objects.get_or_create(
                course_id = COURSE_ID, 
                section = SECTION, 
                credit_hour = CREDIT_HOUR, 
                capacity = CAPACITY, 
                enrolled = ENROLLED, 
                room = room, 
                course_name = COURSE_NAME, 
                faculty = faculty, 
                start_time = START_TIME if check_time(START_TIME) else datetime.time(0,0), 
                end_time = END_TIME if check_time(END_TIME) else datetime.time(0,0), 
                st_mw = ST_MW,
                student_credit = stuCr,
                year = year, 
                semester = semester,
                department = department,
                class_size = 0 if ClassSize == '' else ClassSize,
                level = Level,
            )
            
            course.save()
        return redirect('/upload/')
    return render(request, 'courses/upload.html')

def test_view(request):
    all_years = Course.objects.all().values_list('year', flat=True).distinct()
    all_semesters = Course.objects.all().values_list('semester', flat=True).distinct()
    
    revenue_dict = {}
    for year in all_years:
        for semester in all_semesters:
            revenue_dict[(year, semester)] = Course.objects.filter(year=year, semester=semester).aggregate(Sum('student_credit'))['student_credit__sum']
    
    return render(request, 'courses/test.html', {'revenue_dict': revenue_dict})