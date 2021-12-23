from django.shortcuts import redirect, render
from .models import *

# upload an xl file and save data to database
def upload(request):
    if request.method == 'POST':
        year = request.POST['year']
        semester = request.POST['semester']
        myfile = request.FILES.get('myfile')
        data = myfile.read().decode('utf-8').splitlines()
        #skip the first line
        data = data[1:]
        for line in data:
            # SCHOOL_TITLE	COFFER_COURSE_ID	COFFERED_WITH	SECTION	CREDIT_HOUR	CAPACITY	ENROLLED	ROOM_ID	ROOM_CAPACITY	BLOCKED	COURSE_NAME	FACULTY_FULL_NAME	STRAT_TIME	END_TIME	ST_MW
            SCHOOL_TITLE, COFFER_COURSE_ID, COFFERED_WITH, SECTION, CREDIT_HOUR, CAPACITY, ENROLLED, ROOM_ID, ROOM_CAPACITY, BLOCKED, COURSE_NAME, FACULTY_FULL_NAME, STRAT_TIME, END_TIME, ST_MW = line.split(',')
        
            faculty = Faculty.objects.get_or_create(id = FACULTY_FULL_NAME.split('-')[0], name = FACULTY_FULL_NAME.split('-')[1])
            faculty.save()
            
            school = School.objects.get_or_create(school_title = SCHOOL_TITLE)
            school.save()
            
            department = Department.objects.get_or_create(name = COFFER_COURSE_ID[:3], school = school)
            department.save()
            
            room = Room.objects.get_or_create(room_id = ROOM_ID, room_capacity = ROOM_CAPACITY)
            room.save()
            
            course = Course.objects.get_or_create(
                course_id = COFFER_COURSE_ID, 
                section = SECTION, 
                credit_hour = CREDIT_HOUR, 
                capacity = CAPACITY, 
                enrolled = ENROLLED, 
                room = room, 
                course_name = COURSE_NAME, 
                faculty = faculty, 
                start_time = STRAT_TIME, 
                end_time = END_TIME, 
                st_mw = ST_MW, 
                year = year, 
                semester = semester,
                department = department
            )
            course.save()
        return redirect('/')
    return render(request, 'courses/upload.html')

