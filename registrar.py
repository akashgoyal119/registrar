import numpy as np 

#global variable that allows you to lookup an instance 
#of person/student/teacher class from a username
allThePeople = {}
allTheStudents = {}
allTheTeachers = {}

#convert season to a number so that you can sort by season
seasons = {"WINTER":1,"SPRING":2,"SUMMER":3,"FALL":4}

class Course():
	def __init__(self,department,number,name,credits):
		self.department = department
		self.number = number
		self.name = name
		self.credits = credits

	def __eq__(self,other):
		return self.__dict__ == other.__dict__

class CourseOffering():
	def __init__(self,course,section_number,instructor,year,quarter):
		self.course = course
		self.section_number = section_number
		self.instructor = instructor
		self.year = year
		self.quarter = quarter.upper() #make it case insensitive
		self.studentsEnrolled = []
		instructor.courseTaught.append(self)

	def __eq__(self,other):
		return self.__dict__ == other.__dict__

	def register_students(self,*students):
		for kid in students:
			#add course to dictionary, using tuple as key since an instance of a class isn't hashable
			kid.courseTaken[(self.course.department,self.course.number,self.course.name, 
				self.course.credits,self.section_number,self.instructor,self.year,self.quarter)] = None 
			self.studentsEnrolled.append(kid)

	def get_students(self):
		for student in self.studentsEnrolled:
			print (student.username)

	def submit_grade(self,studentOrUN, grade): #should affect Student class only
		try:
			studentOrUN.courseTaken[(self.course.department,self.course.number,self.course.name, 
				self.course.credits,self.section_number,self.instructor,self.year,self.quarter)] = grade 
		except:
			theStudent = allTheStudents[studentOrUN]
			theStudent.courseTaken[(self.course.department,self.course.number,self.course.name, 
				self.course.credits,self.section_number,self.instructor,self.year,self.quarter)] = grade 
			#find them in the dictionary list.

	def get_grade(self,studentOrUN):
		try:
			#assumes argument is a Student
			return studentOrUN.courseTaken[(self.course.department,self.course.number,self.course.name, 
				self.course.credits,self.section_number,self.instructor,self.year,self.quarter)]
		except:
			#argument is a username so need to find the instance of Student
			theStudent = allTheStudents[studentOrUN]
			return theStudent.courseTaken[(self.course.department,self.course.number,self.course.name, 
				self.course.credits,self.section_number,self.instructor,self.year,self.quarter)]

class Institution():
	def __init__(self,name):
		self.name = name
		self.list_of_courses = [] #list of all courses offered
		self.list_of_course_offerings = [] #list of course offerings
		self.students = [] #list of all students belong to university
		self.instructors =[] #list of all professors

	def __eq__(self,other):
		return self.__dict__ == other.__dict__

	def list_students(self):
		return self.students 

	def enroll_student(self,aStudent):
		self.students.append(aStudent)

	def hire_instructor(self,anInstructor):
		myBool = False
		for item in self.instructors:
			if item == anInstructor:
				myBool = True
		if not myBool:
			self.instructors.append(anInstructor)

	def list_instructors(self):
		return self.instructors 

	def list_course_catalog(self):
		for item in self.list_of_courses:
			print ('Department: '+item.department+'  Number: '+str(item.number)
				+'  Name: '+item.name+'  Credits: '+item.credits)

	def list_course_schedule(self,year,quarter,departmentName=None):
		if departmentName is None:
			schedule = list(filter(lambda x: x.year == year 
				and x.quarter == quarter.upper(), self.list_of_course_offerings))
		else:
			schedule = list(filter(lambda x: x.year == year 
				and x.quarter == quarter.upper() and x.course.department == departmentName,
				self.list_of_course_offerings))

		for courseO in schedule:
			print ('Department: '+courseO.course.department+'   Name: '+courseO.course.name+'  Teacher: '+
				courseO.instructor.first_name+' '+courseO.instructor.last_name+'   Year: '+
				courseO.year+'   Quarter: '+courseO.quarter+'\n')

	def add_course(self,aCourse):
		myBool = False
		for item in self.list_of_courses:
			if item == aCourse:
				myBool = True
		if myBool == False:
			self.list_of_courses.append(aCourse)

	def add_course_offering(self,aCourseOffering):
		self.list_of_course_offerings.append(aCourseOffering)

	def list_enrolled_students(self):
		for kid in self.list_students():
			print ('name: '+kid.first_name+' '+kid.last_name+
				' his/her GPA is: '+ str(kid.gpa))

	def find_course(self,course_id):
		for item in self.list_of_courses:
			if course_id == item.number:
				return item

class Person():
	def __init__(self,last_name,first_name,school,date_of_birth,username):
		self.last_name = last_name
		self.first_name = first_name
		self.school = school
		self.dob = date_of_birth
		self.username = username
		self.affiliation = None
		self.email = username + '@' + school.name +'.edu'
		allThePeople[self.username] = self #update the dictionary so you can look up a person from a username

