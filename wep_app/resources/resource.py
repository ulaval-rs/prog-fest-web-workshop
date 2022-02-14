from flask_restful import Resource


class APIResource(Resource):

    def __call__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        return self

    @property
    def __name__(self):
        return type(self).__name__
