from app import app
from flask import Flask, request, jsonify, json, url_for, redirect, session, render_template
import pickle
import pandas as pd


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        labels = ['Resource Quantity', 'Resource Unit Price (USD)', 'Project Type', 'Project Subject Category Tree',
                  'Project Subject Subcategory Tree', 'Project Grade Level Category', 'Project Resource Category',
                  'Project Cost (USD)', 'Project Current Status', 'Teacher Prefix', 'School Metro Type',
                  'School Percentage Free Lunch (%)', 'School State', 'School City', 'School County',
                  'School District']

        pickle_in = open("categories.pickle","rb")
        categories = pickle.load(pickle_in)
        cat_list = []
        for c in categories.values():
            cat_list.append(c)

        return render_template('index.html', labels=labels, categories=cat_list)
        
    elif request.method == 'POST':
        input = []
        for i in range(1,17):
            input.append(request.form.get(str(i)))
        print(input)
        session['input'] = input
        return redirect(url_for('predict_kaggle'))

    return '<h2>Request method type not supported</h2>' 

def index_old():
    if request.method == 'GET':
        s = """
        <!DOCTYPE html><link rel="stylesheet" type='text/css' href="/static/css/bootstrap.min.css">
        <div class="jumbotron jumbotron-fluid">
            <div class='container'>
                <h1>Donors Choose Recommendation System (DCRS)</h1>
                <h4>by Tristan Alba, Prince Javier, and Jude Teves</h4>
            </div>
        </div>
        """
        # <div class="container">
        #     <form method="POST">
        #         Resource Quantity: <input type="number" min=0 name="1" value="10"><br>
        #         Resource Unit Price: <input type="number" min=0 name="2" value="10"><br>
        #         Project Type: <input type="text" name="3" value="Teacher-Led"><br>
        #         Project Subject Category Tree: <input type="text" name="4" value="Health & Sports"><br>
        #         Project Subject Subcategory Tree: <input type="text" name="5" value="Gym & Fitness, Health & Wellness"><br>
        #         Project Grade Level Category: <input type="text" name="6" value="Grades 9-12"><br>
        #         Project Resource Category: <input type="text" name="7" value="Sports & Exercise Equipment"><br>
        #         Project Cost: <input type="number" step=0.01 min=0 name="8" value="53.3"><br>
        #         Project Current Status: <input type="text" name="9" value="Fully Funded"><br>
        #         Teacher Prefix: <input type="text" name="10" value="Mrs."><br>
        #         School Metro Type: <input type="text" name="11" value="suburban"><br>
        #         School Percentage Free Lunch: <input type="number" min=0 name="12" value="65"><br>
        #         School State: <input type="text" name="13" value="New York"><br>
        #         School City: <input type="text" name="14" value="New York City"><br>
        #         School County: <input type="text" name="15" value="Queens"><br>
        #         School District: <input type="text" name="16" value="New York Dept Of Education"><br>
        #         <input type="submit" value="Submit"><br>
        #     </form>
        # </div>
        s += """<div class="container"><form method="POST">"""
        labels = ['Resource Quantity', 'Resource Unit Price (USD)', 'Project Type', 'Project Subject Category Tree',
                  'Project Subject Subcategory Tree', 'Project Grade Level Category', 'Project Resource Category',
                  'Project Cost (USD)', 'Project Current Status', 'Teacher Prefix', 'School Metro Type',
                  'School Percentage Free Lunch (%)', 'School State', 'School City', 'School County',
                  'School District']

        option_template = lambda x: """<option value="{0}">{0}</option>""".format(x)

        pickle_in = open("categories.pickle","rb")
        categories = pickle.load(pickle_in)

        for idx, c in enumerate(categories):
            col = categories[c]
            s += labels[idx]
            if not col:
                step = 1
                if idx == 7:
                    step = 0.01
                s += """  <input type="number" step={1} min=0 name="{0}" value="0"><br> """.format(idx+1, step)
            else:
                s += """<select name="{0}" size="1">""".format(idx+1)
                for options in col:
                    s += option_template(options)
                s += """</select><br>"""

        s += """
        <input type="submit" value="Submit"><br>
        </form>
        </div>
        """

        return s
    elif request.method == 'POST':
        input = []
        for i in range(1,17):
            input.append(request.form.get(str(i)))
        #print(input)
        session['input'] = input
        #test = session.get('input', None)
        #print(type(test))
        #print(test)
        return redirect(url_for('predict_kaggle'))

    return 

