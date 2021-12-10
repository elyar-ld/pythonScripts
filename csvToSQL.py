import csv 
import sys

tableName = sys.argv[1] #table name equals to file name by default
if len(sys.argv) > 2: #if a table name is given in args
	tableName = sys.argv[2]

sqlScript = open(tableName+".sql","w") #an .sql file will be the output

with open(sys.argv[1],'r', encoding="utf-8") as file:
	reader = csv.reader(file, delimiter=',')
	fields = next(reader)
	dict = {} #this will check if a field name is repeated

	createStatement = "CREATE TABLE %s (" % tableName
	for field in fields:
		cleanedField = field.replace(" ",""); #remove blank spaces in fields
		if cleanedField in dict: #Check if the field name already exists
			dict[cleanedField] += 1
			cleanedField += ('%d' % dict[cleanedField]) #if indeed exists a number is appended
		else:
			dict[cleanedField] = 1
		createStatement += (cleanedField+" VARCHAR(255),")					
	sqlScript.write(createStatement[:-1]+");\n") #CREATE TABLE statement is added to file
	sqlScript.write("\n")

	#all the INSERT statements are created 
	for row in reader:
		insertStatement = "INSERT INTO %s VALUES(" % tableName
		for value in row:
			insertStatement += "\'%s\'," % value
		sqlScript.write(insertStatement[:-1]+");\n")