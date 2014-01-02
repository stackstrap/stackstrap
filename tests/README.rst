StackStrap testing notes
========================

We need two git repositories as part of our tests, but since we can't have a
git repo in a git repo we have renamed the .git directories to _git so they
will be tracked in our main repo.

The tests will automatically move the _git dir back to .git so that the tests
work and then set it back to _git when it's done. If you need to manually make
changes to the test repositories you'll need to manually move the _git dir to
.git, make your changes and move it back.
