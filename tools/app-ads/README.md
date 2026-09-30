# Unity app-ads.txt full-list validation

Copy the complete authorized sellers list from Unity Monetization → Settings → Organization → App-ads.txt → Show full list to a local source file. Record the organization and observation date with the receipt. This source is currently pending; the existing app-ads.txt has not been changed.

From the repository root:

```sh
python3 tools/app-ads/app_ads_full_list.py merge --source /absolute/path/unity-full-list.txt --target app-ads.txt --observed-date YYYY-MM-DD
python3 tools/app-ads/app_ads_full_list.py check --source /absolute/path/unity-full-list.txt --target app-ads.txt --observed-date YYYY-MM-DD
PYTHONPATH=tools/app-ads python3 -m unittest discover -s tools/app-ads
```

The merger preserves current sellers, comments and IAB variable records, adds every seller from the captured list, deduplicates rows, and writes a dated source SHA-256 header. Repeated merging is byte-identical. The validator fails for missing sellers or malformed source rows. A partial or historical source file does not prove current Unity coverage.

Public deployment and main-branch merge require the authorized release gate. This tool never deploys. Read back both public hosts after an authorized deployment; crawl acceptance is a separate observation.

Source documentation: https://docs.unity.com/en-us/monetization/dashboard/app-ads-txt/set-up-app-ads-txt and https://iabtechlab.com/ads-txt/
