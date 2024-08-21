from fastapi import APIRouter
from flutter_app.routers.users import user
from flutter_app.routers.auth import auth
from flutter_app.routers.institution import institution
from flutter_app.routers.contact import contact_us
from flutter_app.routers.payment import payment
from flutter_app.routers.google_login import google_auth
from flutter_app.routers.blog import blog
from flutter_app.routers.comment import comment
from flutter_app.routers.billing_plan import bill_plan
from flutter_app.routers.faq import faq
from flutter_app.routers.notification_settings import notification_setting
from flutter_app.routers.payment_flutterwave import flutterwave_router
from flutter_app.routers.profile import profile
from flutter_app.routers.card import card_router
from flutter_app.routers.activity_logs import activity_logs


api_flutter_one = APIRouter(prefix="/api/flutter_app")

api_flutter_one.include_router(user)
api_flutter_one.include_router(auth)
api_flutter_one.include_router(institution)
api_flutter_one.include_router(contact_us)
api_flutter_one.include_router(payment)
api_flutter_one.include_router(google_auth)
api_flutter_one.include_router(blog)
api_flutter_one.include_router(comment)
api_flutter_one.include_router(faq)
api_flutter_one.include_router(notification_setting)
api_flutter_one.include_router(flutterwave_router)
api_flutter_one.include_router(activity_logs)
api_flutter_one.include_router(bill_plan)
api_flutter_one.include_router(profile)
api_flutter_one.include_router(card_router)