@app.route('/testpage', methods=['GET', 'POST'])
def test_page():
    if request.method == 'GET':
        labels = ['Resource Quantity', 'Resource Unit Price (USD)', 'Project Type', 'Project Subject Category Tree',
                  'Project Subject Subcategory Tree', 'Project Grade Level Category', 'Project Resource Category',
                  'Project Cost (USD)', 'Project Current Status', 'Teacher Prefix', 'School Metro Type',
                  'School Percentage Free Lunch (%)', 'School State', 'School City', 'School County',
                  'School District']

        #option_template = lambda x: """<option value="{0}">{0}</option>""".format(x)

        pickle_in = open("categories.pickle","rb")
        categories = pickle.load(pickle_in)
        #number_cats = [idx for idx, val in categories.items() if not val]
        #print(number_cats)
        # return 'haha'

        cat_list = []
        for c in categories.values():
            cat_list.append(c)

        return render_template('index.html', labels=labels, categories=cat_list)
    elif request.method == 'POST':
        input = []
        for i in range(1,17):
            input.append(request.form.get(str(i)))
        print(input)
        session['input'] = input
        #test = session.get('input', None)
        #print(type(test))
        #print(test)
        return redirect(url_for('predict_kaggle'))

    return 

@app.route('/apis/<string:text>', methods=['GET'])
def method1(text):
    s = 'The text you have submitted is:\n{0}\n'.format(text)
    return s

@app.route('/apis/list', methods=['GET'])
def method2():
    s = '<b>Here are the inputs:</b>'
    for key,val in request.args.items():
        s += '<p>{0} : {1}</p>'.format(key, val)
    return s

@app.route('/apis/json/', methods=['GET'])
def method3():
    req_data = request.get_json()
    s = '<b>Here are the inputs:</b>'
    for key,val in req_data.items():
        s += '<p>{0} : {1}</p>'.format(key, val)
    return s

def donors_to_recommend(X_test, clf, index = 0, cluster_disp = False):
    project_type = []
    project_subject_cat = []
    project_subject_subcat = []
    project_grade_level_cat = [] 
    project_resource_cat = [] 
    project_current_stat = []
    teacher_pref = []
    school_metro = []
    school_state = []
    school_city = []
    school_county = []
    school_district = []

    
    pickle_in = open("labels.pickle","rb")
    labels = pickle.load(pickle_in)

    for i in range(len(X_test)):
        project_type.append(labels['Project Type'].index(X_test['Project Type'][i]))
        project_subject_cat.append(labels['Project Subject Category Tree'].index(X_test['Project Subject Category Tree'][i]))
        project_subject_subcat.append(labels['Project Subject Subcategory Tree'].index(X_test['Project Subject Subcategory Tree'][i]))      
        project_grade_level_cat.append(labels['Project Grade Level Category'].index(X_test['Project Grade Level Category'][i]))
        project_resource_cat.append(labels['Project Resource Category'].index(X_test['Project Resource Category'][i]))  
        project_current_stat.append(labels['Project Current Status'].index(X_test['Project Current Status'][i])) 
        teacher_pref.append(labels['Teacher Prefix'].index(X_test['Teacher Prefix'][i]))
        school_metro.append(labels['School Metro Type'].index(X_test['School Metro Type'][i]))
        school_state.append(labels['School State'].index(X_test['School State'][i]))
        school_city.append(labels['School City'].index(X_test['School City'][i]))
        school_county.append(labels['School County'].index(X_test['School County'][i]))
        school_district.append(labels['School District'].index(X_test['School District'][i]))
    
    X_test_transformed = pd.DataFrame(columns=['Resource Quantity', 'Resource Unit Price','Project Type',
       'Project Subject Category Tree', 'Project Subject Subcategory Tree',
       'Project Grade Level Category', 'Project Resource Category',
       'Project Cost', 'Project Current Status', 'Teacher Prefix',
       'School Metro Type','School Percentage Free Lunch', 'School State', 'School City',
       'School County', 'School District'])

    X_test_transformed['Resource Quantity'] = X_test['Resource Quantity']
    X_test_transformed['Resource Unit Price'] = X_test['Resource Unit Price']
    X_test_transformed['Project Type'] = project_type
    X_test_transformed['Project Subject Category Tree'] = project_subject_cat
    X_test_transformed['Project Subject Subcategory Tree'] = project_subject_subcat
    X_test_transformed['Project Grade Level Category'] = project_grade_level_cat
    X_test_transformed['Project Resource Category'] = project_resource_cat
    X_test_transformed['Project Cost'] = X_test['Project Cost']
    X_test_transformed['Project Current Status'] = project_current_stat
    X_test_transformed['Teacher Prefix'] = teacher_pref
    X_test_transformed['School Metro Type'] = school_metro
    X_test_transformed['School Percentage Free Lunch'] = X_test['School Percentage Free Lunch']
    X_test_transformed['School State'] = school_state
    X_test_transformed['School City'] = school_city
    X_test_transformed['School County'] = school_county
    X_test_transformed['School District'] = school_district
    
    y = clf.predict(X_test_transformed)

    if cluster_disp == True:
        print(y[index])

    pickle_in = open("clusters.pickle","rb")
    clusters_by_all = pickle.load(pickle_in)
    
    return clusters_by_all[y[index]], y[index]
    #return clusters_by_all[y]
                 
