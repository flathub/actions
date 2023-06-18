# Flathub actions

These actions are run to streamline certain tasks related to Flathub.

## Running the external data checker

The folder `flathub-external-data-checker` holds the code that runs the external data checker. It is run by the GitHub action `external-data-checker.yml` found [here](https://github.com/flathub/flathub/blob/master/.github/workflows/external-data-checker.yml) which is triggered by on a schedule.

## The merge command

The folder `merge` holds the code used for the `/merge` command used in the [flathub/flathub](https://github.com/flathub/flathub) repository. It is run by the GitHub action `merge.yml` found [here](https://github.com/flathub/flathub/blob/master/.github/workflows/merge.yml) which is triggered by a comment on a pull request.
