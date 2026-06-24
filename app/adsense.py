import os

def adsense_script():
    enabled = os.getenv("ADSENSE_ENABLED", "false").lower() == "true"
    pub_id = os.getenv("ADSENSE_PUB_ID", "").strip()
    if not enabled or not pub_id or "XXXX" in pub_id:
        return "<!-- AdSense belum aktif. Isi ADSENSE_PUB_ID dan ubah ADSENSE_ENABLED=true setelah disetujui. -->"
    return (
        f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={pub_id}" '
        'crossorigin="anonymous"></script>'
    )

def ad_block(slot_name="default"):
    enabled = os.getenv("ADSENSE_ENABLED", "false").lower() == "true"
    pub_id = os.getenv("ADSENSE_PUB_ID", "").strip()
    if not enabled or not pub_id or "XXXX" in pub_id:
        return f'<div class="ad-placeholder">Area iklan: {slot_name}. Aktifkan setelah AdSense disetujui.</div>'
    return (
        '<ins class="adsbygoogle" style="display:block" '
        f'data-ad-client="{pub_id}" data-ad-slot="1234567890" '
        'data-ad-format="auto" data-full-width-responsive="true"></ins>'
        '<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>'
    )
