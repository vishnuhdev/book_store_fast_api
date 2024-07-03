from fastapi import FastAPI

from app.api.endpoints.category_routers import category_router
from app.api.endpoints.book_routers import book_router
from app.api.endpoints.author_routers import author_router
from app.api.endpoints.review_routers import review_routers
from app.api.endpoints.user_routers import user_router
app = FastAPI()


app.include_router(book_router)
app.include_router(author_router)
app.include_router(user_router)
app.include_router(review_routers)
app.include_router(category_router)