@app.route('/api/kaggle/project', methods=['GET', 'POST'])
def predict_kaggle():
    
    s = '<!DOCTYPE html><link rel=\"stylesheet\" type=\'text/css\' href=\"/static/css/bootstrap.min.css\">'
    #return 'Hi'

    # if request.method == 'GET':
    #     s += '''
    #     <div class='container'>
    #         <form method="POST">
    #             Resource Quantity: <input type="number" min=0 name="1"><br>
    #             Resource Unit Price: <input type="number" min=0 name="2"><br>
    #             Project Type: <input type="text" name="3"><br>
    #             Project Subject Category Tree: <input type="text" name="4"><br>
    #             Project Subject Subcategory Tree: <input type="text" name="5"><br>
    #             Project Grade Level Category: <input type="text" name="6"><br>
    #             Project Resource Category: <input type="text" name="7"><br>
    #             Project Cost: <input type="number" step=0.01 min=0 name="8"><br>
    #             Project Current Status: <input type="text" name="9"><br>
    #             Teacher Prefix: <input type="text" name="10"><br>
    #             School Metro Type: <input type="text" name="11"><br>
    #             School Percentage Free Lunch: <input type="number" min=0 name="12"><br>
    #             School State: <input type="text" name="13"><br>
    #             School City: <input type="text" name="14"><br>
    #             School County: <input type="text" name="15"><br>
    #             School District: <input type="text" name="16"><br>
    #             <input type="submit" value="Submit"><br>
    #         </form>
    #     </div>
    #     '''

    #     return s


    #req_data = request.args
    # input = []
    # for i in range(1,17):
    #     input.append(request.form.get(str(i)))
    input = session.get('input', None)

    if 1 == 1:
    #if 'input' in req_data:
        # s += '<table><tr><th>These are the potential donors for Cluster '

        # input = req_data['input']
        # try:
        #     input = list(input.split(','))
        #     #input = list(map(float,input.split(',')))
        #     #s += '<p>{0}</p>'.format(input)
        # except:
        #     s = 'Input must only be n numbers separated by commas.'
        #     return s

        if len(input) != 16:
            #s += '<b>The kNN model needs only 4 numbers to do the prediction.</b>'
            #s += 'No Data Header received'
            s += 'List should contain 16 elements'
        else:
            pickle_in = open("model.pickle","rb")
            clf = pickle.load(pickle_in)     

            X_test = pd.DataFrame()
            X_test['Resource Quantity'] = [int(input[0])]
            X_test['Resource Unit Price'] = [int(input[1])]
            X_test['Project Type'] = [input[2]]
            X_test['Project Subject Category Tree'] = [input[3]]
            X_test['Project Subject Subcategory Tree'] = [input[4]]
            X_test['Project Grade Level Category'] = [input[5]]
            X_test['Project Resource Category'] = [input[6]]
            X_test['Project Cost'] = [float(input[7])]
            X_test['Project Current Status'] = [input[8]]
            X_test['Teacher Prefix'] = [input[9]]
            X_test['School Metro Type'] = [input[10]]
            X_test['School Percentage Free Lunch'] = [int(input[11])]
            X_test['School State'] = [input[12]]
            X_test['School City'] = [input[13]]
            X_test['School County'] = [input[14]]
            X_test['School District'] = [input[15]]

            # X_test['Resource Quantity'] = [10]
            # X_test['Resource Unit Price'] = [10]
            # X_test['Project Type'] = ['Teacher-Led']
            # X_test['Project Subject Category Tree'] = ['Health & Sports']
            # X_test['Project Subject Subcategory Tree'] = ['Gym & Fitness, Health & Wellness']
            # X_test['Project Grade Level Category'] = ['Grades 9-12']
            # X_test['Project Resource Category'] = ['Sports & Exercise Equipment']
            # X_test['Project Cost'] = [53.3]
            # X_test['Project Current Status'] = ['Fully Funded']
            # X_test['Teacher Prefix'] = ['Mrs.']
            # X_test['School Metro Type'] = ['suburban']
            # X_test['School Percentage Free Lunch'] = [65]
            # X_test['School State'] = ['New York']
            # X_test['School City'] = ['New York City']
            # X_test['School County'] = ['Queens']
            # X_test['School District'] = ['New York Dept Of Education']

            out, c = donors_to_recommend(X_test, clf, index = 0, cluster_disp = False)
            s += '<body><div class=\'container\'>'
            s += '<h4>These are the potential donors for Cluster {0}</h4>'.format(c)
            s += '<table class=\'table table-dark table-striped\' style=\'white-space: nowrap; width: 1%;\'>'
            s += '<tr><td></td><td>Donor</td></tr>'
            # s += '<table><tr><th>These are the potential donors for Cluster '
            # s += '{0}</th></tr><tr>'.format(c)
            for idx, o in enumerate(out['Donor ID'].tolist()):
                s += '<tr><td>{0}</td><td>{1}</td></tr>'.format(idx, o)
            s += '</table></div></body>'
            # out = donors_to_recommend(X_test, clf, index = 0, cluster_disp = False)
            # s += '{0}'.format(out)

    else:
        s = '<b>There is no input :(</b>'
    return s


