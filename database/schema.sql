-- ============================================================
-- 食譜收藏夾系統 — SQLite 建表語法
-- 版本：v1.0　建立日期：2026-04-22
-- ============================================================

-- 啟用外鍵約束（SQLite 預設關閉，需手動開啟）
PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- 1. cuisines（菜系分類表）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cuisines (
    id         INTEGER  PRIMARY KEY AUTOINCREMENT,
    name       TEXT     NOT NULL UNIQUE,
    created_at DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- 預設菜系資料（MVP 初始資料）
INSERT OR IGNORE INTO cuisines (name) VALUES
    ('台式'),
    ('日式'),
    ('中式'),
    ('韓式'),
    ('義式'),
    ('美式'),
    ('泰式'),
    ('其他');

-- ------------------------------------------------------------
-- 2. recipes（食譜主表）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS recipes (
    id                INTEGER  PRIMARY KEY AUTOINCREMENT,
    title             TEXT     NOT NULL,
    description       TEXT,
    is_favorite       BOOLEAN  NOT NULL DEFAULT 0,
    video_url         TEXT,
    cover_image       TEXT,
    cook_time_minutes INTEGER,
    servings          INTEGER,
    cuisine_id        INTEGER  REFERENCES cuisines(id) ON DELETE SET NULL,
    created_at        DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at        DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ------------------------------------------------------------
-- 3. ingredients（食材清單表）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ingredients (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id   INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    name        TEXT    NOT NULL,
    quantity    TEXT,
    unit        TEXT,
    order_index INTEGER NOT NULL DEFAULT 0
);

-- ------------------------------------------------------------
-- 4. steps（烹飪步驟表）
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS steps (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id   INTEGER NOT NULL REFERENCES recipes(id) ON DELETE CASCADE,
    step_number INTEGER NOT NULL,
    description TEXT    NOT NULL
);
