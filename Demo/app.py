from  flask import Flask,render_template, request, url_for ,jsonify
import run 

app = Flask(__name__,template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def index():   
    #  run the deep model   
    if "comment" in request.form:
          comment = request.form["comment"]
          neg, pos = run.r(comment)

          data = {'negative':float(neg) ,'positive':float(pos)}

          resp = jsonify(data)

          return resp
    return render_template("index.html")

app.run(debug=True)