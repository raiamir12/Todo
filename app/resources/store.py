from flask_restful import Resource
from app.models.store import StoreModel
from flask_jwt_extended import jwt_required
from app.util.logz import create_logger
from app.util.ecryption import encrypted_response


class Store(Resource):

    def __init__(self):
        self.logger = create_logger()

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return encrypted_response(store)
        return {'message': 'Store not found'}, 404

    @jwt_required()  # Requires the token
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return encrypted_response(store), 201

    @jwt_required()  # Requires the token
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return encrypted_response({'message': 'Store deleted'})


class StoreList(Resource):
    def get(self):
        return encrypted_response( {'stores': [store.json() for store in StoreModel.query.all()]})
        # return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))} #Alternate Lambda way
