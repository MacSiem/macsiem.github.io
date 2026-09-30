import unittest
from app_ads_full_list import merge, seller_rows, validate

class AppAdsTests(unittest.TestCase):
    def test_iab_owner_variable_preserved_not_counted_as_seller(self):
        old='ownerdomain=macsiem.dev\ngoogle.com,pub-123,DIRECT'
        full='unity.com,42,DIRECT'
        merged=merge(old,full,'2026-09-30')
        self.assertIn('ownerdomain=macsiem.dev',merged)
        self.assertEqual(len(seller_rows(merged)),2)
        self.assertEqual(merge(merged,full,'2026-09-30'),merged)
    def test_full_list_union_deduplicates_and_is_idempotent(self):
        old='# Existing AdMob\ngoogle.com, pub-123, DIRECT, abc\n'
        full='unity.com, 42, DIRECT\nunity.com,42,DIRECT\nexample.com, 23, RESELLER, xyz\n'
        merged=merge(old,full,'2026-09-30')
        self.assertEqual(merge(merged,full,'2026-09-30'),merged)
        self.assertEqual(len(seller_rows(merged)),3)
        self.assertEqual(validate(merged,full),[])
        self.assertIn('observed 2026-09-30',merged)
    def test_incomplete_target_fails(self):
        self.assertEqual(len(validate('unity.com,42,DIRECT','unity.com,42,DIRECT\nexample.com,23,RESELLER')),1)
    def test_empty_and_invalid_source_rejected(self):
        for text in ['# no sellers','not a seller','example.com,42,OTHER']:
            with self.assertRaises(ValueError):merge('',text,'2026-09-30')

if __name__=='__main__':unittest.main()
