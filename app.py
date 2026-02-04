from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user , LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'fuckyou123'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#بختصار هنا اول سطر عرفت البرنامج وحطيته بمتغير اسمه اب 
#ثم عرفت متغير الداتا بيس وحطيت داخله برنامجنا 
#ثم ربطتهم ببعض في السطر الثاني وعرفت له اني بستخدم اسكيول لايت وثم اسم ملف الداتابيس
#واخر شيء سويت سيكرت كي للداتا بيس مدري كيف اوصل له


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length( min=3, max=15)], render_kw={'placeholder': 'username'})
    password = PasswordField(validators=[InputRequired(), Length( min=4, max=20)], render_kw={'placeholder': 'Password'})
#عرفنا هنا متغيرين فورمز لانشاء حساب جديد، واحد متغير لليوزر وحطينا المتطلبات والثاني للباسورد وحطينا المتطلبات
    submit = SubmitField("Register")     #نفس اول بس ذا لزر السبميت

    def validate_username(self, username): #هنا بسوي فنكشن بس يشوف اذا اليوزر مكرر ولا لا
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("That username already exists, so FuckOff")



#ذا نفس الكلاس اللي فوق بس للتسجيل مو لانشاء الحساب
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length( min=3, max=15)], render_kw={'placeholder': 'username'})
    password = PasswordField(validators=[InputRequired(), Length( min=4, max=20)], render_kw={'placeholder': 'Password'})
#عرفنا هنا متغيرين فورمز لانشاء حساب جديد، واحد متغير لليوزر وحطينا المتطلبات والثاني للباسورد وحطينا المتطلبات
    submit = SubmitField("Login")
    #نفس اول بس ذا لزر السبميت




@app.route('/')
def home():
    return render_template('home.html', methods=['GET', 'POST'])



@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  #هنا سوينا متغير اسمه فورم واضفناه للبيج تحت وفوق اضفنا ميثود القيت والبوست\
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    form = RegisterForm() #هنا سوينا متغير اسمه فورم واضفناه للبيج تحت وفوق اضفنا ميثود القيت والبوست

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))


    return render_template('register.html', form=form)


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(host = '0.0.0.0' , port = 8000, debug = True)


    

