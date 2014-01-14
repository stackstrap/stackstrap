import os
import shutil
import tempfile

from stackstrap.cli import StackStrapCLI
from stackstrap.commands import CommandError
from stackstrap.config import settings
from stackstrap.template import Template, TemplateExists, \
                                TemplateRepoException, TemplateMetaException

from . import StackStrapTestCase


# setup repos & branches
repo_url = 'https://github.com/openops/stackstrap-test-template.git'
missing_repo_url = 'https://fail:fail@github.com/openops/stackstrap-non-existant-template.git'
bad_repo_url = 'FAIL:FAIL/F/A/I/L'
bad_meta_branch = 'bad-meta-for-tests'
missing_meta_branch = 'missing-meta-for-tests'

def make_template(template_url=repo_url, ref='master'):
    template = Template('test-template')
    template.setup(template_url, ref)
    return template


class TemplateTestCase(StackStrapTestCase):
    def test_creating_templates(self):
        orig_dir = os.getcwd()
        tmp_dir = tempfile.mkdtemp()
        os.chdir(tmp_dir)

        cli = StackStrapCLI()
        master = Template('master-template')

        self.assertFalse(os.path.exists('./testing'))
        self.assertFalse(master.exists)
        cli.main(['template', 'create', 'testing'])
        self.assertTrue(os.path.exists('./testing'))
        self.assertTrue(os.path.exists('testing/Vagrantfile'))
        self.assertTrue(master.exists)

    def test_validating_templates(self):
        template = make_template()
        self.assertEqual(template.meta['template_name'], 'Your template')
        self.assertEqual(template.meta['template_description'], 'Add your description here.')
        self.assertEqual(template.meta['cleanup'], ['README.rst'])
        self.assertEqual(template.meta['file_templates'], ['Vagrantfile', 'salt/pillar/stackstrap.sls'])
        self.assertEqual(template.meta['path_templates'], [{'PROJECT-README': 'README'}])

    def test_should_fail_on_bad_meta(self):
        self.assertRaises(TemplateMetaException, make_template, repo_url, bad_meta_branch)

    def test_should_fail_on_missing_meta(self):
        self.assertRaises(TemplateMetaException, make_template, repo_url, missing_meta_branch)

    def test_should_fail_on_missing_repo(self):
        self.assertRaises(TemplateRepoException, make_template, missing_repo_url)

    def test_should_fail_on_bad_repo(self):
        self.assertRaises(TemplateRepoException, make_template, bad_repo_url)

    def test_creating_a_template_twice_should_fail(self):
        make_template()
        self.assertRaises(TemplateExists, make_template)

    def test_deleting_a_template(self):
        template = make_template()
        self.assertTrue(os.path.exists(template.path))
        template.delete()
        self.assertFalse(os.path.exists(template.path))


    def test_available(self):
        self.assertEqual(Template.available(), [])
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
