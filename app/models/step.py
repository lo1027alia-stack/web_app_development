from app import db


class Step(db.Model):
    """烹飪步驟 Model"""
    __tablename__ = 'steps'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id   = db.Column(db.Integer,
                            db.ForeignKey('recipes.id', ondelete='CASCADE'),
                            nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    # 關聯
    recipe = db.relationship('Recipe', back_populates='steps')

    def __repr__(self):
        return (f'<Step id={self.id} recipe_id={self.recipe_id} '
                f'step_number={self.step_number}>')

    # ── CRUD ──────────────────────────────────────────────────

    @classmethod
    def create(cls,
               recipe_id: int,
               step_number: int,
               description: str) -> 'Step':
        """新增一個烹飪步驟，回傳 Step 實例。"""
        step = cls(
            recipe_id=recipe_id,
            step_number=step_number,
            description=description,
        )
        db.session.add(step)
        db.session.commit()
        return step

    @classmethod
    def get_all(cls, recipe_id: int) -> list['Step']:
        """取得某食譜下所有步驟，依 step_number 排序。"""
        return (cls.query
                .filter_by(recipe_id=recipe_id)
                .order_by(cls.step_number)
                .all())

    @classmethod
    def get_by_id(cls, step_id: int) -> 'Step | None':
        """依 ID 取得單一步驟；找不到回傳 None。"""
        return cls.query.get(step_id)

    @classmethod
    def update(cls,
               step_id: int,
               step_number: int | None = None,
               description: str | None = None) -> 'Step | None':
        """更新步驟資訊；找不到回傳 None。"""
        step = cls.query.get(step_id)
        if step is None:
            return None
        if step_number is not None:
            step.step_number = step_number
        if description is not None:
            step.description = description
        db.session.commit()
        return step

    @classmethod
    def delete(cls, step_id: int) -> bool:
        """刪除指定步驟；成功回傳 True，找不到回傳 False。"""
        step = cls.query.get(step_id)
        if step is None:
            return False
        db.session.delete(step)
        db.session.commit()
        return True

    @classmethod
    def bulk_replace(cls, recipe_id: int, descriptions: list[str]) -> list['Step']:
        """
        批次替換某食譜的全部步驟（先刪除舊的，再新增）。

        Args:
            recipe_id: 食譜 ID
            descriptions: 步驟說明的列表，順序即為 step_number（從 1 開始）

        Returns:
            新建立的 Step 實例列表
        """
        cls.query.filter_by(recipe_id=recipe_id).delete()
        new_steps = []
        for idx, desc in enumerate(descriptions, start=1):
            step = cls(
                recipe_id=recipe_id,
                step_number=idx,
                description=desc,
            )
            db.session.add(step)
            new_steps.append(step)
        db.session.commit()
        return new_steps
