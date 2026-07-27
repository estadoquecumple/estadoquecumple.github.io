from scripts.territorial.dnp_adapter import discover_downloads


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
