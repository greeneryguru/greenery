from flask import current_app
from potnanny_core.database import db_session


"""
Class that handles the generic CRUD calls, data serialization and validation, etc
Initialization objects are:
    - a class
    - the marshmallow schema class used to validate/serialize
"""

class CrudInterface(object):
    def __init__(self, objclass, objschema):
        self._objclass = objclass
        self._objschema = objschema


    """
    GET object/objects

    notes on the callable:
        a list or tuple ['index_name', 'method_name']

        This is to have additional data added to get(pk) output... data that is
        not immediately available in an obj on instance creation, but must be
        gathered/calculated later by a method call to the object.
        The method call is made, and whatever it retures is added to the data
        dict under the index_name key.
    """
    def get(self, pk=None, post_callable=None):
        http_code = 200
        if not pk:
            r = self._objclass.query.all()
            if not r:
                return (None, {"message": "no data"}, 404)

            serialized, errors = self._objschema(many=True).dump(r)
            if errors:
                http_code = 400
        else:
            obj = self._objclass.query.get(pk)
            if not obj:
                return (None, {"message": "object does not exist"}, 404)

            serialized, errors = self._objschema().dump(obj)

            if post_callable:
                tag, m = post_callable
                serialized[tag] = getattr(obj, m)()

            if errors:
                http_code = 400

        return (serialized, errors, http_code)


    """
    CREATE object
    """
    def create(self, data):
        http_code = 200
        obj = self._objclass(**data)
        db.session.add(obj)
        db.session.commit()
        serialized, errors = self._objschema().dump(obj)

        if errors:
            http_code = 400

        return (serialized, errors, http_code)


    """
    EDIT object

    the pre-modification callback is a function that will be called before the
    object gets been modified.
    the callback func receives the Object, and the data passed.
    If callback returns a non-None result, the obj will not be edited.
    """
    def edit(self, pk, data, premod_callback=None):
        http_code = 200
        obj = self._objclass.query.get(pk)
        if not obj:
            return (None, {"message": "object does not exist"}, 404)

        if premod_callback:
            rval = premod_callback(obj, data)
            if rval:
                return (None, {"message": rval}, 400)

        for k,v in data.items():
            setattr(obj, k, v)

        db.session.commit()
        serialized, errors = self._objschema().dump(obj)
        if errors:
            http_code = 400

        return (serialized, errors, http_code)


    """
    DELETE object
    """
    def delete(self, pk):
        obj = self._objclass.query.get(pk)
        if not obj:
            return(None, {"message": "object does not exist"}, 404)

        db.session.delete(obj)
        db.session.commit()
        return("", None, 204)
