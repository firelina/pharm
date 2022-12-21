import flask
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from userApp import userApp
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import MultiDict

from config import config

login_manager = LoginManager()
login_manager.init_app(userApp)

userApp.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['URI']
userApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(userApp)
# from userApp.database import *
db.create_all()


def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


# служебная функция загрузки пользователя
@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)


@userApp.route('/')
@userApp.route('/index')
def index():
    if current_user.is_authenticated:
        return flask.redirect(f'/{current_user.id}')
        # return flask.render_template("main_page.html", user_id=current_user.id)
    else:
        return flask.render_template("index.html")


# from userApp.forms import *
# регистрация пользователя
@userApp.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    listt = Employee.query.all()
    listt = [f'{i.id} {i.name} {i.surname} {i.fathername}' for i in listt]
    form.id_employee.choices = listt
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return flask.render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
        if User.query.filter_by(email=form.email.data).first():
            return flask.render_template('register.html', title='Регистрация', form=form,
                                         message="Такой пользователь уже есть")

        user = User(login=form.login.data, email=form.email.data, id_employee=form.id_employee.data.split()[0])
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return flask.redirect('/login')
    return flask.render_template('register.html', title='Регистрация', form=form)


# вход пользователя в систему
@userApp.route('/login', methods=['GET', 'POST'])
def login():
    global my_id
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            my_id = user.id
            return flask.redirect("/")
        return flask.render_template('login.html', message="Неправильный логин или пароль", form=form)
    return flask.render_template('login.html', title='Авторизация', form=form)


# выход с сайта
@userApp.route('/logout')
@login_required
def logout():
    logout_user()
    return flask.redirect("/")


@userApp.route('/start', methods=('GET', 'POST'))
@login_required
def start():
    form = DrugstoreForm()
    if form.validate_on_submit():
        data = Drugstore(name=form.name.data, adress=form.adress.data, telethon=form.telethon.data)
        db.session.add(data)
        db.session.commit()
        return flask.redirect(f'/drugstore')
    return flask.render_template("drugstoref.html", title='Добавить аптеку', form=form)


@userApp.route('/provider/create', methods=('GET', 'POST'))
@login_required
def provider_create():
    form = ProviderForm()
    if form.validate_on_submit():
        data = Provider(name=form.name.data, adress=form.adress.data, telethon=form.telethon.data)
        db.session.add(data)
        db.session.commit()
        return flask.redirect(f'/provider')
    return flask.render_template("providerf.html", title='Добавить поставщика', form=form)


@userApp.route('/provider/<int:id>/update', methods=['GET', 'POST'])
@login_required
def provider_update(prov_id):
    providers = Provider.query.filter_by(id=prov_id).first()
    form = ProviderForm(MultiDict([('name', providers.name), ('adress', providers.adress),
                                   ('telethon', providers.telethon)]))
    if flask.request.method == 'POST':
        if providers:
            name = flask.request.form['name']
            adress = flask.request.form['adress']
            telethon = flask.request.form['telethon']
            row = db.session.query(Provider).get(prov_id)
            row.name = name
            row.adress = adress
            row.telethon = telethon
            db.session.commit()
            return flask.redirect(f'/provider')
        return f"Drugstore with id = {prov_id} Does nit exist"
    return flask.render_template('providerf.html', form=form)


