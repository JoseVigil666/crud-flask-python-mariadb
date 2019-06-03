from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators,IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, InputRequired
from passlib.hash import sha256_crypt
from functools import wraps
import mysql.connector as mariadb
from mysql.connector.errors import Error
from MFprg_products import products_fetchall
from MFsql_brands import sql_brands
from MFsql_customers import sql_customers

app = Flask(__name__,static_url_path='/static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

config = {
    'user': 'admin',
    'password': 'admin',
    'database': 'db_mfox'
}

# Register Form Class
class form_brands(Form):
    sbrand = StringField('Brand', [validators.Length(min=1, max=25)])

class form_customers(Form):
    iidcustomer     = StringField('ID')
    snamecustomer   = StringField('Name', [validators.Required("Please enter Customer Name"), validators.Length(min=3, max=100)])
    saddress        = StringField('Address',[validators.optional(), validators.Length(min=3, max=100)])
    scity           = StringField('City',[validators.optional(), validators.Length(min=3, max=50)])
    sstate          = StringField('State',  [validators.optional(),validators.Length(min=1, max=50)], default='New York')
    szipcode        = StringField('Zip Code', [validators.optional(),validators.Length(5)])
    semail          = EmailField ("Email",  [validators.optional(),validators.Length(max=70)])
    sphonenumeber   = StringField("Telephone Number", [validators.optional(),validators.Length(10)])


@app.route("/")
def startweb():
    return render_template('home.html')

@app.route("/products")
def products():
    cp = products_fetchall()
    return render_template ('MFproducts.html', cp = cp)

@app.route("/customers")
def customers():
    cp = sql_customers(config,'cursor','',())
    return render_template ('MFcustomers.html', cp = cp, title = 'cursor')

# Add customer
@app.route("/customers_add/<string:p_opt>", methods=['GET', 'POST'])
def customers_add(p_opt):
    print(p_opt)
    form = form_customers(request.form)
    if p_opt == 'populate':
        form.iidcustomer.data = form_customers.iidcustomer
        form.snamecustomer.data = snamecustomer
        form.saddress.data = saddress
        form.scity = scity
        form.sstate.data = sstate
        form.szipcode.data = szipcode
        form.semail.data = semail
        form.sphonenumeber.data = sphonenumeber

    if request.method == 'POST' and form.validate():

        iidcustomer     = form.iidcustomer.data
        snamecustomer   = form.snamecustomer.data
        saddress        = form.saddress.data
        scity           = form.scity.data
        sstate          = form.sstate.data
        szipcode        = form.szipcode.data
        semail          = form.semail.data
        sphonenumeber   = form.sphonenumeber.data

        customer_data = [
                iidcustomer,
                snamecustomer,
                saddress,
                scity,
                sstate,
                szipcode,
                semail,
                sphonenumeber
        ]

        result = sql_customers(config,'ins',iidcustomer, customer_data)
        print ('result',result)
        if result == 1:
            print("Oops! There was an error")
            opt = 'save'
            return redirect(url_for('customers_add',p_opt="save"))
        elif result == 0:
            opt = 'new'
            flash('You are now registered a new Customer', 'success')

        return redirect(url_for('customers_add',p_opt="populate"))

    return render_template ('MFcustomers.html', form = form, title = 'Add')

# Edite Customer
@app.route("/customers_upd/<string:key>", methods=['GET', 'POST'])
def customers_upd(key):

    register = sql_customers(config,'get',key,[0])
    form = form_customers(request.form)
    form.iidcustomer.data = key
    form.snamecustomer.data = register[1]
    form.saddress.data = register[2]
    form.scity = register[3]
    form.sstate.data = register[4]
    form.szipcode.data = register[5]
    form.semail.data = register[6]
    form.sphonenumeber.data = register[7]

    if request.method == 'POST' and form.validate():

        iidcustomer = key
        snamecustomer = form.snamecustomer.data
        saddress = form.saddress.data
        scity = form.scity.data
        sstate = form.sstate.data
        szipcode = form.szipcode.data
        semail = form.semail.data
        sphonenumeber = form.sphonenumeber.data

        customer_data = [
                iidcustomer,
                snamecustomer,
                saddress,
                scity,
                sstate,
                szipcode,
                semail,
                sphonenumeber
        ]

        result = sql_customers(config,'upd',key, customer_data)

        if result == 1:
            print("Oops! There was an error")
            return redirect('/customers_upd')
        elif result == 0:
            flash('Record was updated', 'success')

        return redirect('/customers_upd')

    return render_template ('MFcustomers.html', form = form, title = 'Edit')

# Delete Customer
@app.route("/customers_del/<string:key>", methods=['GET', 'POST'])
def customers_del(key):

    register = sql_customers(config,'del',key,[0])
    form = form_customers(request.form)
    form.iidcustomer.data = register[0]

    if request.method == 'POST' and form.validate():

        result = sql_customers(config,'del',key)

        if result == 1:
            print("Oops! There was an error")
            return redirect('/customers')
        elif result == 0:
            flash('Record was deleted', 'success')

        return redirect('/customers')

    return render_template ('MFcustomers.html', form = form, title = 'Remove')


@app.route("/brands")
def brands():
    cp = sql_brands(config,'cursor','')
    return render_template ('MFbrands.html', cp = cp, title = 'cursor')

# Add Brand
@app.route("/brands_add", methods=['GET', 'POST'])
def brands_add():

    form = form_brands(request.form)

    if request.method == 'POST' and form.validate():

        sbrand = form.sbrand.data

        result = sql_brands(config,'ins',sbrand)

        if result == 1:
            print("Oops! There was an error")
            return redirect('/brands_add')
        elif result == 0:
            flash('You are now registered a new brand', 'success')

        return redirect('/brands_add')

    return render_template ('MFbrands.html', form = form, title = 'Add')

# Edite Brand
@app.route("/brands_upd/<string:key>", methods=['GET', 'POST'])
def brands_upd(key):

    register = sql_brands(config,'get',key)
    form = form_brands(request.form)
    form.sbrand.data = register[0]

    if request.method == 'POST' and form.validate():

        sbrand = request.form['brand']

        result = sql_brands(config,'upd',key)

        if result == 1:
            print("Oops! There was an error")
            return redirect('/brands_upd')
        elif result == 0:
            flash('Record was updated', 'success')

        return redirect('/brands_upd')

    return render_template ('MFbrands.html', form = form, title = 'Edit')

# Delete Brand
@app.route("/brands_del/<string:key>", methods=['GET', 'POST'])
def brands_del(key):

    register = sql_brands(config,'get',key)
    form = form_brands(request.form)
    form.sbrand.data = register[0]

    if request.method == 'POST' and form.validate():

        result = sql_brands(config,'del',key)

        if result == 1:
            print("Oops! There was an error")
            return redirect('/brands')
        elif result == 0:
            flash('Record was deleted', 'success')

        return redirect('/brands')

    return render_template ('MFbrands.html', form = form, title = 'Remove')

if __name__ == "__main__":
    app.run(debug=True)
