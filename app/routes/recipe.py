"""
app/routes/recipe.py
食譜 Blueprint — 負責食譜的 CRUD 路由

URL 前綴：
  - /           (首頁)
  - /recipes    (食譜資源)
"""

from flask import Blueprint

recipe_bp = Blueprint('recipe', __name__)


# ─────────────────────────────────────────────
# GET /
# ─────────────────────────────────────────────
@recipe_bp.route('/', methods=['GET'])
def index():
    """
    首頁 — 食譜列表頁。

    Query params:
        cuisine_id (int, optional): 依菜系篩選食譜
        favorites  (str, optional): 值為 '1' 時只顯示喜愛食譜

    Logic:
        - 呼叫 Recipe.get_all(cuisine_id, only_favorites) 取得食譜列表
        - 呼叫 Cuisine.get_all() 取得菜系選項（用於篩選 Tab）
        - 將 cuisine_id / favorites 參數回傳給模板以維持選取狀態

    Returns:
        render_template('index.html',
                        recipes=..., cuisines=...,
                        selected_cuisine=..., show_favorites=...)
    """
    pass


# ─────────────────────────────────────────────
# GET /recipes/<id>
# ─────────────────────────────────────────────
@recipe_bp.route('/recipes/<int:id>', methods=['GET'])
def recipe_detail(id):
    """
    食譜詳情頁。

    Path params:
        id (int): 食譜 ID

    Logic:
        - 呼叫 Recipe.get_by_id(id)，找不到則 abort(404)
        - 關聯載入 recipe.ingredients（依 order_index 排序）
        - 關聯載入 recipe.steps（依 step_number 排序）

    Returns:
        render_template('recipe/detail.html', recipe=...)
    Errors:
        404: 食譜不存在
    """
    pass


# ─────────────────────────────────────────────
# GET /recipes/new
# ─────────────────────────────────────────────
@recipe_bp.route('/recipes/new', methods=['GET'])
def recipe_new_form():
    """
    新增食譜表單頁（空白表單）。

    Logic:
        - 呼叫 Cuisine.get_all() 供下拉選單使用

    Returns:
        render_template('recipe/form.html',
                        recipe=None, cuisines=..., form_action='new')
    """
    pass


# ─────────────────────────────────────────────
# POST /recipes/new
# ─────────────────────────────────────────────
@recipe_bp.route('/recipes/new', methods=['POST'])
def recipe_create():
    """
    新增食譜（表單送出）。

    Form fields:
        title             (str, required)
        description       (str, optional)
        cuisine_id        (int, optional)
        video_url         (str, optional)
        cook_time_minutes (int, optional)
        servings          (int, optional)
        ingredient_name[] (list[str])
        ingredient_qty[]  (list[str])
        ingredient_unit[] (list[str])
        step_desc[]       (list[str])

    Logic:
        1. 驗證 title 非空；若失敗 flash error 並重新顯示表單
        2. 呼叫 Recipe.create(...) 建立食譜
        3. 呼叫 Ingredient.bulk_replace(recipe.id, ingredients_data)
        4. 呼叫 Step.bulk_replace(recipe.id, step_descriptions)

    Returns:
        成功 → redirect(url_for('recipe.recipe_detail', id=recipe.id))
        失敗 → render_template('recipe/form.html', ...) with errors
    """
    pass


# ─────────────────────────────────────────────
# GET /recipes/<id>/edit
# ─────────────────────────────────────────────
@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def recipe_edit_form(id):
    """
    編輯食譜表單頁（預填既有資料）。

    Path params:
        id (int): 食譜 ID

    Logic:
        - 呼叫 Recipe.get_by_id(id)，找不到則 abort(404)
        - 呼叫 Cuisine.get_all() 供下拉選單使用

    Returns:
        render_template('recipe/form.html',
                        recipe=..., cuisines=..., form_action='edit')
    Errors:
        404: 食譜不存在
    """
    pass


# ─────────────────────────────────────────────
# POST /recipes/<id>/edit
# ─────────────────────────────────────────────
@recipe_bp.route('/recipes/<int:id>/edit', methods=['POST'])
def recipe_update(id):
    """
    編輯食譜（表單送出）。

    Path params:
        id (int): 食譜 ID

    Form fields:
        同 recipe_create（新增表單欄位相同）

    Logic:
        1. 找不到食譜 → abort(404)
        2. 驗證 title 非空；若失敗 flash error 並重新顯示表單
        3. 呼叫 Recipe.update(id, ...)
        4. 呼叫 Ingredient.bulk_replace(id, ingredients_data)
        5. 呼叫 Step.bulk_replace(id, step_descriptions)

    Returns:
        成功 → redirect(url_for('recipe.recipe_detail', id=id))
        失敗 → render_template('recipe/form.html', ...) with errors
    Errors:
        404: 食譜不存在
    """
    pass


# ─────────────────────────────────────────────
# GET /recipes/<id>/delete
# ─────────────────────────────────────────────
@recipe_bp.route('/recipes/<int:id>/delete', methods=['GET'])
def recipe_delete_confirm(id):
    """
    刪除確認頁。

    Path params:
        id (int): 食譜 ID

    Logic:
        - 呼叫 Recipe.get_by_id(id) 取得食譜名稱供確認頁顯示
        - 找不到則 abort(404)

    Returns:
        render_template('recipe/confirm_delete.html', recipe=...)
    Errors:
        404: 食譜不存在
    """
    pass


# ─────────────────────────────────────────────
# POST /recipes/<id>/delete
# ─────────────────────────────────────────────
@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def recipe_delete(id):
    """
    刪除食譜（確認後執行）。

    Path params:
        id (int): 食譜 ID

    Logic:
        - 找不到食譜 → abort(404)
        - 呼叫 Recipe.delete(id)（CASCADE 自動刪除 ingredients / steps）

    Returns:
        redirect(url_for('recipe.index'))
    Errors:
        404: 食譜不存在
    """
    pass
