from app.services.dice_engine import roll


def test_keep_drop_explode():
    r = roll("4d6kh3", seed=1)
    assert isinstance(r["total"], int)
    r2 = roll("1d6!", seed=2)
    assert r2["total"] >= 1


def test_adv_dis_and_label():
    r = roll("attack: 1d20+5")
    assert r["label"] == "attack"
    a = roll("d20 adv", seed=1)
    d = roll("d20 dis", seed=1)
    assert a["total"] >= d["total"]
