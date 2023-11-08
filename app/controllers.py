from flask import Flask, redirect, render_template, request, session, flash
from . import app
from . import web
from .web import func


# request.form - возможно получится проверять и использовать несколько функции на одной странице!!!!!!!
def check_result(res):
    if isinstance(res, str):
        flash(res)
    else:
        flash('Успешно')

def check_session(html):
    if not session.get('user'):
        return redirect("/login")
    return render_template(f"{html}.html")

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        amount = request.form.get('amount', type=int)
        result = web.buy(amount)
        check_result(result)
    return render_template('base.html', address_contract=web.config['address'])


@app.route('/NFT', methods=["POST", "GET"])
def NFT():
    if request.method == "POST":
        amount = request.form.get('amount', type=int)
        id = request.form.get("id", type=int)
        result = web.func(name="Buy_NFT", args=[id, amount], operation="transact")
        check_result(result)
    return render_template('NFT.html', Get_All_Sell_NFT=func(name="Get_All_Sell_NFT"))


@app.route('/Action')
def Action():
    return render_template('Action.html', Get_All_Action=func(name="Get_All_Action"))


@app.route('/Action/<int:id>')
def ActionID(id):
    return render_template('ActionID.html', Get_One_Action=func(name="Get_One_Action", args=[id]))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not session.get('user'):
        if request.method == "POST":
            key = request.form.get('key')
            res = web.key_check(key)
            if type(res) == str:
                flash(res)
            else:
                session['user'] = res
                return redirect('/lk')
        return render_template('auth.html')
    return redirect('/lk')


@app.route('/Set_Only_NFT', methods=['GET', 'POST'])
def set():
    if request.method == "POST":
        amount = request.form.get("amount", type=int)
        price = request.form.get("price",  type=int)
        res = web.func(name="Set_Only_NFT", args=[amount, price], operation="transact")
        check_result(res)
    return check_session("Set_Only_NFT")


@app.route('/lk', methods=["GET", "POST"])
def lk():
    if not session.get('user'):
        return redirect('/login')
    Get_All_User_NFT=web.func("Get_All_User_NFT")
    res = zip(Get_All_User_NFT[0], Get_All_User_NFT[1])
    if request.method == "POST":
        amount = request.form.get('amount', type=int)
        id = request.form.get("id", type=int)
        result = web.func(name="Sell_NFT", args=[id, amount], operation="transact")
        print(res)
        check_result(result)
    return render_template('lk.html', res=res,  Get_All_User_Collection=web.func("Get_All_User_Collections"), Get_Ballanse=web.func("Get_Ballanse"))
    

@app.route('/Buy_Profi', methods=['GET', 'POST'])
def Buy_Profi():
    if request.method == "POST":
        amount = request.form.get(amount)
        res = web.buy(amount)
        check_result(res)
    return check_session('Buy_Profi')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


