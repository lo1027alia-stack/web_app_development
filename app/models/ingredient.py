from app import db


class Ingredient(db.Model):
    """食材清單 Model"""
    __tablename__ = 'ingredients'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id   = db.Column(db.Integer,
                            db.ForeignKey('recipes.id', ondelete='CASCADE'),
                            nullable=False)
    name        = db.Column(db.Text, nullable=False)
    quantity    = db.Column(db.Text, nullable=True)
    unit        = db.Column(db.Text, nullable=True)
    order_index = db.Column(db.Integer, nullable=False, default=0)

    # 關聯
    recipe = db.relationship('Recipe', back_populates='ingredients')

    def __repr__(self):
        return (f'<Ingredient id={self.id} recipe_id={self.recipe_id} '
                f'name={self.name!r}>')

    # ── CRUD ──────────────────────────────────────────────────

    @classmethod
    def create(cls,
               recipe_id: int,
               name: str,
               quantity: str | None = None,
               unit: str | None = None,
               order_index: int = 0) -> 'Ingredient':
        """新增一個食材，回傳 Ingredient 實例。"""
        ingredient = cls(
            recipe_id=recipe_id,
            name=name,
            quantity=quantity,
            unit=unit,
            order_index=order_index,
        )
        db.session.add(ingredient)
        db.session.commit()
        return ingredient

    @classmethod
    def get_all(cls, recipe_id: int) -> list['Ingredient']:
        """取得某食譜下所有食材，依 order_index 排序。"""
        return (cls.query
                .filter_by(recipe_id=recipe_id)
                .order_by(cls.order_index)
                .all())

    @classmethod
    def get_by_id(cls, ingredient_id: int) -> 'Ingredient | None':
        """依 ID 取得單一食材；找不到回傳 None。"""
        return cls.query.get(ingredient_id)

    @classmethod
    def update(cls,
               ingredient_id: int,
               name: str | None = None,
               quantity: str | None = None,
               unit: str | None = None,
               order_index: int | None = None) -> 'Ingredient | None':
        """更新食材資訊；找不到回傳 None。"""
        ingredient = cls.query.get(ingredient_id)
        if ingredient is None:
            return None
        if name is not None:
            ingredient.name = name
        if quantity is not None:
            ingredient.quantity = quantity
        if unit is not None:
            ingredient.unit = unit
        if order_index is not None:
            ingredient.order_index = order_index
        db.session.commit()
        return ingredient

    @classmethod
    def delete(cls, ingredient_id: int) -> bool:
        """刪除指定食材；成功回傳 True，找不到回傳 False。"""
        ingredient = cls.query.get(ingredient_id)
        if ingredient is None:
            return False
        db.session.delete(ingredient)
        db.session.commit()
        return True

    @classmethod
    def bulk_replace(cls, recipe_id: int, ingredients_data: list[dict]) -> list['Ingredient']:
        """
        批次替換某食譜的全部食材（先刪除舊的，再新增）。

        Args:
            recipe_id: 食譜 ID
            ingredients_data: List of dicts，每個 dict 需含 'name'，
                              可選含 'quantity'、'unit'

        Returns:
            新建立的 Ingredient 實例列表
        """
        cls.query.filter_by(recipe_id=recipe_id).delete()
        new_ingredients = []
        for idx, data in enumerate(ingredients_data):
            ingredient = cls(
                recipe_id=recipe_id,
                name=data['name'],
                quantity=data.get('quantity'),
                unit=data.get('unit'),
                order_index=idx,
            )
            db.session.add(ingredient)
            new_ingredients.append(ingredient)
        db.session.commit()
        return new_ingredients
