import os
import shutil
import tempfile

from nose import with_setup

from stackstrap.template import Template

from . import setup_repositories, restore_repositories

# setup our repo & cache urls & dirs
repo_url = 'file://{0}/test_template/'.format(os.path.dirname(__file__))

@with_setup(setup_repositories, restore_repositories)
def test_template_load_save():
    # put our templates into a temporary dir that we can cleanup
    tmp_dir = tempfile.mkdtemp()
    Template.template_dir = tmp_dir

    try:
        template = Template(
            'test-template',
            repo_url,
            'master',
            'http://files.vagrantup.com/precise32.box'
        )

        # save the file
        assert not os.path.exists(os.path.join(tmp_dir, 'test-template'))
        template.save()
        assert os.path.exists(os.path.join(tmp_dir, 'test-template'))

        # re-load it
        template.ref = None
        assert template.ref is None
        template = Template.load('test-template')
        assert template.ref == 'master'
    finally:
        shutil.rmtree(tmp_dir)
