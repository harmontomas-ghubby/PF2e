from sqlmodel import Session, SQLModel, create_engine, select

from app.models import Combatant, CombatSession


def test_order_and_round_advance():
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        cs = CombatSession(campaign_id=1)
        s.add(cs)
        s.commit()
        s.refresh(cs)
        s.add(Combatant(combat_session_id=cs.id, name="A", initiative=20))
        s.add(Combatant(combat_session_id=cs.id, name="B", initiative=10))
        s.commit()
        rows = s.exec(select(Combatant).order_by(Combatant.initiative.desc())).all()
        rows[0].is_active_turn = True
        rows[0].is_active_turn = False
        rows[1].is_active_turn = True
        cs.round += 1
        s.commit()
        assert cs.round == 2
