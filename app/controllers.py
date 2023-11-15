from flask import Flask, redirect, render_template, request, session, flash
from . import app
from . import web
from .web import func
import json
from datetime import datetime

def render(html, args=None):
    Get_All_Action=func(name="Get_All_Action")
    print(Get_All_Action)
    Get_All_User_NFTS=web.func("Get_All_User_NFT")
    lenNFTuser = len(Get_All_User_NFTS[0])
    _nft = []
    for i in range(lenNFTuser):
        _nft.append(json.load(open(f'./app/json/{"nft_" + str(Get_All_User_NFTS[0][i][0]) + ".json"}')))
    userCollection = web.func("Get_All_User_Collections")
    len_collection = len(userCollection)
    _collection = []
    for i in range(len_collection):
        _collection.append(json.load(open(f'./app/json/{"collection_" + str(userCollection[i][0]) + ".json"}')))
    return render_template(f"{html}.html",  
                           Get_All_Sell_NFT=func(name="Get_All_Sell_NFT"), 
                           Get_All_Action=func(name="Get_All_Action"),
                           address_contract=web.config['address'],
                           Get_Ballanse=web.func("Get_Ballanse"),
                           userNFT=_nft,
                           Get_One_Action=func(name="Get_One_Action", args=[args]),
                           _collection=_collection)


def check_result(res):
    if isinstance(res, str):
        flash(res.split("'")[1])
    else:
        flash('Успешно')


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        amount = request.form.get('amount', type=int)
        result = web.buy(amount)
        check_result(result)
    return render('base')


@app.route('/NFT', methods=["POST", "GET"])
def NFT():
    if request.method == "POST":
        amount = request.form.get('amount', type=int)
        id = request.form.get("id", type=int)
        result = web.func(name="Buy_NFT", args=[id, amount], operation="transact")
        check_result(result)
    return render('NFT')

# вывод всех аукционов , в каждом есть коллекция с нфт
@app.route('/Action')
def Action():
    return render("Action")


@app.route('/Action/<int:id>')
def ActionID(id):
    return render("ActionID", args=[id])


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
        return render('auth')
    return redirect('/lk')


@app.route('/SetNFT', methods=['GET', 'POST'])
def setNFT():
    if not session.get('user'): return redirect("/login")
    if request.method == "POST":
        id = web.func("variety_nft")
        name = request.form.get('name')
        description = request.form.get('description')
        amount = request.form.get("amount", type=int)
        price = request.form.get("price",  type=int)
        res = web.func(name="Set_Only_NFT", args=[amount, price], operation="transact")
        check_result(res)
        nftData = {
            "id":           id,
            "name":         name,
            "description":  description,
            "amount":       amount,
            "price":        price,
        }
        filename = f"./app/json/nft_{id}.json"
        with open(filename, 'w') as file:
            json.dump(nftData, file, indent=4)
    return render("SetNFT")


@app.route('/lk', methods=["GET", "POST"])
def lk():
    if not session.get('user'):
        return redirect('/login')
    if request.method == "POST":
        amount = request.form.get('amount', type=int)
        id = request.form.get("id", type=int)
        result = web.func(name="Sell_NFT", args=[id, amount], operation="transact")
        check_result(result)
    return render('lk')
    

@app.route('/Buy_Profi', methods=['GET', 'POST'])
def Buy_Profi():
    if not session.get('user'): return redirect("/login")
    if request.method == "POST":
        amount = request.form.get(amount)
        res = web.buy(amount)
        check_result(res)
    return render('Buy_Profi')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')



# создание колеции для добавления в нее нфт
@app.route('/setCollection', methods=["GET", 'POST'])
def SetCollection():
    if not session.get('user'): return redirect("/login")
    if request.method == "POST":
        name = request.form.get('name')
        description = request.form.get('description')
        res = web.func(name="Set_Collection", operation="transact")
        id = web.func("amount_collection")
        if type(res) == str:
            flash(res)
        else:
            collection_data = {
                "id":           id,
                "name":         name,
                "description":  description,
            }
            filename = f"./app/json/collection_{id}.json"
            with open(filename, 'w') as file:
                json.dump(collection_data, file, indent=4)
    return render('SetCollection')


# создает нфт специально для коллеции
@app.route('/SetNFTcollection/<int:id>', methods=["GET", 'POST'])
def SetNFTcollection(id):
    if not session.get('user'): return redirect('/login')
    if request.method == "POST":
        id = web.func("variety_nft")
        name = request.form.get('name')
        description = request.form.get('description')
        amount = request.form.get('amount', type=int)
        res = web.func("Set_NFT_In_Collection", args=[id, amount])
        check_result(res)
        nftData = {
            f"nft_{id}": {
                "id":           id,
                "name":         name,
                "description":  description,
                "amount":       amount,
            }
        }
        filename = f"./app/json/nft_{id}.json"
        with open(filename, 'w') as file:
            json.dump(nftData, file, indent=4)
    return render("SetNFTcollection")


# создание аукциона
@app.route('/setAction/<int:id>', methods=['GET', 'POST'])
def setAction(id):
    if not session.get('user'): return redirect('/login')
    if request.method == "POST":
        start = request.form.get('start')
        object_start = datetime.strptime(start, '%Y-%m-%dT%H:%M')
        _start = int(object_start.timestamp())

        end = request.form.get('end')
        object_end = datetime.strptime(end, '%Y-%m-%dT%H:%M')
        _end = int(object_end.timestamp())

        min = request.form.get('min', type=int)
        max = request.form.get('max', type=int)
        print(_start, _end, min, max)
        res = web.func("Set_Action", args=[id, _start, _end, min, max])
        print(res)
        check_result(res)
    return render("setAction")


# создание ставки к ауциону
@app.route('/Action/setBet/<int:id>', methods=['GET', 'POST'])
def setBet(id):
    if not session.get('user'): return redirect('/login')
    if request.method == "POST":
        bet = request.form.get("bet")
        res = web.func("Set_Bet_To_Action", args=[id, bet])
        check_result(res)
    return render("setBet")


# принудительное завершение
@app.route('/Action/endAaction/<int:id>', methods=['GET', 'POST'])
def endAction(id):
    if not session.get('user'): return redirect('/login')
    if request.method == 'POST':
        res = web.func("End_Action", args=[id])
    return render("endAction")

# переход на конкретный аукцион
# @app.route('/Action/<int:id>')
