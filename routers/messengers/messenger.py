from fastapi import APIRouter
from . import telegram
from . import whatsapp

router = APIRouter(prefix="/messengers",
                   )

router.include_router(telegram.router)
router.include_router(whatsapp.router)
