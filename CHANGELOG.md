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
