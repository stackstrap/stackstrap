import os
import tempfile
import shutil
import StringIO
import tempfile
import zipfile

class ZipCreator(object):
    """
    ZipCreator is a object meant to be used via the `with` keyword to make the
    creation of a zipfile using a temporary directory easy.

    You can use the `mkdir` & `join` functions to make directories & construct
    filesystem paths based on the new temporary directory without ever having
    to actually manage the directory.

    There's a stub in place so that you can call `z.path.join` so that the
    method is more familiar looking when reading your code.

    When you're ready to get your zip file contents, to return in a HTTP
    response or write to a file, just call the mkzip method.

    Example::
        with ZipCreator() as z:
            z.mkdir('somedir')
            with open(z.path.join('somedir', 'file.txt')) as f:
                f.write("This is a file that will end up in my zip")

            # now you can write the contents of z.mkzip to a file or return it
            # as a HttpResponse or similar...
    """

    def __init__(self):
        class PathStub(object):
            "stub you can use the familiar z.path.join idiom"
            join = self.join
        self.path = PathStub()

    def join(self, *args):
        "stub to make generating file names relative to our temp dir easier"
        return os.path.join(self.temp_dir, *args)

    def mkdir(self, *args):
        "stub to make directories relative to our temp dir"
        return os.mkdir(self.join(*args))

    def mkzip(self):
        temp_dir_len = len(self.temp_dir) + 1

        # build our zip file to be returned to the user
        zip_io = StringIO.StringIO()
        zip_file = zipfile.ZipFile(zip_io, "w")

        # recursively add our files
        for base, dirs, files in os.walk(self.temp_dir):
            for f in files:
                # build the full name
                zip_name = os.path.join(base, f)

                # write the file relative to the top of the temp dir
                zip_file.write(zip_name, zip_name[temp_dir_len:])

        zip_file.close()

        return zip_io.getvalue()

    def __enter__(self):
        # get our temp dir
        self.temp_dir = tempfile.mkdtemp()
        return self

    def __exit__(self, type, value, tb):
        # clean up our tempdir
        shutil.rmtree(self.temp_dir)
