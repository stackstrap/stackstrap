import os
import shutil
import tempfile

from stackstrap.template import Template, TemplateRepoException, TemplateMetaException

from . import StackStrapTestCase


# setup our repo & cache urls & dirs
repo_url = 'file://{0}/test_template/'.format(os.path.dirname(__file__))
bad_repo_url = 'file://{0}/test_template_bad/'.format(os.path.dirname(__file__))
missing_repo_url = 'file://{0}/test_template_missing/'.format(os.path.dirname(__file__))


def make_template(template_url=repo_url):
    return Template(
        'test-template',
        template_url,
        'master',
        'http://files.vagrantup.com/precise32.box'
    )


class TemplateTestCase(StackStrapTestCase):
    def test_template_load_save(self):
        template = make_template()

        # save the file
        self.assertFalse(os.path.exists(template.template_file))
        template.save()
        self.assertTrue(os.path.exists(template.template_file))

        # make sure the file is what we're expecting
        expected = "{box: 'http://files.vagrantup.com/precise32.box', box_name: precise32, name: test-template,\n  nopull: false, ref: master, url: '%s'}\n" % repo_url
        self.assertEqual(expected, open(template.template_file).read())

        # re-load it
        template.ref = None
        self.assertIsNone(template.ref)
        template = Template.load('test-template')
        self.assertEqual(template.ref, 'master')


    def test_template_validate(self):
        template = make_template()
        template.validate()
        assert template.meta['template_name'] == 'Test Template'
        assert template.meta['template_description'] == 'Testing'
        assert template.meta['file_templates'] == ['README']
        assert template.meta['path_templates'] == [{'README': 'README.transformed'}]


    def test_template_validate_fail_bad_meta(self):
        template = make_template(bad_repo_url)
        self.assertRaises(TemplateMetaException, template.validate)


    def test_template_validate_fail_bad_repo(self):
        template = make_template(missing_repo_url)
        self.assertRaises(TemplateRepoException, template.validate)
