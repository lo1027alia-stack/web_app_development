from datetime import datetime

from app import db


class Recipe(db.Model):
    """食譜主表 Model"""
    __tablename__ = 'recipes'

    id                = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title             = db.Column(db.Text, nullable=False)
    description       = db.Column(db.Text, nullable=True)
    is_favorite       = db.Column(db.Boolean, nullable=False, default=False)
    video_url         = db.Column(db.Text, nullable=True)
    cover_image       = db.Column(db.Text, nullable=True)
    cook_time_minutes = db.Column(db.Integer, nullable=True)
    servings          = db.Column(db.Integer, nullable=True)
    cuisine_id        = db.Column(db.Integer,
                                  db.ForeignKey('cuisines.id', ondelete='SET NULL'),
                                  nullable=True)
    created_at        = db.Column(db.DateTime, nullable=False,
                                  default=datetime.now)
    updated_at        = db.Column(db.DateTime, nullable=False,
                                  default=datetime.now, onupdate=datetime.now)

    # 關聯
    cuisine     = db.relationship('Cuisine', back_populates='recipes')
    ingredients = db.relationship(
        'Ingredient',
        back_populates='recipe',
        cascade='all, delete-orphan',
        order_by='Ingredient.order_index',
        lazy='select'
    )
    steps = db.relationship(
        'Step',
        back_populates='recipe',
        cascade='all, delete-orphan',
        order_by='Step.step_number',
        lazy='select'
    )

    def __repr__(self):
        return f'<Recipe id={self.id} title={self.title!r}>'

    # ── CRUD ──────────────────────────────────────────────────

    @classmethod
    def create(cls,
               title: str,
               description: str | None = None,
               cuisine_id: int | None = None,
               video_url: str | None = None,
               cover_image: str | None = None,
               cook_time_minutes: int | None = None,
               servings: int | None = None) -> 'Recipe':
        """新增一道食譜，回傳 Recipe 實例。"""
        recipe = cls(
            title=title,
            description=description,
            cuisine_id=cuisine_id,
            video_url=video_url,
            cover_image=cover_image,
            cook_time_minutes=cook_time_minutes,
            servings=servings,
        )
        db.session.add(recipe)
        db.session.commit()
        return recipe

    @classmethod
    def get_all(cls,
                cuisine_id: int | None = None,
                only_favorites: bool = False) -> list['Recipe']:
        """
        取得食譜列表，支援篩選。

        Args:
            cuisine_id: 若提供，只回傳屬於該菜系的食譜。
            only_favorites: 若 True，只回傳喜愛食譜。
        """
        query = cls.query
        if cuisine_id is not None:
            query = query.filter_by(cuisine_id=cuisine_id)
        if only_favorites:
            query = query.filter_by(is_favorite=True)
        return query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, recipe_id: int) -> 'Recipe | None':
        """依 ID 取得單一食譜（含關聯 ingredients / steps）；找不到回傳 None。"""
        return cls.query.get(recipe_id)

    @classmethod
    def update(cls, recipe_id: int, **kwargs) -> 'Recipe | None':
        """
        更新食譜欄位。支援的 kwargs：
            title, description, cuisine_id, video_url,
            cover_image, cook_time_minutes, servings
        找不到食譜回傳 None。
        """
        recipe = cls.query.get(recipe_id)
        if recipe is None:
            return None
        allowed_fields = {
            'title', 'description', 'cuisine_id',
            'video_url', 'cover_image', 'cook_time_minutes', 'servings'
        }
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(recipe, field, value)
        recipe.updated_at = datetime.now()
        db.session.commit()
        return recipe

    @classmethod
    def toggle_favorite(cls, recipe_id: int) -> 'Recipe | None':
        """切換食譜的 is_favorite 狀態；找不到回傳 None。"""
        recipe = cls.query.get(recipe_id)
        if recipe is None:
            return None
        recipe.is_favorite = not recipe.is_favorite
        recipe.updated_at = datetime.now()
        db.session.commit()
        return recipe

    @classmethod
    def delete(cls, recipe_id: int) -> bool:
        """刪除指定食譜（連帶刪除 ingredients / steps）；成功回傳 True。"""
        recipe = cls.query.get(recipe_id)
        if recipe is None:
            return False
        db.session.delete(recipe)
        db.session.commit()
        return True

    @classmethod
    def search(cls, keyword: str) -> list['Recipe']:
        """依關鍵字搜尋食譜標題（Should Have）。"""
        pattern = f'%{keyword}%'
        return (cls.query
                .filter(cls.title.like(pattern))
                .order_by(cls.created_at.desc())
                .all())
