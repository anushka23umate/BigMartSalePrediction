from flask import Flask, render_template, request
import joblib
import numpy as np
import datetime as dt

app = Flask(__name__)

current_year = dt.datetime.today().year
model = joblib.load('C:\\Users\\Hp\\Desktop\\BigMartSalePrediction\\bigmart_model')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        p1 = float(request.form['Item_MRP'])
        outlet_identifier = request.form['Outlet_Identifier']
        outlet_size = request.form['Outlet_Size']
        outlet_type = request.form['Outlet_Type']
        p5 = current_year - int(request.form['Outlet_Establishment_Year'])

        outlet_identifier_mapping = {
            "OUT010": 0, "OUT013": 1, "OUT017": 2, "OUT018": 3,
            "OUT019": 4, "OUT027": 5, "OUT035": 6, "OUT045": 7,
            "OUT046": 8, "OUT049": 9
        }

        outlet_size_mapping = {"High": 0, "Medium": 1, "Small": 2}

        outlet_type_mapping = {
            "Supermarket Type1": 1, "Supermarket Type2": 2,
            "Supermarket Type3": 3, "Grocery Store": 0
        }

        p2 = outlet_identifier_mapping[outlet_identifier]
        p3 = outlet_size_mapping[outlet_size]
        p4 = outlet_type_mapping[outlet_type]

        result = model.predict(np.array([[p1, p2, p3, p4, p5]]))[0]
        lower_bound = result - 714.42
        upper_bound = result + 714.42

        return render_template('index.html', prediction=(lower_bound, upper_bound))

    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    app.run(debug=True)
