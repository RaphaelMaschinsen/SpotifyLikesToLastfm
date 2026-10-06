import unittest

from title_cleaner import clean_title


class CleanTitleTest(unittest.TestCase):
    def test_strips_remaster_markers(self):
        cases = {
            "Changes - 2013 Remaster": "Changes",
            "Here Comes The Sun - Remastered 2009": "Here Comes The Sun",
            "Paranoid (2012 Remaster)": "Paranoid",
            "Hand of Doom - 2012 - Remaster": "Hand of Doom",
            "Song [Remastered]": "Song",
            "Song - 2019 Digital Remaster": "Song",
            "Canción - Remasterizado 2007": "Canción",
        }
        for raw, clean in cases.items():
            with self.subTest(raw=raw):
                # Act & Assert
                self.assertEqual(clean_title(raw), clean)

    def test_strips_edition_and_bonus_markers(self):
        cases = {
            "Song (Deluxe Edition)": "Song",
            "Song (30th Anniversary Super Deluxe)": "Song",
            "Song - Bonus Track": "Song",
            "Song (Explicit)": "Song",
        }
        for raw, clean in cases.items():
            with self.subTest(raw=raw):
                # Act & Assert
                self.assertEqual(clean_title(raw), clean)

    def test_strips_stacked_markers(self):
        # Act & Assert
        self.assertEqual(clean_title("Song (Deluxe Edition) - 2011 Remaster"), "Song")

    def test_keeps_mix_word_from_combined_marker(self):
        # Act & Assert
        self.assertEqual(clean_title("Song (Mono Remastered)"), "Song - Mono")

    def test_leaves_real_title_content_alone(self):
        for title in [
            "Song (Live in Rotterdam 1984)",
            "Song - Live",
            "Song (Taylor's Version)",
            "Song, Pt. II",
            "Time of the Season - Mono Version",
            "Song - Radio Edit",
            "Master of Puppets",
            "Deluxe",
            "The Beatles 1967 - 1970",
            "2012",
        ]:
            with self.subTest(title=title):
                # Act & Assert
                self.assertEqual(clean_title(title), title)


if __name__ == "__main__":
    unittest.main()
