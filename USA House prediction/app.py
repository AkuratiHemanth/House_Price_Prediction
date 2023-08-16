import numpy as np

#Import Flask modules
from flask import Flask, request, render_template

#Import pickle to save our regression model
import pickle 

#Initialize Flask and set the template folder to "template"
app = Flask(__name__, template_folder='template')

#Open our model
import os
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, './model.pkl')
model = pickle.load(open(file_path, 'rb'))

#create our "home" route using the "index.html" page
@app.route('/')
def home():
    return render_template('index.html')

#Set a post method to yield predictions on page
@app.route('/', methods=['POST','GET'])
def predict():
    try:
        #obtain all form values and place them in an array, convert into integers
        int_features = [int(x) for x in request.form.values()]
        #Combine them all into a final numpy array
        final_features = [np.array(int_features)]
        #predict the price given the values inputted by user
        prediction = model.predict(final_features)
    
        #Round the output to 2 decimal places
        output = round(prediction[0], 2)
    
        #If the output is negative, the values entered are unreasonable to the context of the application
        #If the output is greater than 0, return prediction
        if output < 0:
            raise ValueError("Predicted Price is negative, values entered not reasonable")
        else:
            return render_template('index.html', prediction_text='${:,.2f}'.format(output))
    except Exception as e:
        error_msg = str(e) if str(e) else "An error occurred while processing the request."
        return render_template('index.html', error_message=error_msg)
    


#Run app
if __name__ == "__main__":
    app.run(debug=True)
