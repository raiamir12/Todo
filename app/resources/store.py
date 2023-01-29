"""Store Resource"""
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from app.models.store import StoreModel
from app.util.logz import create_logger
from app.util.encryption import encrypted_response


class Store(Resource):
    """Store Resource Class"""
    def __init__(self):
        self.logger = create_logger()

    def get(self, name):
        """Get Record BY Name"""
        store = StoreModel.find_by_name(name)
        if store:
            return encrypted_response(store)
        return {'message': 'Store not found'}, 404

    @jwt_required()  # Requires the token
    def post(self, name):
        """Save Data """
        if StoreModel.find_by_name(name):
            return {f"message": "A store with name '{name}' already exists."}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return encrypted_response(store), 201

    @jwt_required()  # Requires the token
    def delete(self, name):
        """Delete Data"""
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return encrypted_response({'message': 'Store deleted'})


class StoreList(Resource):
    """StoreList Class"""
    def get(self):
        """Get List Data"""
        return encrypted_response( {'stores': [store.json() for store in StoreModel.query.all()]})
        # return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
        #  #Alternate Lambda way
