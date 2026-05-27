from cybershield_ai.services.evidence_vault import EvidenceVault


def test_evidence_hash_chain(tmp_path):
    db = tmp_path / "test.db"
    vault = EvidenceVault(str(db))
    rec1 = vault.add_text_evidence("case1", "screenshot.txt", "hello")
    rec2 = vault.add_text_evidence("case1", "chat.txt", "world")
    assert rec1.evidence_hash != rec2.evidence_hash
    assert rec1.chain_hash != rec2.chain_hash
    assert len(rec1.evidence_hash) == 64
