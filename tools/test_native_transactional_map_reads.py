import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADER = (ROOT / 'glue/rexglue-sdk-main/src/graphics/gta4_native/'
          'native_transactional_map.h')
FRONTEND = (ROOT / 'glue/rexglue-sdk-main/src/graphics/gta4_native/'
            'metal_frame_frontend.inc')


class NativeTransactionalMapReadsTest(unittest.TestCase):
    def test_hot_lowering_uses_non_copying_lookups(self):
        header = HEADER.read_text(encoding='utf-8')
        frontend = FRONTEND.read_text(encoding='utf-8')
        self.assertIn('const Value* Find(const Key& key)const', header)
        # A non-const find()/at() would call Touch() and copy the registry node
        # even when lowering only reads it.
        self.assertNotIn('next.surfaces.find(', frontend)
        self.assertNotIn('next.textures.find(', frontend)
        self.assertIn('next.surfaces.Read(id)', frontend)
        self.assertIn('next.surfaces.Find(it->second.surface)', frontend)
        self.assertIn('next.textures.Read(parent->generation)', frontend)
        self.assertIn('next.textures.Read(resource->generation)', frontend)


if __name__ == '__main__':
    unittest.main()
