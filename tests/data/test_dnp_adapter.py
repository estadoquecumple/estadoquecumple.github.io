from scripts.territorial.dnp_adapter import discover_downloads
from scripts.territorial.common import PUBLIC, read_json


def test_discovers_only_official_download_formats_and_resolves_relative_urls():
    html = """
      <a href="/files/idf-2024.xlsx">IDF</a>
      <a href="https://dnp.gov.co/files/mdm.csv">MDM</a>
      <iframe src="https://app.powerbi.com/view"></iframe>
      <a href="javascript:alert(1)">unsafe</a>
    """
    assert discover_downloads("https://www.dnp.gov.co/page", html) == [
        "https://dnp.gov.co/files/mdm.csv",
        "https://www.dnp.gov.co/files/idf-2024.xlsx",
    ]


def test_official_dnp_products_have_explicit_period_hash_and_national_coverage():
    expected = {
        "typologies.json": ("dnp-typologies-2026", "2026"),
        "fiscal.json": ("dnp-idf-2024", "2024"),
        "municipal-performance.json": ("dnp-mdm", "2024"),
    }
    for filename, (source, period) in expected.items():
        document = read_json(PUBLIC / "indicators" / filename)
        assert document["source"] == source
        assert document["status"] == "current"
        assert document["dataPeriod"] == period
        assert len(document["inputHash"]) == 64
        assert document["coverage"] == {
            "municipalities": 1103,
            "departments": 32,
            "complete": True,
        }
        assert len(document["records"]) == 1135
