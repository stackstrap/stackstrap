# [Changelog](https://github.com/freesurface/stackstrap/releases)

## [0.2.1](https://github.com/freesurface/stackstrap/compare/0.2.0...0.2.1)

* [e9bb5ce](https://github.com/freesurface/stackstrap/commit/e9bb5ce) Updated test to use test project repo's new location
* [3e95f51](https://github.com/freesurface/stackstrap/commit/3e95f51) Switching all paths to match new Org name
* [6b0271e](https://github.com/freesurface/stackstrap/commit/6b0271e) Improve test coverage
* [19b2368](https://github.com/freesurface/stackstrap/commit/19b2368) Remove stackstrap.yml. Fix #51
* [8842af5](https://github.com/freesurface/stackstrap/commit/8842af5) Add further installation documentation
* [9fb69a2](https://github.com/freesurface/stackstrap/commit/9fb69a2) Most vanilla systems do not have pip, switch to easy_install
* [51a25f4](https://github.com/freesurface/stackstrap/commit/51a25f4) Fixed typo [ci skip]
* [7c4db2e](https://github.com/freesurface/stackstrap/commit/7c4db2e) Updated available context variables in docs
* [00c2db1](https://github.com/freesurface/stackstrap/commit/00c2db1) Removing old salt doc content until we update with a link to other docs
* [6dfa8c7](https://github.com/freesurface/stackstrap/commit/6dfa8c7) added cleanup to docs
* [f925414](https://github.com/freesurface/stackstrap/commit/f925414) Adding complete simple workflow to README
* [379a17d](https://github.com/freesurface/stackstrap/commit/379a17d) We don't work on python 3 yet. [ci skip]
* [d71f981](https://github.com/freesurface/stackstrap/commit/d71f981) Run tests on all different python versions
* [e98609e](https://github.com/freesurface/stackstrap/commit/e98609e) Remove note about alpha software from the docs
* [25206ae](https://github.com/freesurface/stackstrap/commit/25206ae) Bumping dev status to Beta for the next release

## [0.2.0](https://github.com/freesurface/stackstrap/compare/0.1.2...0.2.0)

* [bf30011](https://github.com/freesurface/stackstrap/commit/bf30011) Format readme properly
* [c5e0b2a](https://github.com/freesurface/stackstrap/commit/c5e0b2a) Updated readme to get user's started quickly
* [e2818f5](https://github.com/freesurface/stackstrap/commit/e2818f5) Some tweaks based on coverage feedback
* [3781693](https://github.com/freesurface/stackstrap/commit/3781693) Restore coverage command to get proper metrics
* [002a9e1](https://github.com/freesurface/stackstrap/commit/002a9e1) There's something different about git on travis...
* [01ef177](https://github.com/freesurface/stackstrap/commit/01ef177) Still trying to debug travis problem
* [78afbe2](https://github.com/freesurface/stackstrap/commit/78afbe2) Turn on verbose to debug why the test failed on Travis
* [00c2183](https://github.com/freesurface/stackstrap/commit/00c2183) Lots more overhauling, Projects & Templates are now the same thing
* [1666a60](https://github.com/freesurface/stackstrap/commit/1666a60) Remove setup/teardown code for test repos
* [b93d748](https://github.com/freesurface/stackstrap/commit/b93d748) Removing test repos, moving to github
* [2889fd8](https://github.com/freesurface/stackstrap/commit/2889fd8) Fix a subtle bug: Ensure each CommandLoader gets it's own commands dict
* [0dc71ae](https://github.com/freesurface/stackstrap/commit/0dc71ae) Updated the template list function to work with the updated structure
* [78de4ad](https://github.com/freesurface/stackstrap/commit/78de4ad) Initial 'template create' implementation
* [df6e462](https://github.com/freesurface/stackstrap/commit/df6e462) Removing project_template, moved to it's own repo
* [ed62fc9](https://github.com/freesurface/stackstrap/commit/ed62fc9) Remove the extra template steps from project creation
* [74f8c12](https://github.com/freesurface/stackstrap/commit/74f8c12) Rename template.create to .setup
* [a7c2744](https://github.com/freesurface/stackstrap/commit/a7c2744) Complete of rejig
* [5c1e267](https://github.com/freesurface/stackstrap/commit/5c1e267) Restore Vagrantfile, it will be needed for the 'template create' command
* [41a80d8](https://github.com/freesurface/stackstrap/commit/41a80d8) Hand off for Evan to complete
* [7a7f60b](https://github.com/freesurface/stackstrap/commit/7a7f60b) Updating test template to match new strategy
* [ba5ccd5](https://github.com/freesurface/stackstrap/commit/ba5ccd5) forgot to import errno
* [5c7ca09](https://github.com/freesurface/stackstrap/commit/5c7ca09) cleaned mkdir function to have a better exception
* [1b597ac](https://github.com/freesurface/stackstrap/commit/1b597ac) Fixed issue where error occured because of merging salt folders in project
* [75c3975](https://github.com/freesurface/stackstrap/commit/75c3975) Implemented the ref option in the process of cloning a template
* [f1e0dae](https://github.com/freesurface/stackstrap/commit/f1e0dae) updating more file paths to match new template structure
* [53f9ce7](https://github.com/freesurface/stackstrap/commit/53f9ce7) Upated files to reflect the new path the the meta data file
* [a5eb8b0](https://github.com/freesurface/stackstrap/commit/a5eb8b0) Updated template docs to reflect changes to templates
* [f518af1](https://github.com/freesurface/stackstrap/commit/f518af1) Use better casing for representation of other projects in docs
* [7039bbc](https://github.com/freesurface/stackstrap/commit/7039bbc) adding jinja link
* [f813ecc](https://github.com/freesurface/stackstrap/commit/f813ecc) Adding a link to overview as well
* [dd4ca70](https://github.com/freesurface/stackstrap/commit/dd4ca70) updated the overview in the documention to reflect the project more

## [0.1.2](https://github.com/freesurface/stackstrap/compare/0.1.1...0.1.2)

* [4425781](https://github.com/freesurface/stackstrap/commit/4425781) updated copyright
* [beaa675](https://github.com/freesurface/stackstrap/commit/beaa675) moving repo once again

## [0.1.1](https://github.com/freesurface/stackstrap/compare/0.1.0...0.1.1)

* [45536bb](https://github.com/freesurface/stackstrap/commit/45536bb) Added commands folder to MANIFEST
* [719543e](https://github.com/freesurface/stackstrap/commit/719543e) adding a requirements.txt file for development
* [42d9c5e](https://github.com/freesurface/stackstrap/commit/42d9c5e) Adding changelog for better release information

## [0.1.0](https://github.com/freesurface/stackstrap/compare/0.1.0...0.1.0)


