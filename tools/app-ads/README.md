# Unity app-ads.txt full-list validation

Copy the complete authorized sellers list from Unity Monetization → Settings → Organization → App-ads.txt → Show full list to a local source file. Record the organization and observation date with the receipt. Captured on 2026-09-30 from organization `maciek-sieminski-gmail-com` (7972571656487). The included `unity-full-list-20260930.txt` contains all 160 sellers; SHA-256 `aa9f182a52e93a792539f197bdd1bf4401ebb0579998f4223eeaac118985fa5e`. The new app-ads.txt contains 175 unique sellers, covers all 160 Unity entries, and preserves every one of the 168 current deployed baseline sellers (included as `deployed-baseline-20260930.txt`). Seven sellers are added, including the seventh entry absent from Unity’s six-missing preview: `sharethrough.com, UvcAx8IL, RESELLER, d53b998a7bd4ecd2`. Candidate SHA-256: `3c5e52b3ac97b98223095015d62e2c6bc88191281dfcb301b2592b2116bdad83`.

From the repository root:

```sh
python3 tools/app-ads/app_ads_full_list.py merge --source /absolute/path/unity-full-list.txt --target app-ads.txt --observed-date YYYY-MM-DD
python3 tools/app-ads/app_ads_full_list.py check --source /absolute/path/unity-full-list.txt --target app-ads.txt --observed-date YYYY-MM-DD
PYTHONPATH=tools/app-ads python3 -m unittest discover -s tools/app-ads
```

The merger preserves current sellers, comments and IAB variable records, adds every seller from the captured list, deduplicates rows, and writes a dated source SHA-256 header. Repeated merging is byte-identical. The validator fails for missing sellers or malformed source rows. A partial or historical source file does not prove current Unity coverage.

Public deployment and main-branch merge require the authorized release gate. This tool never deploys. Read back both public hosts after an authorized deployment; crawl acceptance is a separate observation.

Source documentation: https://docs.unity.com/en-us/monetization/dashboard/app-ads-txt/set-up-app-ads-txt and https://iabtechlab.com/ads-txt/
