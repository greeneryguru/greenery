
class CrudInterface(object):
    """
    Class that handles the CRUD type object operations, data serialization and
    validation, etc

    Initialization args:
        - sqlalchemy db session
        - a class
        - the marshmallow schema class used to validate/serialize class objects
    """

    def __init__(self, session, objclass, objschema):
        self._objclass = objclass
        self._objschema = objschema
        self._db = session


    def get(self, pk=None):
        """
        GET object/objects

        args:
            - int: (optional)
        returns:
            tuple: (data, errors, http_code)
        """

        http_code = 200
        data = None
        errors = None

        if pk is None:
            r = self._objclass.query.all()
            if not r:
                return (None, {"msg": "no data"}, 404)

            data, errors = self._objschema(many=True).dump(r)
            if errors:
                http_code = 400
        else:
            obj = self._objclass.query.get(int(pk))
            if not obj:
                return (None, {"msg": "object does not exist"}, 404)

            data, errors = self._objschema().dump(obj)

        return (data, errors, http_code)


    def create(self, data):
        """
        CREATE object

        args:
            - dict
        returns:
            tuple: (data, errors, http_code)
        """

        http_code = 200
        try:
            obj = self._objclass(**data)
            self._db.add(obj)
            self._db.commit()
        except Exception as x:
            return (None, x, 400)

        data, errors = self._objschema().dump(obj)
        if errors:
            http_code = 400

        return (data, errors, http_code)


    def edit(self, pk, data):
        """
        EDIT object with id

        args:
            - int
            - dict

        returns:
            tuple: (data, errors, http_code)
        """

        http_code = 200
        obj = self._objclass.query.get(pk)
        if not obj:
            return (None, {"msg": "object does not exist"}, 404)

        try:
            for k,v in data.items():
                setattr(obj, k, v)
        except:
            pass

        self._db.commit()
        data, errors = self._objschema().dump(obj)
        if errors:
            http_code = 400

        return (data, errors, http_code)


    def delete(self, pk):
        """
        DELETE object with id

        args:
            - int

        returns:
            tuple: (data, errors, http_code)
        """

        obj = self._objclass.query.get(pk)
        if not obj:
            return(None, {"msg": "object does not exist"}, 404)

        self._db.delete(obj)
        self._db.commit()
        return("", None, 204)
