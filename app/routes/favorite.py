"""
app/routes/favorite.py
喜愛狀態 Blueprint — 負責切換食譜 is_favorite 的路由

URL 前綴：/recipes
"""

from flask import Blueprint

favorite_bp = Blueprint('favorite', __name__)


# ─────────────────────────────────────────────
# POST /recipes/<id>/favorite
# ─────────────────────────────────────────────
@favorite_bp.route('/recipes/<int:id>/favorite', methods=['POST'])
def toggle_favorite(id):
    """
    切換食譜的喜愛狀態（is_favorite toggle）。

    Path params:
        id (int): 食譜 ID

    Form fields:
        next (str, optional): 切換完成後重導向的 URL
                              預設回首頁 url_for('recipe.index')

    Logic:
        - 呼叫 Recipe.get_by_id(id)；找不到則 abort(404)
        - 呼叫 Recipe.toggle_favorite(id)

    Returns:
        redirect(request.form.get('next') or url_for('recipe.index'))
    Errors:
        404: 食譜不存在
    """
    pass
