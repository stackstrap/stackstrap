import os

from stackstrap.config import settings, SettingsException

from . import StackStrapTestCase

class SettingsTestCase(StackStrapTestCase):
    def test_configure_save(self):
        tmp_dir = settings.base_dir

        self.assertFalse(os.path.exists(settings.path('settings')))
        settings.configure(tmp_dir)
        settings.save()
        self.assertTrue(os.path.exists(settings.path('settings')))

    def test_unreadable_settings_file(self):
        tmp_dir = settings.base_dir

        with open(settings.path('settings'), 'w') as f:
            f.write('---\n')

        # make it unreadable
        os.chmod(settings.path('settings'), 0000)

        self.assertRaises(IOError, lambda: settings.configure(tmp_dir))

    def test_bad_yaml_settings_file(self):
        tmp_dir = settings.base_dir

        with open(settings.path('settings'), 'w') as f:
            f.write('---\n')
            f.write('INVALID :) YAML :$ FAIL{+!}\n')

        self.assertRaises(SettingsException, lambda: settings.configure(tmp_dir))

    def test_get_set(self):
        self.assertEqual(settings.get('setting_name'), None)
        settings.set('setting_name', 'value')
        self.assertEqual(settings.get('setting_name'), 'value')
