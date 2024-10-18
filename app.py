# from flask import Flask, render_template, request, redirect , url_for, flash, session
# from flask_sqlalchemy import SQLAlchemy 
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# #update the sqlalchemy_database_uri to connect to your mysql database on xampp
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask_data'#replace 'root' with your mysql user name aned provide the password any
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'your_secret_key'#change this to a secure random key
# db = SQLAlchemy(app)

# #user model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)

# #define routes
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/contact')
# def contact():
#     if 'user id' in session:
#         return render_template('contact.html')
#     else:
#         flash('You need to login first.','danger')
#         return redirect(url_for('login'))
    
# @app.route('/login', methods=['GET','POST'])
# def login():
#     if request.method =='POST':
#         email = request.form['email']
#         password = request.form['password']

#         #retrieve the user based on the provided email
#         user= User.query.filter_by(email=email).first()

#         if user and check_password_hash(user.password, password):
#             #store the user's id in the session 
#             session['user_id']= user.id
#             session['username']= user.username #store username in session
#             flash('Login successful!', 'success')
#             return redirect (url_for('index'))
#         else:
#             flash('Invlid email or password. Please try again.','danger')

#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     #clear the user session
#     session.pop('user_id',None)
#     session.pop('username',None) #remove username
#     flash('You have been logged out.','success')
#     return redirect(url_for('login'))

# @app.route('/register' , methods=['GET', 'POST'])
# def register():
#     if request.method =='POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
        
#         #check if the username or email is already in use
#         existing_user =User.query.filter((User.username ==username)| (User.email == email)).first()

#         if existing_user:
#             flash('Username on email already in use.choose a different one.','danger')
#         else:
#             #hash the password before storing it
#             hashed_password = generate_password_hash(password, method='sha256')

#             new_user = User(username=username,email=email,password=hashed_password)
#             db.session.add(new_user)
#             db.session.commit()

#             flash('Registeration successful! Please login.','success')
#             return redirect(url_for('login'))
        
#     return render_template('register.html')

# @app.route('/blogs')
# def blogs():
#     if 'user_id' in session:
#         return render_template('blogs.html')
#     else:
#         flash('You need to login first.','danger')
#         return redirect(url_for('login'))
    
# if __name__ =='__main__':
#     with app.app_context():
#         db.create_all()
#         print("------->!! DB CONNECTED OR NOT CHECK THAT !!<-----------")
#         app.run(debug=True)



from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)

# Generate a secure secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)

# Update the SQLALCHEMY_DATABASE_URI to connect to your MySQL database on XAMPP
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    if 'user_id' in session:
        return render_template('contact.html')
    else:
        flash('You need to login first.', 'danger')
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Retrieve the user based on the provided email
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Store the user's id in the session
            session['user_id'] = user.id
            session['username'] = user.username  # Store username in session
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the user session
    session.pop('user_id', None)
    session.pop('username', None)  # Remove username from session
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))



# ...

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username or email is already in use
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            flash('Username or email already in use. Choose a different one.', 'danger')
        else:
            # Hash the password before storing it
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

# ...








#@app.route('/blogs')
#def blogs():
  #  if 'user_id' in session:
   #     return render_template('blogs.html')
    #else:
     #   flash('You need to login first.', 'danger')
      #  return redirect(url_for('login'))
    
#---------------
@app.route('/blogs', methods=['GET', 'POST'])
def blogs():
    if 'user_id' in session:
        if request.method == 'POST':
            email = request.form['email']
            mobile = request.form['mobile']
            problem = request.form['problem']
            car_model = request.form['car_model']
            address = request.form['address']

            # Here you can do something with the form data like saving it to a database
            # For now, let's just print the form data
            print(f"Email: {email}, Mobile: {mobile}, Problem: {problem}, Car Model: {car_model}, Address: {address}")

            flash('Form submitted successfully!', 'success')
            return redirect(url_for('index'))
        return render_template('blogs.html')
    else:
        flash('You need to login first.', 'danger')
        return redirect(url_for('login'))
#--------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("------> !! DB CONNECTED OR NOT CHECK THAT !!<---------")
    app.run(debug=True)