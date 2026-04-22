"""
app/routes/cuisine.py
菜系 Blueprint — 負責菜系分類的管理路由

URL 前綴：/cuisines
"""

from flask import Blueprint

cuisine_bp = Blueprint('cuisine', __name__)


# ─────────────────────────────────────────────
# GET /cuisines
# ─────────────────────────────────────────────
@cuisine_bp.route('/cuisines', methods=['GET'])
def cuisine_index():
    """
    菜系管理頁 — 顯示所有菜系列表。

    Logic:
        - 呼叫 Cuisine.get_all() 取得所有菜系（依名稱排序）

    Returns:
        render_template('cuisine/index.html', cuisines=...)
    """
    pass


# ─────────────────────────────────────────────
# POST /cuisines/new
# ─────────────────────────────────────────────
@cuisine_bp.route('/cuisines/new', methods=['POST'])
def cuisine_create():
    """
    新增菜系。

    Form fields:
        name (str, required): 菜系名稱（需唯一）

    Logic:
        1. 驗證 name 非空；若失敗 flash error 並重導向菜系管理頁
        2. 驗證 name 不重複（UNIQUE 約束）；若重複 flash error 並重導向
        3. 呼叫 Cuisine.create(name)

    Returns:
        redirect(url_for('cuisine.cuisine_index'))
    Errors:
        名稱為空   → flash('菜系名稱不可為空', 'error')
        名稱重複   → flash('此菜系已存在', 'error')
    """
    pass


# ─────────────────────────────────────────────
# POST /cuisines/<id>/delete
# ─────────────────────────────────────────────
@cuisine_bp.route('/cuisines/<int:id>/delete', methods=['POST'])
def cuisine_delete(id):
    """
    刪除菜系。

    Path params:
        id (int): 菜系 ID

    Logic:
        - 找不到菜系 → abort(404)
        - 呼叫 Cuisine.delete(id)
        - 該菜系下的食譜 cuisine_id 自動設為 NULL（ON DELETE SET NULL）

    Returns:
        redirect(url_for('cuisine.cuisine_index'))
    Errors:
        404: 菜系不存在
    """
    pass