@userApp.route('/provider/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def provider_delete(prov_id):
    # store = Drugstore.query.filter_by(id=id).first()
    if flask.request.method == 'POST':
            dell = db.session.query(Provider).get(prov_id)
            db.session.delete(dell)
            db.session.commit()
            return flask.redirect(f'/provider')
    return flask.render_template('delete.html')


@userApp.route('/drugstore/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(drugst_id):
    # store = Drugstore.query.filter_by(id=id).first()
    if flask.request.method == 'POST':
            dell = db.session.query(Drugstore).get(drugst_id)
            db.session.delete(dell)
            db.session.commit()
            return flask.redirect(f'/drugstore')
    return flask.render_template('delete.html')


@userApp.route('/batch/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def batchdelete(batch_id):
    if flask.request.method == 'POST':
            dell = db.session.query(Batch).get(batch_id)
            db.session.delete(dell)
            db.session.commit()
            return flask.redirect(f'/batch')
    return flask.render_template('delete.html')


@userApp.route('/drug/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def drug_delete(drug_id):
    if flask.request.method == 'POST':
            dell = db.session.query(Drug).get(drug_id)
            db.session.delete(dell)
            db.session.commit()
            return flask.redirect(f'/drug')
    return flask.render_template('delete.html')


@userApp.route('/employee/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def employee_delete(emp_id):
    if flask.request.method == 'POST':
            dell = db.session.query(Employee).get(emp_id)
            db.session.delete(dell)
            db.session.commit()
            return flask.redirect(f'/employee')
    return flask.render_template('delete.html')


@userApp.route('/supplaycontract/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def supplaydelete(supp_id):
    if flask.request.method == 'POST':
            dell = db.session.query(SupplayContract).get(supp_id)
            db.session.delete(dell)
            db.session.commit()
            return flask.redirect(f'/supplaycontract')
    return flask.render_template('delete.html')


@userApp.route('/drug/<int:id>/update', methods=['GET', 'POST'])
@login_required
def drug_update(drug_id):
    drug_upd = Drug.query.filter_by(id=drug_id).first()

    form = DrugForm(MultiDict([('name', drug_upd.name), ('price', drug_upd.price),
                               ('release_date', str(drug_upd.release_date)),
                               ('id_provider', drug_upd.id_provider), ('consist', drug_upd.consist),
                               ('suitability', drug_upd.suitability)]))
    listt = Provider.query.all()
    listt = [f'{i.id} {i.name} {i.adress} {i.telethon}' for i in listt]
    form.id_provider.choices = listt
    if flask.request.method == 'POST':
            name = flask.request.form['name']
            price = flask.request.form['price']
            release_date = flask.request.form['release_date']
            id_provider = flask.request.form['id_provider'].split()[0]
            consist = flask.request.form['consist']
            suitability = form.suitability.data
            ba = db.session.query(Drug).get(drug_id)
            ba.name = name
            ba.release_date = release_date
            ba.id_provider = id_provider
            ba.price = price
            ba.consist = consist
            if suitability == 'True':
                ba.suitability = True
            else:
                ba.suitability = False
            # print(goods_number)
            db.session.commit()
            return flask.redirect(f'/drug')
    return flask.render_template('drugf.html', form=form)


@userApp.route('/drug/create', methods=('GET', 'POST'))
@login_required
def drug_create():
    form = DrugForm()
    listt = Provider.query.all()
    listt = [f'{i.id} {i.name} {i.adress} {i.telethon}' for i in listt]
    form.id_provider.choices = listt
    if form.validate_on_submit():
        data = Drug(name=form.name.data, price=form.price.data, release_date=form.release_date.data,
                    id_provider=form.id_provider.data.split()[0],
                    consist=form.consist.data, suitability=form.suitability.data)
        db.session.add(data)
        db.session.commit()
        return flask.redirect(f'/drug')
    return flask.render_template("drugf.html", title='Добавить лекарство', form=form)


@userApp.route('/drugstore/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(drugst_id):
    store = Drugstore.query.filter_by(id=drugst_id).first()
    if flask.request.method == 'POST':
        if store:
            name = flask.request.form['name']
            adress = flask.request.form['adress']
            telethon = flask.request.form['telethon']
            row = db.session.query(Drugstore).get(drugst_id)
            row.name = name
            row.adress = adress
            row.telethon = telethon
            db.session.commit()
            return flask.redirect(f'/drugstore')
        return f"Drugstore with id = {drugst_id} Does nit exist"
    return flask.render_template('drugstore_update.html', store=store)


@userApp.route('/employee/<int:id>/update', methods=['GET', 'POST'])
@login_required
def employeeupdate(emp_id):
    emp = Employee.query.filter_by(id=emp_id).first()
    form = EmployeeForm(MultiDict([('name', emp.name), ('surname', emp.surname), ('fathername', emp.fathername),
                                   ('gender', emp.gender), ('telethon', emp.telethon), ('birthday', str(emp.birthday)),
                                   ('hire_date', str(emp.hire_date)), ('id_drugstore', emp.id_drugstore),
                                   ('salary', str(emp.salary))]))
    list_drugstore = Drugstore.query.all()
    list_drugstore = [f'{i.id} {i.name} {i.adress} {i.telethon}' for i in list_drugstore]
    form.id_drugstore.choices = list_drugstore
    if flask.request.method == 'POST':
        if emp:
            name = flask.request.form['name']
            surname = flask.request.form['surname']
            fathername = flask.request.form['fathername']
            gender = flask.request.form['gender']
            birthday = flask.request.form['birthday']
            telethon = flask.request.form['telethon']
            hire_date = flask.request.form['hire_date']
            salary = flask.request.form['salary']
            id_drugstore = flask.request.form['id_drugstore'].split()[0]
            row = db.session.query(Employee).get(emp_id)
            row.name = name
            row.surname = surname
            row.fathername = fathername
            row.gender = gender
            row.birthday = birthday
            row.telethon = telethon
            row.hire_date = hire_date
            row.salary = salary
            row.id_drugstore = id_drugstore
            db.session.commit()
            return flask.redirect(f'/employee')
        return f"Employee with id = {emp_id} Does nit exist"
    return flask.render_template('employeef.html', title='Добавить работника',  form=form)


@userApp.route('/employee/create', methods=('GET', 'POST'))
@login_required
def employeecreate():
    form = EmployeeForm()
    list_emp = Drugstore.query.all()
    list_emp = [f'{i.id} {i.name} {i.adress} {i.telethon}' for i in list_emp]
    form.id_drugstore.choices = list_emp
    if form.validate_on_submit():
        data = Employee(name=form.name.data, surname=form.surname.data, fathername=form.fathername.data,
                        gender=form.gender.data, telethon=form.telethon.data, birthday=form.birthday.data,
                        hire_date=form.hire_date.data, salary=form.salary.data,
                        id_drugstore=form.id_drugstore.data.split()[0])
        db.session.add(data)
        db.session.commit()
        return flask.redirect(f'/employee')
    return flask.render_template("employeef.html", title='Добавить работника', form=form)


@userApp.route('/employee')
@login_required
def employee():
    model = Employee.query.filter(id != current_user.employee.id).all()
    # print(current_user.employee.id)
    return flask.render_template("employees.html", model=model)


@userApp.route('/drugstore')
@login_required
def drugstore():
    model = Drugstore.query.all()
    return flask.render_template("drugstores.html", model=model)


@userApp.route('/batch')
@login_required
def batch():
    model = Batch.query.all()
    return flask.render_template("batchs.html", model=model)


@userApp.route('/provider')
@login_required
def provider():
    model = Provider.query.all()
    return flask.render_template("providers.html", model=model)


@userApp.route('/drug')
@login_required
def drug():
    model = Drug.query.all()
    return flask.render_template("drugs.html", model=model)


@userApp.route('/supplaycontract')
@login_required
def supplaycontract():
    model = SupplayContract.query.all()
    return flask.render_template("supplaycontracts.html", model=model)


@userApp.route('/batch/<int:id>/update', methods=['GET', 'POST'])
@login_required
def batchupdate(batch_id):
    batch_update = Batch.query.filter_by(id=batch_id).first()

    form = BatchForm(MultiDict([('goods_number', batch_update.goods_number),
                                ('batch_date', str(batch_update.batch_date)),
                                ('id_provider', batch_update.provider.id), ('id_drug', batch_update.drug.id)]))
    listt = Provider.query.all()
    listt = [f'{i.id} {i.name} {i.adress} {i.telethon}' for i in listt]
    form.id_provider.choices = listt
    drug_ba = Drug.query.all()
    drug_ba = [f'{i.id} {i.name} {i.price} {i.id_provider} {i.consist} {i.release_date}' for i in drug_ba]
    # drug = [i.id for i in drug]
    form.id_drug.choices = drug_ba
    if flask.request.method == 'POST':
            goods_number = flask.request.form['goods_number']
            batch_date = flask.request.form['batch_date']
            id_provider = flask.request.form['id_provider'].split()[0]
            id_drug = flask.request.form['id_drug'].split()[0]
            ba = db.session.query(Batch).get(batch_id)
            ba.goods_number = goods_number
            ba.batch_date = batch_date
            ba.id_provider = id_provider
            ba.id_drug = id_drug
            # print(goods_number)
            db.session.commit()
            return flask.redirect(f'/batch')
    return flask.render_template('batch_update.html', form=form)


@userApp.route('/batch/create', methods=('GET', 'POST'))
@login_required
def create():
    form = BatchForm()
    listt = Provider.query.all()
    listt = [f'{i.id} {i.name} {i.adress} {i.telethon}' for i in listt]
    form.id_provider.choices = listt
    drug_batch = Drug.query.all()
    drug_batch = [f'{i.id} {i.name} {i.price} {i.id_provider} {i.consist} {i.release_date}' for i in drug_batch]
    form.id_drug.choices = drug_batch
    if form.validate_on_submit():
        data = Batch(goods_number=form.goods_number.data, batch_date=form.batch_date.data,
                     id_provider=form.id_provider.data.split()[0], id_drug=form.id_drug.data.split()[0])
        db.session.add(data)
        db.session.commit()
        return flask.redirect(f'/index')
    return flask.render_template("batchf.html", title='Добавить партию', form=form)


@userApp.route('/supplaycontract/create', methods=('GET', 'POST'))
@login_required
def supplaycontractcreate():
    form = SupplayContractForm()
    listt = Batch.query.all()
    listt = [f'{i.id} {i.goods_number} {i.batch_date} {i.id_provider} {i.id_drug}' for i in listt]
    form.id_batch.choices = listt
    drug_sup = Drugstore.query.all()
    drug_sup = [f'{i.id} {i.name} {i.adress} {i.telethon}' for i in drug_sup]
    form.id_drugstore.choices = drug_sup
    emp = Employee.query.all()
    emp = [f'{i.id} {i.name} {i.surname} {i.fathername}' for i in emp]
    form.id_employee.choices = emp
    if form.validate_on_submit():
        data = SupplayContract(id_batch=form.id_batch.data.split()[0], id_drugstore=form.id_drugstore.data.split()[0],
                               contract_date=form.contract_date.data, notes=form.notes.data,
                               id_employee=form.id_employee.data.split()[0])
        db.session.add(data)
        db.session.commit()
        return flask.redirect(f'/supplaycontract')
    return flask.render_template("supplaycontractf.html", title='Добавить договор поставки', form=form)


@userApp.route('/supplaycontract/<int:id>/update', methods=['GET', 'POST'])
@login_required
def supplaycontractupdate(sup_id):
    supplay_cont = SupplayContract.query.filter_by(id=sup_id).first()

    form = SupplayContractForm(MultiDict([('id_batch', supplay_cont.id_batch),
                                          ('id_drugstore', supplay_cont.id_drugstore),
                                          ('contract_date', str(supplay_cont.contract_date)),
                                          ('id_employee', supplay_cont.id_employee),
                                          ('notes', supplay_cont.notes)]))
    listt = Batch.query.all()
    listt = [f'{i.id} {i.goods_number} {i.batch_date} {i.id_provider} {i.id_drug}' for i in listt]
    form.id_batch.choices = listt
    drugg = Drugstore.query.all()
    drugg = [f'{i.id} {i.name} {i.adress} {i.telethon}' for i in drugg]
    form.id_drugstore.choices = drugg
    emp = Employee.query.all()
    emp = [f'{i.id} {i.name} {i.surname} {i.fathername}' for i in emp]
    form.id_employee.choices = emp
    if flask.request.method == 'POST':
            id_batch = flask.request.form['id_batch'].split()[0]
            id_drugstore = flask.request.form['id_drugstore'].split()[0]
            contract_date = flask.request.form['contract_date']
            id_employee = flask.request.form['id_employee'].split()[0]
            notes = flask.request.form['notes']
            ba = db.session.query(SupplayContract).get(sup_id)
            ba.id_batch = id_batch
            ba.id_drugstore = id_drugstore
            ba.contract_date = contract_date
            ba.id_employee = id_employee
            ba.notes = notes
            db.session.commit()
            return flask.redirect(f'/supplaycontract')
    return flask.render_template('supplaycontractf.html', form=form)


@userApp.route('/<int:id>')
@login_required
def user_page(user_id):
    model = User.query.filter_by(id=user_id).first()
    emp = Employee.query.filter_by(id=model.id_employee).first()
    p = Drugstore.query.filter_by(id=emp.id_drugstore).first()
    return flask.render_template("user_page.html", res=emp, pharm=p.name)


if __name__ == "__main__":
    userApp.run(debug=True,  port=8080)
