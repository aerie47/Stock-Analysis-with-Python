import cx_Oracle
import pandas as pd
import cgi

def main():
    form = cgi.FieldStorage()  # cgi script line 
    theStr = form.getfirst('Path','')
    contents = processInput(theStr)
    print contents
    
def processInput(Path):
    con = cx_Oracle.connect('FP/1234')
    cur = con.cursor()
    
    #cur.execute('drop table sprices')
    cur.execute('create table sprices (sdate CHAR(10))')
    
    data = pd.read_csv(Path,header=None)
    col_name = data.iloc[0]
    del col_name[0]

    # add more columns to expand the sprice tables 
    for line in col_name:
        line = line+'_'
        cur.execute('alter table sprices add %s FLOAT' %(line))
    # add underscore in original dataset

    for i in range(len(col_name)):
        col_name.iloc[i] = col_name.iloc[i] + '_'
    
    value = data[3:]
    date = value[0]
    del value[0]
    value = value.astype(float)    
    
    num = value.shape[0]
    for i in range(num):
        list1 = list(col_name)
        list2 = list(value.iloc[i,:])
        mydict = dict(zip(list1,list2))
        mydict['sdate']=date.iloc[i]
        key = str(mydict.keys()).replace('[','(').replace(']',')').replace("'","")
        dict_value = str(mydict.values()).replace('[','(').replace(']',')')
        cur.execute('insert into sprices %s values %s' %(key,dict_value))

    con.commit()
    cur.close()
    con.close()
    
    return makePage('done_submission_template.html')
    
        
def fileToStr(fileName):
    #Return a string containing the contents of the named file.
    fin = open(fileName);
    contents = fin.read();
    fin.close()
    return contents
    
def makePage(templateFileName):
    pageTemplate = fileToStr(templateFileName)
    return pageTemplate

try:
    print "Content-type: text/html\n\n"
    main()
except:
    cgi.print_exception()
