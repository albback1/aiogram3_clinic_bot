from .start import common_router
from .enrollment import enroll_router
from .fallback import fallback_router
from .group_handler import group_router
from .price_list import price_router
from .questions import question_router

router = common_router
router.include_router(enroll_router)
router.include_router(price_router)
router.include_router(question_router)
router.include_router(group_router)
router.include_router(fallback_router) # Должен стоять в конце, чтобы не перехватывать 
                                       # callback'и, обрабатываемые в других файла 
