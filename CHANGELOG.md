# Changelog

This file includes a history of past releases. Changes that were not yet added to a release are in the [changelog.d/](./changelog.d) folder.

<!--
⚠️ DO NOT ADD YOUR CHANGES TO THIS FILE! (unless you want to modify existing changelog entries in this file)
Changelog entries are managed by scriv. After you have made some changes to this plugin, create a changelog entry with:

    scriv create

Edit and commit the newly-created file in changelog.d.

If you need to create a new release, create a separate commit just for that. It is important to respect these
instructions, because git commits are used to generate release notes:
  - Modify the version number in `__about__.py`.
  - Collect changelog entries with `scriv collect`
  - The title of the commit should be the same as the new version: "vX.Y.Z".
-->

<!-- scriv-insert-here -->

<a id='changelog-18.0.1'></a>
## v18.0.1 (2024-12-12)

- [Bugfix] Fix legacy warnings during Docker build. (by @regisb)
- [Bugfix] Fix ecommerce image build, which was failing because of a missing pkg-config apt package. (by @regisb)
- 💥 [Deprecation] Drop support for python 3.8 and set Python 3.9 as the minimum supported python version. (by @Faraz32123)
- 💥[Improvement] Rename Tutor's two branches (by @DawoudSheraz):
  * Rename **master** to **release**, as this branch runs the latest official Open edX release tag.
  * Rename **nightly** to **main**, as this branch runs the Open edX master branches, which are the basis for the next Open edX release.

<a id='changelog-18.0.0'></a>
## v18.0.0 (2024-05-15)

- 💥[Feature] Upgrade to Redwood. (by @Faraz32123)
- [Feature] Add support to `atlas pull` - FC-0012 project, OEP-58. (by @shadinaif)
- [Improvement] Change ecommerce and ecommerce-worker remotes from `edx` to `openedx`. (by @christopappas)
- 💥[Feature] Upgrade Python version to 3.12.2. (by @Faraz32123)
- [BugFix] Fix wrong mime type by adding mime-support dependency. (by @Faraz32123)

<a id='changelog-17.0.2'></a>
## v17.0.2 (2024-04-09)

- [Feature] Make it possible to use mounts for a local development. (by @cmltawt0)

- [bugFix] Change the ecommerce MFEs remotes from `edx` to `openedx`. (by @christopappas)

<a id='changelog-17.0.1'></a>
## v17.0.1 (2024-03-01)

- [Improvement] Added flex_run_environment setting variable for cybersource payment. Updated docs for it as well. (by @Danyal-Faheem)

- [Bugfix] Make plugin compatible with Python 3.12 by removing dependency on `pkg_resources`. (by @regisb)

- [Bugfix] Add forward slash at the end of payment page url. Payment page appears to be blank without forward slash in production. (by @Faraz32123)

<a id='changelog-17.0.0'></a>
## v17.0.0 (2023-12-09)

- 💥 [Feature] Upgrade to Quince. (by @ziafazal)

<a id='changelog-16.0.4'></a>
## v16.0.4 (2023-12-11)

- [Bugfix] Fix 500 internal server error due to lms_user_id not found on accessing the ecommerce admin panel. (by @Faraz32123)

<a id='changelog-16.0.3'></a>
## v16.0.3 (2023-12-11)

- [Bugfix] Fix error during init task: "'tuple object' has no attribute 'name'". (by @regisb)

<a id='changelog-16.0.2'></a>
## v16.0.2 (2023-12-09)

[Bugfix] Mounted settings in kubernetes. (by @hoffmannkrzysztof)

<a id='changelog-16.0.1'></a>
## v16.0.1 (2023-12-08)

- [Improvement] Add a changelog file to this plugin. (by @regisb)
- [Feature] Improve support of auto-mounted ecommerce repository. (by @regisb)
- [Improvement] Added Typing to code, Makefile and test action to the repository and formatted code with Black and isort. (by @CodeWithEmad)
- [Feature] Add patch ecommerce-dockerfile-pre-assets. (by @igobranco)
- [Bugfix] Switch ecommerce MFE port from 1996 to 7296, as it clashes with the new learner dashboard. (by @regisb)
