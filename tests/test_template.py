import os
import shutil
import tempfile

from stackstrap.cli import StackStrapCLI
from stackstrap.commands import CommandError
from stackstrap.config import settings
from stackstrap.template import Template, TemplateExists, \
                                TemplateRepoException, TemplateMetaException

from . import StackStrapTestCase


# setup our repo & cache urls & dirs
repo_url = 'file://{0}/test_template/'.format(os.path.dirname(__file__))
bad_repo_url = 'file://{0}/test_template_bad/'.format(os.path.dirname(__file__))
missing_repo_url = 'file://{0}/test_template_missing/'.format(os.path.dirname(__file__))


def make_template(template_url=repo_url, ref='master'):
    template = Template('test-template')
    template.setup(template_url, ref)
    return template


class TemplateTestCase(StackStrapTestCase):
    def test_template_validate(self):
        template = make_template()
        template.validate()
        assert template.meta['template_name'] == 'Test Template'
        assert template.meta['template_description'] == 'Testing'
        assert template.meta['file_templates'] == ['README']
        assert template.meta['path_templates'] == [{'README': 'README.transformed'}]


    def test_template_validate_fail_bad_meta(self):
        self.assertRaises(TemplateMetaException, make_template, bad_repo_url)

    def test_template_validate_fail_bad_repo(self):
        self.assertRaises(TemplateRepoException, make_template, missing_repo_url)

    def test_template_create_exists(self):
        make_template()
        self.assertRaises(TemplateExists, make_template)

    def test_template_delete(self):
        template = make_template()
        self.assertTrue(os.path.exists(template.path))
        template.delete()
        self.assertFalse(os.path.exists(template.path))


    def test_template_available(self):
        make_template()
        self.assertEqual(Template.available(), ['test-template'])


    def test_template_cli(self):
        cli = StackStrapCLI()

        self.assertFalse(os.path.exists(settings.path('templates', 'test-template')))

        cli.main(['template', 'add', 'test-template', repo_url])
        self.assertTrue(os.path.exists(settings.path('templates', 'test-template')))

        cli.main(['template', 'remove', 'test-template'])
        self.assertFalse(os.path.exists(settings.path('templates', 'test-template')))

        # call this a second time and it should error because the template
        # doesn't exist
        self.assertRaises((CommandError, SystemExit),
                          lambda: cli.main(['template', 'remove', 'test-template']))
