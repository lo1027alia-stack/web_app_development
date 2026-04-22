# app/routes/__init__.py
# 集中匯出所有 Blueprint，供 app/__init__.py 統一註冊

from app.routes.recipe   import recipe_bp
from app.routes.favorite import favorite_bp
from app.routes.cuisine  import cuisine_bp

__all__ = ['recipe_bp', 'favorite_bp', 'cuisine_bp']
