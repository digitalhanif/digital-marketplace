"""README animation validation without optional image dependencies."""
from pathlib import Path
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestReadmeAnimations(unittest.TestCase):
    def test_gif_files_are_valid_and_appropriately_sized(self):
        for name in ("digital-marketplace-workflow.gif", "digital-marketplace-chat-demo.gif"):
            with self.subTest(name=name):
                p = ROOT / "assets" / name
                self.assertTrue(p.is_file())
                self.assertGreater(p.stat().st_size, 50_000)
                self.assertLess(p.stat().st_size, 8_000_000)
                header = p.read_bytes()[:10]
                self.assertIn(header[:6], (b"GIF87a", b"GIF89a"))
                w, h = struct.unpack("<HH", header[6:10])
                self.assertGreaterEqual(w, 800)
                self.assertGreaterEqual(h, 400)

    def test_chat_demo_has_readable_hd_dimensions(self):
        p = ROOT / "assets" / "digital-marketplace-chat-demo.gif"
        header = p.read_bytes()[:10]
        w, h = struct.unpack("<HH", header[6:10])
        self.assertEqual((w, h), (1280, 720))


if __name__ == "__main__":
    unittest.main()
