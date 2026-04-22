from app import db


class Cuisine(db.Model):
    """菜系分類 Model"""
    __tablename__ = 'cuisines'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name       = db.Column(db.Text, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.func.now())

    # 關聯：一個菜系可有多道食譜
    recipes = db.relationship(
        'Recipe',
        back_populates='cuisine',
        lazy='select'
    )

    def __repr__(self):
        return f'<Cuisine id={self.id} name={self.name!r}>'

    # ── CRUD ──────────────────────────────────────────────────

    @classmethod
    def create(cls, name: str) -> 'Cuisine':
        """新增一個菜系，回傳 Cuisine 實例。"""
        cuisine = cls(name=name)
        db.session.add(cuisine)
        db.session.commit()
        return cuisine

    @classmethod
    def get_all(cls) -> list['Cuisine']:
        """取得所有菜系，依名稱排序。"""
        return cls.query.order_by(cls.name).all()

    @classmethod
    def get_by_id(cls, cuisine_id: int) -> 'Cuisine | None':
        """依 ID 取得單一菜系；找不到回傳 None。"""
        return cls.query.get(cuisine_id)

    @classmethod
    def update(cls, cuisine_id: int, name: str) -> 'Cuisine | None':
        """更新菜系名稱；找不到回傳 None。"""
        cuisine = cls.query.get(cuisine_id)
        if cuisine is None:
            return None
        cuisine.name = name
        db.session.commit()
        return cuisine

    @classmethod
    def delete(cls, cuisine_id: int) -> bool:
        """刪除指定菜系；成功回傳 True，找不到回傳 False。"""
        cuisine = cls.query.get(cuisine_id)
        if cuisine is None:
            return False
        db.session.delete(cuisine)
        db.session.commit()
        return True
