from flask import Flask, request, render_template_string, render_template
import subprocess
import os
import satanize

app = Flask(__name__)

# Load flag content
FLAG = open('../flag.txt', 'r').read().strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", result="")

@app.route('/chall', methods=['POST'])
def chall():
    userinput = ""
    name = ""
    if request.method == 'POST':
        challindex = request.form['chall']
        if challindex != '1' and challindex != '2':
                return render_template("index.html", result="")
        if challindex == '1':
                script = "scripts/execute.py"
                desc = "It will execute every single line code (Math, Logical check, Concat String, Statistics): a = 5;b = 4;print(a+b), x = 23;y = 23;print(x==y), a = 'The'; b = 'demon'; print(a+b), x = [1,2,3,4,5,6,7,8];print(max(x)), etc"
        elif challindex == '2':
                script = "scripts/evaluate.py"
                desc = "It will calculate your sins: 1+1, 2*2, 5-2, etc"
        try:
            userinput = request.form['input']
        except Exception as e:
            return render_template("chall.html", challindex = challindex, result = "", desc=desc)
        
        if(userinput != ""):
            try:
                FLAG = open('../flag.txt', 'r').read().strip()
                result = subprocess.check_output(['python', script, userinput, FLAG])
                print(result)
            except subprocess.CalledProcessError as e:
                result = e.output.decode()
            return render_template("chall.html", challindex = challindex, result=result, desc = desc)
        else:
            return render_template("chall.html", challindex = challindex, result = "", desc = desc)
        
@app.route('/render', methods=['GET'])            
def render():
    with open('templates/template.html', 'r') as file:
            template = file.read()
    name = request.args.get('name')
    if name != "":
        try:
            stn = satanize.Satanize()
            if(stn.satanizer(name)):
                name = "Bad boy"
                return render_template_string(template.replace("thisistemplate",name))
        except Exception as e:
            pass
        return render_template_string(template.replace("thisistemplate",request.args.get('name')))
    else:
        return "Hello, please send me your 'name'"

@app.route('/sourcecode/<challindex>', methods=['GET'])
def sourcecode(challindex):
    if challindex == '1':
        sc = "scripts/execute.py"
    elif challindex == '2':
        sc = "scripts/evaluate.py"
    elif challindex == '3':
        sc = "satanize.py"
    # Read the content of script.py
    with open(sc, 'r') as script_file:
        script_content = script_file.read()

    return render_template("source.html", script_content=script_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=1)