class Instructor(Person):
	def __init__(self,last_name,first_name,school,date_of_birth,username):
		Person.__init__(self,last_name,first_name,school,date_of_birth,username)
		self.courseTaught = []
		self.affiliation = 'Instructor'
		allTheTeachers[self.username] = self #update dictionary so you can look up teacher from a username

	#take a year/quarter as optional inputs and list the instructor's courses in that year and or quarter 
	def list_courses(self,year=None,quarter=None):
		courseList = []
		if year is None and quarter is None:
			courseList = self.courseTaught
		elif quarter is None:
			courseList = list(filter(lambda x: x.year == year,self.courseTaught))
		elif year is None:
			courseList = list(filter(lambda x: x.quarter == quarter.upper(),self.courseTaught))
		else:
			courseList = list(filter(lambda x: x.quarter == quarter.upper() and x.year==year,
				self.courseTaught))
		return self.reverseChronologicalOrder(courseList)

	#helper function for list courses
	def reverseChronologicalOrder(self,listOfClasses):
		theArray = np.array([[x.year,seasons[x.quarter.upper()],x] for x in listOfClasses])
		theArray = theArray[np.lexsort((theArray[:,1],theArray[:,0]))][::-1]
		return theArray[:,2].tolist()

	#take a courseID,section_number,instructor user_id,year,quarter, and find the appropriate course
	def addNewCourse(self,course_offering_concatenated,university):
		components = course_offering_concatenated.split('-')
		instructorInstance = allTheTeachers[components[2]]
		newCourse = CourseOffering(university.find_course(components[0]),components[1],
			instructorInstance,components[3],components[4])

		for course_off in university.list_of_course_offerings:
			if newCourse == course_off:
				self.courseTaught.append(course_off)
				return

	def __eq__(self,other):
		return self.__dict__ == other.__dict__

class Student(Person):
	def __init__(self,last_name,first_name,school,date_of_birth,username):
		Person.__init__(self,last_name,first_name,school,date_of_birth,username)
		self.courseTaken = {}
		self.affiliation = 'Student'
		allTheStudents[self.username] = self #update dictionary so you can look up student from a username

	@property
	def gpa(self):
		totalPoints = 0
		totalCredits = 0
		GradeDictionary = {'A+':4,'A':4,'A-':3.7,'B+':3.3,'B':3,'B-':2.7,'C+':2.3,'C':2,'C-':1.7,'D':1,'F':0}
		for key in self.courseTaken.keys():
			if self.courseTaken[key] is None:	#i.e. quarter not over yet.
				pass	
			else:
				totalCredits += key[3] #the tuple's 4th argument is credits
				gradeNumber = GradeDictionary[self.courseTaken[key]]
				totalPoints += key[3] * gradeNumber
		return totalPoints/totalCredits

	@property
	def credits(self):
		numberOfCredits = 0
		for key in self.courseTaken.keys():
			numberOfCredits += key[3]
		return numberOfCredits

	@property	
	def list_courses(self):
		#x[6] and x[7] are the year and quarter
		theList = [x for x in self.courseTaken.keys()]
		return self.reverseChronologicalOrder(theList)

	def reverseChronologicalOrder(self,listOfClasses):
		theArray = np.array([[x[0],x[1],x[2],x[3],x[4],x[5],x[6],seasons[x[7].upper()]] for x in listOfClasses])
		theArray = theArray[np.lexsort((theArray[:,7],theArray[:,6]))][::-1]
		return theArray.tolist()
		#0 dept
		#1 course number
		#2 name
		#3 credits
		#4 section_num
		#5 instructor
		#6 year
		#7 quarter 
	
#scrap work
if 3 == 4:
	IntroPython = Course('MPCS',51402,'Intro to Python',1)
	PythonFall17 = CourseOffering(IntroPython,1,'Flees',2017,'fall')
	PythonSpr17 = CourseOffering(IntroPython,2,'Flees',2016,'spring')
	PythonFall16 = CourseOffering(IntroPython,2,'Flees',2016,'fall')
	Databases = Course('MPCS',53000,'Databases',1)
	DatabasesFall16 = CourseOffering(Databases,1,'Freeman',2016,'fall')

	UC = Institution('UChicago')
	akashgoyal = Instructor('Goyal','Akash',UC,'Jan19','akashgoyal')
	akashgoyal.courseTaught.extend((PythonFall17,PythonSpr17,PythonFall16))
	for item in akashgoyal.list_courses():
		print (item.course.name +' year' + str(item.year) + 'quarter ' + item.quarter)



	UC.list_of_course_offerings.extend((DatabasesFall16,PythonFall16,PythonSpr17,PythonFall17))
	l1 = map(lambda x: x.course.name, UC.list_course_schedule(2016,'spring'))
	print (*l1,sep='\n')

	johnnysack = Student('Sack','Johnny',UC,'blah','johnnysack')
	PythonSpr17.submit_grade(johnnysack,'A+')
	DatabasesFall16.submit_grade('johnnysack','B-')

	for item in johnnysack.courseTaken.keys():
		print (johnnysack.courseTaken[item])

	print (johnnysack.gpa)
	print (johnnysack.credits)
	print (johnnysack.list_courses)

