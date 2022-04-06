# will split string into list according to commas
def Convert(string): 
    li = list(string.split(","))
    return li

#function to reduce domain of variable. but not used in program, better version of this is used  
def retlist(num,summ):
	if(summ == ((num*(num+1))/2)):
		return [x for x in range(1,num+1)]
	elif(summ == (((num*(num+1))/2)+(9-num)*num)):
		return [(x+(9-num)) for x in range(1,num+1)]
	else:
		return [1,2,3,4,5,6,7,8,9]

#returns intersection of two lists
def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2))

#this dictionary contains reduced domains according to sum and number of variable in a block
global dic
dic={}

#sum can go upto 45 and number of elements can go upto 9
for x in range(0,46):
	for y in range(0,10):
		dic[str(x)+"-"+str(y)]=[]
#returns union of two lists
def Union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list		
#this function calculates reduced domain 
def rep(i,summ,count,lis):
	if(i==10):
		return None
	nlis=dic[str(summ)+"-"+str(count)].copy()
	dic[str(summ)+"-"+str(count)]=Union(lis,nlis)
	for x in range(i+1,10):
		rep(x,summ+x,count+1,lis+[x])
	return None

#will calculate the required dictionary on line 21
rep(0,0,0,[])
#print(dic)

#enter test case file name here
s = "simple/input0.txt"

fle = open(s,'r')

#removes \n character and creates list accordingly
reader= fle.read().splitlines()

#number of rows
global rows
rows = int(reader[0][5:])

#number of colums
global colums
colums = int(reader[1][8:])

#horizzontal consstraint sums
global hsums
hsums = []

#vertical constraint sums 
global vsums
vsums = []

#this is constraint matrix, will tell consstraint location , for particular variable 
global consmatrix
consmatrix = []

#this will contain solution values
global valmatrix
valmatrix = []

#intitialisations and sstoring horizontal constraint values
for x in range(rows):
	hsums.append(Convert(reader[3+x]))
	consmatrix.append([])
	valmatrix.append([])

#vertical constraint values
for x in range(rows):
	vsums.append(Convert(reader[4+rows+x]))
	for y in range(colums):
		consmatrix[x].append([])
		valmatrix[x].append([])

#use of file values is done
fle.close()
"""
#print(hsums)
#print(vsums)
#print(consmatrix)
#global re
#re = 0
"""
global vartype
vartype={}
global lascons
lascons=[]

#contains variable list , which we will iterate on while backtracking
global varlist
varlist=[]

#constraints dictionary that will store all the neccessarry information related to a constraint
global constraints
constraints={}

backtrack = 0 

global remdomain
remdomain=[1,2,3,4,5,6,7,8,9]

#first we attach row wise constraints to their block variables 
for x in range(rows):
	for y in range(len(hsums[x])):
		if(hsums[x][y]=='#' and vsums[x][y]=='#'):#means this is not a variable
			valmatrix[x][y]='#'#update in final solution are also done simultaneously
			continue
		if(hsums[x][y]=='0' and vsums[x][y]=='0'):#means this is  variable 
			consmatrix[x][y].append(lascons) #constraint correspoinding to a variable is attatched here
			constraints[str(lascons[0])+"_"+str(lascons[1])+"_h"][2]+=1#one more variable added to a constraint
			varlist.append([x,y]) #variable's are appended to the varlist 
		elif(hsums[x][y]!='#' and hsums[x][y]!='0'):#means this is  constraint
			constraints[str(x)+"_"+str(y)+"_h"]=[[1,2,3,4,5,6,7,8,9],int(hsums[x][y]),0]#constraint initialisation
			valmatrix[x][y]='S'#update in final solution are also done simultaneously
			lascons=[x,y]	#now next variable in this row will be connected to this constraint sum only
#now we attach column wise constraints to their block variables 
for x in range(colums):
	for y in range(rows):
		if(hsums[y][x]=='#' and vsums[y][x]=='#'):#means this is not a variable
			valmatrix[y][x]='#'#update in final solution are also done simultaneously
			continue
		if(hsums[y][x]=='0' and vsums[y][x]=='0'):#means this is  variable
			consmatrix[y][x].append(lascons) #constraint correspoinding to a variable is attatched here
			constraints[str(lascons[0])+"_"+str(lascons[1])+"_v"][2]+=1#one more variable added to a constraint
		elif(vsums[y][x]!='#' and vsums[y][x]!='0'):#means this is  constraint
			constraints[str(y)+"_"+str(x)+"_v"]=[[1,2,3,4,5,6,7,8,9],int(vsums[y][x]),0]#constraint initialisation
			valmatrix[y][x]='S'#update in final solution are also done simultaneously
			lascons=[y,x] #connects column constraints to column elements 

