# 食譜收藏夾系統 — 路由設計文件（ROUTES）

> **版本**：v1.0　｜　**建立日期**：2026-04-22　｜　**參考文件**：docs/PRD.md、docs/ARCHITECTURE.md、docs/DB_DESIGN.md

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | Blueprint | 對應模板 | 說明 |
|---|---|---|---|---|---|
| 首頁 / 食譜列表 | GET | `/` | `recipe` | `index.html` | 顯示全部食譜，支援菜系篩選與喜愛篩選 |
| 食譜詳情 | GET | `/recipes/<int:id>` | `recipe` | `recipe/detail.html` | 顯示單筆食譜（含食材、步驟、影片） |
| 新增食譜（表單頁） | GET | `/recipes/new` | `recipe` | `recipe/form.html` | 顯示空白新增表單 |
| 新增食譜（送出） | POST | `/recipes/new` | `recipe` | — | 驗證並寫入 DB，重導向至詳情頁 |
| 編輯食譜（表單頁） | GET | `/recipes/<int:id>/edit` | `recipe` | `recipe/form.html` | 顯示預填編輯表單（重用 form.html） |
| 編輯食譜（送出） | POST | `/recipes/<int:id>/edit` | `recipe` | — | 驗證並更新 DB，重導向至詳情頁 |
| 刪除確認頁 | GET | `/recipes/<int:id>/delete` | `recipe` | `recipe/confirm_delete.html` | 顯示刪除確認頁面 |
| 刪除食譜 | POST | `/recipes/<int:id>/delete` | `recipe` | — | 刪除食譜及關聯資料，重導向至首頁 |
| 切換喜愛狀態 | POST | `/recipes/<int:id>/favorite` | `favorite` | — | Toggle is_favorite，重導向回原頁 |
| 菜系管理頁 | GET | `/cuisines` | `cuisine` | `cuisine/index.html` | 顯示所有菜系列表 |
| 新增菜系 | POST | `/cuisines/new` | `cuisine` | — | 新增菜系，重導向至菜系管理頁 |
| 刪除菜系 | POST | `/cuisines/<int:id>/delete` | `cuisine` | — | 刪除菜系，重導向至菜系管理頁 |

---

## 2. 每個路由的詳細說明

---

### Blueprint: `recipe`（`app/routes/recipe.py`）

---

#### `GET /` — 首頁 / 食譜列表

| 項目 | 說明 |
|---|---|
| **函式名稱** | `index` |
| **URL 參數** | `cuisine_id`（int, 選填）：篩選指定菜系；`favorites`（bool, 選填）：只顯示喜愛 |
| **處理邏輯** | 呼叫 `Recipe.get_all(cuisine_id, only_favorites)`；呼叫 `Cuisine.get_all()` 取得篩選選項 |
| **輸出** | `render_template('index.html', recipes=..., cuisines=..., ...)` |
| **錯誤處理** | 無特殊處理，查無資料時顯示空列表提示 |

---

#### `GET /recipes/<int:id>` — 食譜詳情

| 項目 | 說明 |
|---|---|
| **函式名稱** | `recipe_detail` |
| **URL 參數** | `id`（int）：食譜 ID |
| **處理邏輯** | 呼叫 `Recipe.get_by_id(id)`，關聯載入 `ingredients`（按 order_index）與 `steps`（按 step_number） |
| **輸出** | `render_template('recipe/detail.html', recipe=...)` |
| **錯誤處理** | 找不到食譜 → `abort(404)` |

---

#### `GET /recipes/new` — 新增食譜表單頁

| 項目 | 說明 |
|---|---|
| **函式名稱** | `recipe_new_form` |
| **URL 參數** | 無 |
| **處理邏輯** | 呼叫 `Cuisine.get_all()` 供表單菜系下拉選單使用 |
| **輸出** | `render_template('recipe/form.html', cuisines=..., recipe=None)` |
| **錯誤處理** | 無 |

---

#### `POST /recipes/new` — 新增食譜（送出）

| 項目 | 說明 |
|---|---|
| **函式名稱** | `recipe_create` |
| **表單欄位** | `title`（必填）、`description`、`cuisine_id`、`video_url`、`cook_time_minutes`、`servings`、`ingredients[]`（name/quantity/unit 陣列）、`steps[]`（description 陣列） |
| **處理邏輯** | 1. 驗證 `title` 非空；2. 呼叫 `Recipe.create(...)`；3. 呼叫 `Ingredient.bulk_replace()`；4. 呼叫 `Step.bulk_replace()` |
| **輸出** | 成功 → `redirect(url_for('recipe.recipe_detail', id=recipe.id))`；失敗 → 重新渲染表單並帶錯誤訊息 |
| **錯誤處理** | `title` 為空 → flash error，重新顯示表單 |

---

#### `GET /recipes/<int:id>/edit` — 編輯食譜表單頁

| 項目 | 說明 |
|---|---|
| **函式名稱** | `recipe_edit_form` |
| **URL 參數** | `id`（int）：食譜 ID |
| **處理邏輯** | 呼叫 `Recipe.get_by_id(id)` 取得既有資料；呼叫 `Cuisine.get_all()` 供下拉選單使用 |
| **輸出** | `render_template('recipe/form.html', recipe=..., cuisines=...)` |
| **錯誤處理** | 找不到食譜 → `abort(404)` |

---

