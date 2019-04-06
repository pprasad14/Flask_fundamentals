from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:MySqlp@ssw0rd@localhost/test'
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

mysql_db = SQLAlchemy(app)

# create SqlAlchemy Model
class Products(mysql_db.Model):
    __tablename__ = "products"
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    rate = mysql_db.Column(mysql_db.Integer, nullable=False)
    name = mysql_db.Column(mysql_db.String(20), nullable=False)

    def __init__(self, rate, name):
        self.rate = rate
        self.name = name

    def __repr__(self):
        return "<Products (%s, %s, %s)>" % (self.id, self.rate, self.name)

    @property
    def cols(self):
        return ["id", "rate", "name"]


def JsonPresent():
    try:
        if not request.json:
            return {"Error": "Empty Json"}
        return 0
    except:
        return {"Error": "No Json Found"}  # when not even empty {} is sent


def checkKeys(key_list):
    keys = request.get_json().keys()
    #    if len(keys)!=2:
    #        return ({"Error":"Incorrect No. of Keys"})
    for key in keys:
        if key not in key_list:
            return {"Error": "Incorrect Key Name Given"}
    return 0


@app.route('/product', methods=['POST'])
def createProduct():
    check = JsonPresent()
    if check != 0:
        return jsonify(check)

    keys = request.json.keys()

    check = checkKeys(['rate', 'name'])
    if check != 0:
        return jsonify(check)

    if not len(keys) == 2:  # or not 'rate' in keys or not 'name' in keys:
        return jsonify({"Error": "Incorrect No of Keys"})

    # fetch name and rate from the request
    rate = request.get_json()["rate"]
    name = request.get_json()["name"]
    #    return jsonify({"check":"yes"})

    #    return jsonify({"rate":rate, "name":name})
    #    or:   ({"rate":"{}".format(rate), "name":"{}".format(name)})

    product = Products(rate, name)  # prepare query statement

    try:
        mysql_db.session.add(product)  # add prepared statement to opened session
        mysql_db.session.commit()  # commit changes
    #        return jsonify({"check":"yes"})

    except:
        mysql_db.session.rollback()
        mysql_db.session.flush()  # for resetting non-committed .add()
    #        return jsonify({"check":"no"})

    productId = product.id  # fetch last inserted id
    #    return jsonify({"check":productId})

    data = Products.query.filter_by(id=productId).first()  # fetch our inserted product

    #    config.read('rating_db.conf')

    result = [data.name, data.rate]  # prepare visual data

    return jsonify(session=result)


@app.route('/product', methods=['GET'])
def show_all():
    all_products = Products.query.all()
    d_list = []  # to store list of dictionaries
    try:
        for prod in all_products:
            d_list.append([prod.id, prod.name, prod.rate])  # list of lists of products

        return jsonify(products=d_list)

        # to send a list of dictionaries:
        res = {}  # dictionary to send via jsonify as response
        l = []
        d = {}
        for prod in all_products:
            d['rate'] = prod.rate
            d['name'] = prod.name
            l.append(d)

        res["status"] = "success"
        res["data"] = l

        return jsonify(res)  # can only send dictionary object via jsonify

    except:
        return jsonify({"status": "unsuccessful"})


def databases(model_table_name, prod_id, new_dict):

    prod = model_table_name.query.filter_by(id=prod_id)

    new_data_list = []
    for key, value in new_dict.items():
        temp = [key, value]
        new_data_list.append(temp)

    new_dict_keys = new_dict.keys()

    if 'name' in new_dict_keys:
        for d in new_data_list:
            if d[0] == 'name':
                prod[0].name = d[1]
    if 'rate' in new_dict_keys:
        for d in new_data_list:
            if d[0] == 'rate':
                prod[0].rate = d[1]

    mysql_db.session.commit()
    prod = model_table_name.query.filter_by(id=prod_id)
    return [prod[0].name, prod[0].rate]


@app.route('/product/<int:prod_id>', methods=['PATCH'])
def updateProduct(prod_id):

    check = Products.query.filter_by(id=prod_id)
    try:
        check[0]
    except:
        return jsonify({"Error": "Product to Update Not Found"})

    check = JsonPresent() # to check if new json to be replaced is present
    if check != 0:
        return jsonify(check)

    check = checkKeys(['rate', 'name'])

    if check != 0:
        return jsonify(check)

    new_data = request.get_json()

    result = databases(Products, prod_id, new_data)

    return jsonify(session=result)


@app.route('/product/<int:prod_id>', methods=['DELETE'])
def deleteProduct(prod_id):
    try:
        Products.query.filter_by(id=prod_id).delete()
        mysql_db.session.commit()
        return show_all()

    except:
        return jsonify({"Error": "Product to Delete Not Found"})


if __name__ == "__main__":
    mysql_db.create_all()
    app.run()
