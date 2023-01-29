"""Item Resource"""
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from app.models.item import ItemModel
from app.utils.logs import create_logger
from app.utils.encryption import encrypted_response


class Item(Resource):
    """Items Resource Class"""
    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('price', type=float, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('store_id', type=int, required=True,
                        help='Must enter the store id')

    def __init__(self):
        self.logger = create_logger()

    @jwt_required()  # Requires the token
    def get(self, name):
        """Record Get By Name"""
        item = ItemModel.find_by_name(name)
        self.logger.info('returning item:%s', item.json())
        if item:
            return encrypted_response(item)

        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        """Save Record"""
        self.logger.info(f'parsed args: {Item.parser.parse_args()}')

        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(
                name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except :
            return {'message': "An error occurred inserting the item."}, 500

        return  encrypted_response(item) ,201


    @jwt_required()
    def delete(self, name):
        """Delete Record"""
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return encrypted_response({'message': 'item has been deleted'}),200

    @jwt_required()
    def put(self, name):
        """Update Record"""
        # Create or Update
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()

        # if item:
        #     data=encrypted_response(item)

        return  encrypted_response(item)

class ItemList(Resource):
    """Items List Class"""
    @jwt_required()
    def get(self):
        """Get Item List"""

        return encrypted_response({'items': [item.json() for item in ItemModel.query.all()]})

        # return {
#     'items': [item.json() for item in ItemModel.query.all()]}
        # More pythonic
        ##return {'items': list(map(lambda x: x.json(),
        #  ItemModel.query.all()))} #Alternate Lambda way
