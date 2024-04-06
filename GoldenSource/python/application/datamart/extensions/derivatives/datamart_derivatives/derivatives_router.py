"""Derivatives Router."""

from datamart_core.app.router import Router

from datamart_derivatives.futures.futures_router import router as futures_router
from datamart_derivatives.options.options_router import router as options_router

router = Router(prefix="")
router.include_router(options_router)
router.include_router(futures_router)
