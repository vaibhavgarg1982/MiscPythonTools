from flask import Flask, render_template, request, url_for, redirect
import sqlite3

app = Flask("__name__")

@app.route("/")
def index():
    return render_template("start.html", title = "RTT Home Page")

@app.route("/viewsources")
def viewsources():
    conn = sqlite3.connect("RTT.db")
    conn.execute("PRAGMA foreign_keys = 1") ##to enforce foreign key rules
    c = conn.cursor()
    
    #print("----&& REQUIREMENTS SOURCES &&----")
    srclist=[]
    for row in (c.execute('SELECT * FROM RequirementSourcesMaster')):
        #print(row)
        srclist.append(row)
    conn.close()
    return render_template("viewsources.html", title = "View Requirement Sources",srclist = srclist)

@app.route('/viewaddreqsources', methods = ['GET', 'POST'])
def viewaddsources():
    
    conn = sqlite3.connect("RTT.db")
    conn.execute("PRAGMA foreign_keys = 1") ##to enforce foreign key rules
    c = conn.cursor()
    
    #print("----&& REQUIREMENTS SOURCES &&----")

    
    if request.method == 'POST':
        Source = (request.form['ReqSource'])
        Comments = (request.form['comments'])
        if Source.strip() !="":
            c.execute(" INSERT INTO RequirementSourcesMaster (Source, Comments) VALUES(:Source, :Comments)", {"Source": Source, "Comments": Comments}) 
            conn.commit()

    srclist=[]
    for row in (c.execute('SELECT * FROM RequirementSourcesMaster')):
        #print(row)
        srclist.append(row)
    conn.close()

    return render_template("viewaddreqsources.html", title = "View and add Requirement Sources",srclist = srclist)


@app.route('/viewaddreqs', methods = ['GET', 'POST'])
def viewaddreqs():
    
    conn = sqlite3.connect("RTT.db")
    conn.execute("PRAGMA foreign_keys = 1") ##to enforce foreign key rules
    c = conn.cursor()
    
    #print("----&& REQUIREMENTS SOURCES &&----")

    
    if request.method == 'POST':
        SourceID = (request.form['ReqSourceID'])
        ReqText = (request.form['ReqText'])
        c.execute(" INSERT INTO Requirements (SourceID, ReqText) VALUES(:Source, :ReqText)", {"Source": SourceID, "ReqText": ReqText}) 
        conn.commit()
    
        
    srclist=[]
    query =  '''SELECT RequirementSourcesMaster.id, RequirementSourcesMaster.Source ,Requirements.id, Requirements.ReqText
                 FROM Requirements 
                 INNER JOIN RequirementSourcesMaster
                 ON RequirementSourcesMaster.id = Requirements.sourceID'''
    for row in (c.execute(query)):
        #print(row)
        srclist.append(row)
    conn.close()

    return render_template("viewaddreqs.html", title = "View and add Requirement Sources",srclist = srclist)

@app.route('/viewaddtstcase', methods = ['GET', 'POST'])
def viewaddtestcase():
    
    conn = sqlite3.connect("RTT.db")
    conn.execute("PRAGMA foreign_keys = 1") ##to enforce foreign key rules
    c = conn.cursor()
    
    #print("----&& REQUIREMENTS SOURCES &&----")

    
    if request.method == 'POST':
        TestCategory = (request.form['TestCat'])
        TestName = (request.form['TestName'])
        TestDescription = request.form['TestDes']
        if len(TestCategory.strip())>2 and len(TestName.strip())>5 and len(TestDescription.strip())>5:
            c.execute(" INSERT INTO TestCases (TestCategory, TestName, TestDescription) VALUES(:TestCategory, :TestName, :TestDescription)", {"TestCategory": TestCategory, "TestName": TestName, "TestDescription":TestDescription}) 
            conn.commit()        
        else:
            pass            # ToDo: handle error and bubble it up to user
    srclist=[]
    query =  "select * FROM TestCases"
    for row in (c.execute(query)):
        #print(row)
        srclist.append(row)
    
    conn.close()

    return render_template("viewaddtstcase.html", title = "View and add Requirement Sources",srclist = srclist)


