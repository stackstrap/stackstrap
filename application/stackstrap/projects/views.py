import os
import shutil
import StringIO
import tempfile
import zipfile

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from .models import Project, Membership

@login_required
def zip(request, project_id):
    temp_dir = tempfile.mkdtemp()

    def temp_file(*args):
        return os.path.join(temp_dir, *args)

    # make the rest of our dirs
    os.mkdir(temp_file('salt'))
    os.mkdir(temp_file('salt', 'keys'))

    # look up the project & membership
    project = get_object_or_404(Project, id=project_id)
    membership = get_object_or_404(Membership, project=project, user=request.user)

    context = {
            'user': request.user,
            'project': project,
            'membership': membership,
            }

    temp_files = [
            temp_file('Vagrantfile'),
            temp_file('salt', 'minion'),
            temp_file('salt', 'keys', 'minion.pem'),
            temp_file('salt', 'keys', 'minion.pub')
            ]

    with open(temp_files[0], 'w') as f:
        f.write(render_to_string('projects/Vagrantfile', context))

    with open(temp_files[1], 'w') as f:
        f.write(render_to_string('projects/salt.minion', context))

    with open(temp_files[2], 'w') as f:
        f.write(membership.private_key.read())

    with open(temp_files[3], 'w') as f:
        f.write(membership.public_key.read())

    # build our zip file to be returned to the user
    zs = StringIO.StringIO()
    zf = zipfile.ZipFile(zs, "w")

    for filename in temp_files:
        zf.write(filename, filename.split(temp_dir)[1])
    zf.close()

    # clean up our tempdir
    shutil.rmtree(temp_dir)

    # send our response
    resp = HttpResponse(zs.getvalue(), mimetype = "application/x-zip-compressed")
    resp['Content-Disposition'] = 'attachment; filename=StackStrap-Project-Template_%d-%s.zip' % (project.id, project.name)
    return resp
