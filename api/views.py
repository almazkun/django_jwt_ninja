from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)


@api.get("/protected", auth=JWTAuth())
def protected(request):
    return {"message": "Hello World!"}