#### `POST /recipes/<int:id>/edit` — 編輯食譜（送出）

| 項目 | 說明 |
|---|---|
| **函式名稱** | `recipe_update` |
| **URL 參數** | `id`（int）：食譜 ID |
| **表單欄位** | 同新增表單 |
| **處理邏輯** | 1. 驗證 `title`；2. 呼叫 `Recipe.update(id, ...)`；3. 呼叫 `Ingredient.bulk_replace()`；4. 呼叫 `Step.bulk_replace()` |
| **輸出** | 成功 → `redirect(url_for('recipe.recipe_detail', id=id))`；失敗 → 重新渲染表單 |
| **錯誤處理** | 找不到食譜 → `abort(404)`；`title` 為空 → flash error |

---

#### `GET /recipes/<int:id>/delete` — 刪除確認頁

| 項目 | 說明 |
|---|---|
| **函式名稱** | `recipe_delete_confirm` |
| **URL 參數** | `id`（int）：食譜 ID |
| **處理邏輯** | 呼叫 `Recipe.get_by_id(id)` 取得食譜名稱供確認頁顯示 |
| **輸出** | `render_template('recipe/confirm_delete.html', recipe=...)` |
| **錯誤處理** | 找不到食譜 → `abort(404)` |

---

#### `POST /recipes/<int:id>/delete` — 刪除食譜

| 項目 | 說明 |
|---|---|
| **函式名稱** | `recipe_delete` |
| **URL 參數** | `id`（int）：食譜 ID |
| **處理邏輯** | 呼叫 `Recipe.delete(id)`（CASCADE 自動刪除 ingredients / steps） |
| **輸出** | `redirect(url_for('recipe.index'))` |
| **錯誤處理** | 找不到食譜 → `abort(404)` |

---

### Blueprint: `favorite`（`app/routes/favorite.py`）

---

#### `POST /recipes/<int:id>/favorite` — 切換喜愛狀態

| 項目 | 說明 |
|---|---|
| **函式名稱** | `toggle_favorite` |
| **URL 參數** | `id`（int）：食譜 ID |
| **表單欄位** | `next`（選填）：完成後重導向的 URL，預設回首頁 |
| **處理邏輯** | 呼叫 `Recipe.toggle_favorite(id)` |
| **輸出** | `redirect(request.form.get('next') or url_for('recipe.index'))` |
| **錯誤處理** | 找不到食譜 → `abort(404)` |

---

### Blueprint: `cuisine`（`app/routes/cuisine.py`）

---

#### `GET /cuisines` — 菜系管理頁

| 項目 | 說明 |
|---|---|
| **函式名稱** | `cuisine_index` |
| **URL 參數** | 無 |
| **處理邏輯** | 呼叫 `Cuisine.get_all()` |
| **輸出** | `render_template('cuisine/index.html', cuisines=...)` |
| **錯誤處理** | 無 |

---

#### `POST /cuisines/new` — 新增菜系

| 項目 | 說明 |
|---|---|
| **函式名稱** | `cuisine_create` |
| **表單欄位** | `name`（必填）：菜系名稱 |
| **處理邏輯** | 驗證 `name` 非空且不重複；呼叫 `Cuisine.create(name)` |
| **輸出** | `redirect(url_for('cuisine.cuisine_index'))` |
| **錯誤處理** | 名稱為空或重複 → flash error，重導向菜系管理頁 |

---

#### `POST /cuisines/<int:id>/delete` — 刪除菜系

| 項目 | 說明 |
|---|---|
| **函式名稱** | `cuisine_delete` |
| **URL 參數** | `id`（int）：菜系 ID |
| **處理邏輯** | 呼叫 `Cuisine.delete(id)`（食譜的 cuisine_id 自動設為 NULL） |
| **輸出** | `redirect(url_for('cuisine.cuisine_index'))` |
| **錯誤處理** | 找不到菜系 → `abort(404)` |

---

## 3. Jinja2 模板清單

| 模板檔案路徑 | 繼承自 | 說明 |
|---|---|---|
| `templates/base.html` | — | 基礎模板：導覽列、Flash 訊息、全域 CSS / JS |
| `templates/index.html` | `base.html` | 首頁：食譜卡片列表、菜系篩選 Tabs、喜愛切換按鈕 |
| `templates/recipe/detail.html` | `base.html` | 食譜詳情：食材表、步驟清單、影片連結、編輯 / 刪除按鈕 |
| `templates/recipe/form.html` | `base.html` | 新增 / 編輯共用表單：動態增減食材列、動態增減步驟列 |
| `templates/recipe/confirm_delete.html` | `base.html` | 刪除確認頁：顯示食譜名稱、確認 / 取消按鈕 |
| `templates/cuisine/index.html` | `base.html` | 菜系管理頁：菜系列表、新增表單（行內）、刪除按鈕 |

---

## 4. Flask Blueprint 骨架對照

| Blueprint 名稱 | 檔案 | URL 前綴 |
|---|---|---|
| `recipe` | `app/routes/recipe.py` | `/`（首頁）、`/recipes` |
| `favorite` | `app/routes/favorite.py` | `/recipes` |
| `cuisine` | `app/routes/cuisine.py` | `/cuisines` |

骨架程式碼存放於 `app/routes/` 目錄下，詳見各 `.py` 檔案。

---

*此文件為動態文件，隨開發進程持續更新。*