#reduced domains for constraint variables 
for st in constraints:
	constraints[st][0]=dic[str(constraints[st][1])+"-"+str(constraints[st][2])]#reduced domain for particular sum and number of variables in block is stored in this dictionary

"""print(consmatrix)
print()
print(varlist)
print()
print(constraints)"""

# re variable contains number of constraints that have been solved
def legalassignment(a,re):# this is the function which implements bactracking to find solution
	"""#print(a,"a val")
	#print(len(varlist))"""
	if(a<len(varlist)):# because we are looping over the variable list , we don't want to cross the end
		i=varlist[a][0]#variable location in kakuro
		j=varlist[a][1]
		m = consmatrix[i][j][0]#constraint location for this variable
		n = consmatrix[i][j][1]
		k = str(m[0])+"_"+str(m[1])+"_h"# converting the horizontal and vertical constraint for this variable to a string ,so we can use as key in constraints dictionary
		l = str(n[0])+"_"+str(n[1])+"_v"
		"""#print(k,l)"""
		cpylis = constraints[k][0].copy()
		cpy2lis = constraints[l][0].copy()
		cpy3lis = intersection(cpylis,cpy2lis)# intersection of domain for the variable found from both the constraints, ANOTHER NODE CONSISTENCY OPTIMIZATION
		"""#print(cpy3lis)"""
		for b in cpy3lis:# iterating over variable's domain
			"""#print("range")"""
			if(b <= constraints[k][1] and b <= constraints[l][1] ): # checking that variable doesn't cross the sum value of its constraints
				"""#print(a,b,"abval")"""
				if (b in constraints[k][0]) and (b in constraints[l][0]) :# checking if this variable is present in the domain of it's constraint
					
					"""#print("got inside")"""
					global backtrack
					backtrack+=1
					
					#if all variables for a constraint have been found and this value doesn't equal to the remaining sum we don't need to go further
					if(( constraints[k][2] == 1 and b != constraints[k][1]) or ( constraints[l][2] == 1 and b != constraints[l][1])):
						continue
					
					"""#print(constraints)"""
					# sum value in constraint is adjusted according to newly introduced variables value
					constraints[k][1] -= b
					constraints[l][1] -= b
					# we remove this value from domain of constraint since in same block variables can't have same value
					cpylis=constraints[k][0].copy()
					cpylis.remove(b)
					constraints[k][0]=cpylis
					"""#print(constraints)"""
					cpy2lis=constraints[l][0].copy()
					cpy2lis.remove(b)
					constraints[l][0]=cpy2lis
					"""#print(constraints)"""
					constraints[k][2]-=1
					constraints[l][2]-=1
					
					#early success detection
					if(constraints[l][2]==0):# if all variables correspoinding to constraint have been found we check if all constraints have been solved 
						re +=1
						if(re == len(constraints)):
							valmatrix[i][j] = b
							return True 
					if(constraints[k][2]==0):
						re +=1
						if(re == len(constraints)):
							valmatrix[i][j] = b
							return True 

					"""#print(constraints)
					#a+=1"""
					if(legalassignment(a+1,re) == True):
						valmatrix[i][j] = b
						return True
					"""#a-=1
					#print("false return")"""
					# we reach here it means this value of variable was false , so we redo the changes we made 
					constraints[k][1] += b
					constraints[l][1] += b
					constraints[l][0].append(b)
					constraints[k][0].append(b)
					if(constraints[l][2]==0):
						re -=1
					if(constraints[k][2]==0):
						re -=1
					constraints[k][2]+=1
					constraints[l][2]+=1
		return False			
#text file where solution kakuro will be printed
filename = "yoursolll.txt"
sm = open(filename,'a')
print(s[6:],file = sm)		
				
if(legalassignment(0,0) == True):#means we have done the complete legal assignment for the problem
	print("horizontal",file = sm)#first i print the horizontal constraint matrix and then i print the vertical constraint matrix given in input
	for x in range(rows):
		print(reader[3+x],file = sm)
	print("vertical",file = sm)
	for x in range(rows):
		print(reader[4+x+rows],file = sm)
	print("ans",file = sm)
	for x in range(rows):#from here i print the solution in file
		print(" ".join(map(str,valmatrix[x])),file = sm)
	print("",file = sm)
else:
	print("ERRROR")
print(backtrack)		
sm.close()				
		
	
		
		
		
