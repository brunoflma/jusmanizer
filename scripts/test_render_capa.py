from pathlib import Path
import runpy
import unittest


ROOT = Path(__file__).resolve().parents[1]
validar_png = runpy.run_path(str(ROOT / "scripts" / "render-capa.py"))["validar_png"]


class RenderCapaTests(unittest.TestCase):
    def test_png_signature_guard_remains_active_when_optimized(self):
        validar_png(b"\x89PNG\r\n\x1a\nresto", "capa.png")
        for dados in (b"", b"not-a-png"):
            with self.subTest(dados=dados):
                with self.assertRaisesRegex(RuntimeError, "PNG válido"):
                    validar_png(dados, "capa.png")


if __name__ == "__main__":
    unittest.main()
