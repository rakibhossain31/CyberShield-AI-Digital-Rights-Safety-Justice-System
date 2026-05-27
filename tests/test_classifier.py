from cybershield_ai.services.case_classifier import classify_case


def test_blackmail_classifier():
    result = classify_case("They demand money and will leak private photo tonight")
    assert result.category == "blackmail"
    assert result.confidence > 0.5


def test_hacking_classifier():
    result = classify_case("Unauthorized login changed my password recovery phone")
    assert result.category == "hacking"
