# 食譜收藏夾系統 — 流程圖文件（FLOWCHART）

> **版本**：v1.0　｜　**建立日期**：2026-04-15　｜　**參考文件**：docs/PRD.md、docs/ARCHITECTURE.md

---

## 1. 使用者流程圖（User Flow）

描述使用者從進入網站到完成各項操作的完整路徑。

```mermaid
flowchart LR
    Start([🌐 使用者開啟網站]) --> Home[首頁\n食譜列表]

    Home --> Filter{想要篩選？}
    Filter -->|依菜系篩選| FilterCuisine[套用菜系過濾\n顯示對應食譜]
    Filter -->|切換喜愛| FilterFav[只看我的最愛]
    FilterCuisine --> Home
    FilterFav --> Home

    Home --> Action{選擇操作}

    %% 查看食譜
    Action -->|點選食譜卡片| Detail[食譜詳情頁\n食材 + 步驟 + 影片]
    Detail --> DetailAction{繼續操作？}
    DetailAction -->|編輯| EditForm[編輯食譜表單]
    DetailAction -->|刪除| ConfirmDelete{確認刪除？}
    DetailAction -->|返回列表| Home
    EditForm -->|送出| UpdateDB[(更新資料庫)]
    UpdateDB --> Detail
    ConfirmDelete -->|確認| DeleteDB[(從資料庫刪除)]
    ConfirmDelete -->|取消| Detail
    DeleteDB --> Home

    %% 新增食譜
    Action -->|點擊新增按鈕| NewForm[新增食譜表單\n填寫標題/菜系/食材/步驟/影片]
    NewForm --> Validate{表單驗證}
    Validate -->|驗證失敗| NewForm
    Validate -->|驗證通過| SaveDB[(儲存至資料庫)]
    SaveDB --> Detail

    %% 切換喜愛
    Action -->|點擊愛心| ToggleFav[(切換 is_favorite)]
    ToggleFav --> Home

    %% 管理菜系
    Action -->|進入菜系管理| CuisineMgmt[菜系管理頁]
    CuisineMgmt --> CuisineAction{操作}
    CuisineAction -->|新增菜系| AddCuisine[(新增菜系至資料庫)]
    CuisineAction -->|刪除菜系| DelCuisine[(刪除菜系)]
    AddCuisine --> CuisineMgmt
    DelCuisine --> CuisineMgmt
```

---

## 2. 系統序列圖（System Sequence Diagrams）

### 2.1 新增食譜

描述使用者填寫表單到資料成功寫入資料庫的完整流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\n(routes/recipe.py)
    participant Model as Model\n(models/recipe.py)
    participant DB as SQLite\n(database.db)

    User->>Browser: 點擊「新增食譜」按鈕
    Browser->>Flask: GET /recipes/new
    Flask-->>Browser: 回傳新增食譜表單頁面

    User->>Browser: 填寫標題、菜系、食材、步驟、影片URL
    User->>Browser: 點擊送出
    Browser->>Flask: POST /recipes/new

    Flask->>Flask: 驗證表單（標題不得為空等）

    alt 驗證失敗
        Flask-->>Browser: 重新渲染表單，顯示錯誤提示
    else 驗證通過
        Flask->>Model: 建立 Recipe 物件
        Model->>DB: INSERT INTO recipes ...
        DB-->>Model: 回傳新增的 recipe.id
        Model-->>Flask: 回傳 Recipe 實例
        Flask-->>Browser: 重導向至 GET /recipes/<id>
        Browser->>Flask: GET /recipes/<id>
        Flask->>Model: Recipe.query.get(id)
        Model->>DB: SELECT * FROM recipes WHERE id=?
        DB-->>Model: 食譜資料
        Model-->>Flask: Recipe 物件
        Flask-->>Browser: 渲染食譜詳情頁
    end
```

---

### 2.2 查看食譜詳情

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model
    participant DB as SQLite

    User->>Browser: 點擊食譜卡片
    Browser->>Flask: GET /recipes/<id>
    Flask->>Model: Recipe.query.get(id)\n含關聯的 ingredients、steps
    Model->>DB: SELECT recipes, ingredients, steps WHERE recipe_id=?
    DB-->>Model: 完整食譜資料
    Model-->>Flask: Recipe 物件（含關聯）
    Flask-->>Browser: render_template('recipe/detail.html', recipe=recipe)
    Browser-->>User: 顯示食材清單、步驟、影片連結
```

---

### 2.3 切換喜愛狀態

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route\n(routes/favorite.py)
    participant Model as Model
    participant DB as SQLite

    User->>Browser: 點擊愛心圖示（toggle）
    Browser->>Flask: POST /recipes/<id>/favorite
    Flask->>Model: Recipe.query.get(id)
    Model->>DB: SELECT is_favorite FROM recipes WHERE id=?
    DB-->>Model: 目前狀態（True / False）
    Model->>DB: UPDATE recipes SET is_favorite=NOT is_favorite WHERE id=?
    DB-->>Model: 更新成功
    Flask-->>Browser: 重導向至原頁面（或回傳 JSON）
    Browser-->>User: 愛心圖示狀態更新
```

---

### 2.4 刪除食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model
    participant DB as SQLite

    User->>Browser: 點擊「刪除」按鈕
    Browser->>Flask: GET /recipes/<id>/delete
    Flask-->>Browser: 渲染刪除確認頁面

    User->>Browser: 點擊「確認刪除」
    Browser->>Flask: POST /recipes/<id>/delete
    Flask->>Model: Recipe.query.get(id)
    Model->>DB: DELETE FROM recipes WHERE id=?\n（連帶刪除 ingredients、steps）
    DB-->>Model: 刪除成功
    Flask-->>Browser: 重導向至首頁 GET /
    Browser-->>User: 回到食譜列表，該食譜已消失
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | 對應 Blueprint |
|---|---|---|---|
| 首頁 / 食譜列表 | `/` | GET | `recipe` |
| 食譜詳情 | `/recipes/<id>` | GET | `recipe` |
| 新增食譜（表單頁） | `/recipes/new` | GET | `recipe` |
| 新增食譜（送出） | `/recipes/new` | POST | `recipe` |
| 編輯食譜（表單頁） | `/recipes/<id>/edit` | GET | `recipe` |
| 編輯食譜（送出） | `/recipes/<id>/edit` | POST | `recipe` |
| 刪除確認頁 | `/recipes/<id>/delete` | GET | `recipe` |
| 刪除食譜 | `/recipes/<id>/delete` | POST | `recipe` |
| 切換喜愛狀態 | `/recipes/<id>/favorite` | POST | `favorite` |
| 菜系管理頁 | `/cuisines` | GET | `cuisine` |
| 新增菜系 | `/cuisines/new` | POST | `cuisine` |
| 刪除菜系 | `/cuisines/<id>/delete` | POST | `cuisine` |

---

*此文件為動態文件，隨開發進程持續更新。*