@app.route('/api/kaggle/project/v2', methods=['POST'])
def predict_kaggle_v2():
    if request.method == 'GET':
        return 'Request method must be POST'
    
    if request.headers['Content-Type'] != 'application/json':
        return 'No Json content found'

    req_data = json.loads(request.get_json())
    if 'input' not in req_data:
        return "'input' key not found"

    #return str(type(req_data))
    #return str(type(json.loads(req_data)))
    #return str(type(req_data))

    input = req_data['input']

    print('Success! There is an input')
    #return str(input)

    if len(input) != 16:
        return 'List should contain 16 elements'
    
    print('16 elements found!')
    pickle_in = open("model.pickle","rb")
    clf = pickle.load(pickle_in)     

    X_test = pd.DataFrame()
    X_test['Resource Quantity'] = [int(input[0])]
    X_test['Resource Unit Price'] = [int(input[1])]
    X_test['Project Type'] = [input[2]]
    X_test['Project Subject Category Tree'] = [input[3]]
    X_test['Project Subject Subcategory Tree'] = [input[4]]
    X_test['Project Grade Level Category'] = [input[5]]
    X_test['Project Resource Category'] = [input[6]]
    X_test['Project Cost'] = [float(input[7])]
    X_test['Project Current Status'] = [input[8]]
    X_test['Teacher Prefix'] = [input[9]]
    X_test['School Metro Type'] = [input[10]]
    X_test['School Percentage Free Lunch'] = [int(input[11])]
    X_test['School State'] = [input[12]]
    X_test['School City'] = [input[13]]
    X_test['School County'] = [input[14]]
    X_test['School District'] = [input[15]]

    print('Data transformation successful!')

    donors, c = donors_to_recommend(X_test, clf, index = 0, cluster_disp = False)
    d = {'cluster': int(c), 'donors': donors['Donor ID'].tolist()}
    print('Donors classified!')
    return jsonify(d)


