import sys
import urllib.request

class LED_board():
    '''Class defined for the LED board'''
    def __init__(self, L):
        '''Board is initialized with an LxL array, with every value set to 
        -1. This is the value used to indicate a light is off'''
        self.array=[[False]*L for _ in range(L)]
        self.size=L
    
    def check_parameters(self,start,end):
        '''Function checks if coordinates extend the range of the array and sets them to
        0 or self.size-1 as appropriate'''
        if start[0]<0:
            start[0]=0
        if start[1]<0:
            start[1]=0
        if end[0]>=self.size:
            end[0]=self.size-1
        if end[1]>=self.size:
            end[1]=self.size-1
        return start,end
            
    def turn_on(self, start, end):
        '''Function runs from start to end coordinates turning lights on'''
        if start[0]<=end[0] and start[1]<=end[1]:
            for i in range(start[0],end[0]+1):
                for j in range(start[1], end[1]+1):
                    self.array[i][j]=True
                
    def turn_off(self, start, end):
        '''Function runs from start to end coordinates turning lights off'''
        if start[0]<=end[0] and start[1]<=end[1]:
            for i in range(start[0],end[0]+1):
                for j in range(start[1], end[1]+1):
                    self.array[i][j]=False
 
    def toggle(self, start, end):
        '''Function runs from start to end coordinates switching on lights to off and off lights to on'''
        if start[0]<=end[0] and start[1]<=end[1]:
            for i in range(start[0],end[0]+1):
                for j in range(start[1], end[1]+1):
                    if self.array[i][j]:
                        self.array[i][j]=False
                    else:
                        self.array[i][j]=True
                
def read_file(link):
    '''Function which reads in a file from a URL or local file and returns the
    contents of the file in a string'''
    if link.startswith("http://"):
        req=urllib.request.urlopen(link)
        buffer=req.read().decode('utf-8')
    else:
        buffer=open(link,'r').read() #.read() converts to a string
    return buffer

def return_coordinates(a):
    '''Function which reads in a string with coordinates "x,y" and returns
    the coordinates as integers in a list'''
    x,y=a.split(",")
    return [int(x), int(y)]

def comma_space_removal(line):
    '''Function which removes whitespace surrounding the comma separating coordinates'''
    line=line.replace(" ,", ",")
    line=line.replace(", ", ",")
    return line
    
def main():
    if len(sys.argv)<3:
        print("\nCheck the parameters, no file given.\nInput should be of form 'solve_led --input file_link'")
    else:
        link=sys.argv[2] #Reading link to file from command line parameter
        file=read_file(link)
        arraySize=int(file.split("\n")[0]) #Obtaining size of array from first line of file
        board=LED_board(arraySize)
              
        for line in file.split("\n"):
            if "turn on" in line:
                line=comma_space_removal(line)
                a,b,c,d,e=line.split() #splits string into 5 variables, with coordinates in c and e
                start_point,end_point=board.check_parameters(return_coordinates(c),return_coordinates(e))
                board.turn_on(start_point, end_point)
            elif "turn off" in line:
                line=comma_space_removal(line)
                a,b,c,d,e=line.split()
                start_point,end_point=board.check_parameters(return_coordinates(c),return_coordinates(e))
                board.turn_off(start_point, end_point)
            elif "switch" in line:
                line=comma_space_removal(line)
                a,b,c,d=line.split()
                start_point,end_point=board.check_parameters(return_coordinates(b),return_coordinates(d))
                board.toggle(start_point, end_point)
            else:
                pass 
        on_count=0
        for i in range(arraySize):
            for j in range(arraySize):
                if board.array[i][j]==True:
                    on_count+=1
        print(on_count)