@app.route("/updatetrac", methods = ['GET', 'POST'])
def updatetrac():
    conn = sqlite3.connect("RTT.db")
    conn.execute("PRAGMA foreign_keys = 1") ##to enforce foreign key rules
    c = conn.cursor()

    if request.method == 'POST':
        #print (request.form)
        reqtext = request.form['reqs']
        tstcase = request.form['testcases'].split(" (")[0]
        
        reqids = []
        for reqid in c.execute('select id from Requirements WHERE ReqText ="' + reqtext + '"'):
            reqids.append(reqid)
        reqid =  (reqid[0])

        tstcases = []
        for testid in c.execute('select id from Testcases WHERE TestName ="' + tstcase + '"'):
            tstcases.append(testid)
        testid =  (tstcases[0][0])

        #print(f"{reqid=} {testid=}")

        c.execute("INSERT INTO Traceability (ReqID, TestID) VALUES(:ReqID, :TestID)", {"ReqID" : reqid, "TestID":testid})
        conn.commit()
        conn.close()
        return redirect('updatetrac')




    queryview = "select Requirements.ReqText,TestCases.TestCategory ,TestCases.TestName FROM Traceability INNER JOIN Requirements on Traceability.ReqID = Requirements.id INNER JOIN TestCases on Traceability.TestID = TestCases.id ORDER BY Requirements.ReqText"
    tracs = []
    for trac in c.execute(queryview):
        #print(trac)
        tracs.append(trac)

    


    query = 'SELECT ReqText FROM Requirements'
    reqs = []
    for row in (c.execute(query)):
        #print(row)
        reqs.append(row[0])
    
    testcases = []
    query =  "SELECT TestCategory, TestName FROM TestCases"
    for row in (c.execute(query)):
        #print(row)
        testcases.append(row[1] + " (" + row[0] + ")")

    return render_template('updatetrac.html', reqs=reqs, testcases = testcases, tracs= tracs)

@app.route("/reqnotest")
def reqnotest():
    conn = sqlite3.connect("RTT.db")
    conn.execute("PRAGMA foreign_keys = 1") ##to enforce foreign key rules
    c = conn.cursor()
    OrpReq = c.execute("SELECT id, reqText FROM Requirements WHERE Requirements.id NOT IN(SELECT Traceability.ReqID FROM Traceability)")
    orphans = []

    for orphan in c.execute("SELECT id, reqText FROM Requirements WHERE Requirements.id NOT IN(SELECT Traceability.ReqID FROM Traceability)"):
        orphans.append(orphan)
    
    #print(orphans)

    return render_template("reqnotest.html", orphans = orphans)

@app.route("/undercon")
@app.route("/")
def undercon():
    return str(db2json())
    return render_template('undercon.html')

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def db2json():
    # connect to the SQlite databases
    connection = sqlite3.connect("RTT.db")
    connection.row_factory = dict_factory
    
    cursor = connection.cursor()

    # select all the tables from the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    op = ''
    for table_name in tables:
            # table_name = table_name[0]
            #print (table_name['name'])

            conn = sqlite3.connect("RTT.db")
            conn.row_factory = dict_factory
            
            cur1 = conn.cursor()
            
            cur1.execute("SELECT * FROM "+table_name['name'])
            
            # fetch all or one we'll go for all.
            
            results = cur1.fetchall()
            
            #print (results)
            op += str(results)
        
    return op

            # generate and save JSON files with the table name for each of the database tables
            # with open(table_name['name']+'.json', 'a') as the_file:
            #     the_file.write(format(results).replace(" u'", "'").replace("'", "\""))

    connection.close()




if __name__ == '__main__':
    app.run(debug=True)


# '''SELECT RequirementSourcesMaster.id, RequirementSourcesMaster.Source ,Requirements.id, Requirements.ReqText
# FROM Requirements 
# INNER JOIN RequirementSourcesMaster
# ON RequirementSourcesMaster.id = Requirements.sourceID'''

# select Requirements.ReqText,TestCases.TestCategory ,TestCases.TestName FROM Traceability INNER JOIN Requirements on Traceability.ReqID = Requirements.id INNER JOIN TestCases on Traceability.TestID = TestCases.id ORDER BY Requirements.ReqText