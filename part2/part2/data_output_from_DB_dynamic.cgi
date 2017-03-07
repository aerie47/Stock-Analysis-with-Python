import cgi
import cx_Oracle

def main():
    contents = processInput()
    print contents

def processInput():
    con = cx_Oracle.connect('FP/1234')
    cur = con.cursor()
    
    cur.execute('''select SDATE, B_ as Change_percentage, company 
                   from sprices, sname
                    where symbol = 'B' and abs(B_ ) > 6
                    order by Change_percentage desc
                    ''')
    output = cur.fetchall()
    len_out = len(output)
    line=''
    for i in range(len_out):
        line += '<td style="text-align: center;">%s</td>'%((output[i])[0])
        line += '<td style="text-align: center;">%s</td>'%((output[i])[1])
        line += '<td style="text-align: center;">%s</td>'%((output[i])[2])
        line += '</tr>'        
        
    return makePage('see_result_template.html',line)
    
    cur.close()
    con.close()
    
def fileToStr(fileName):
    fin = open(fileName)
    contents = fin.read()
    fin.close()
    return contents

def makePage(templateFileName, substitutions):
    pageTemplate = fileToStr(templateFileName)
    return pageTemplate.format(substitutions)   
    
try:
    print "Content-type: text/html\n\n"
    main()
except:
    cgi.print_exception()
  
