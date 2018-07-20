# Contribution guidelines

First of all, thanks for thinking of contributing to this project. :smile:

Before sending a Pull Request, please make sure that you're assigned the task on a GitHub issue.

- If a relevant issue already exists, discuss on the issue and get it assigned to yourself on GitHub.
- If no relevant issue exists, open a new issue and get it assigned to yourself on GitHub.

Please proceed with a Pull Request only after you're assigned. It'd be a waste of your time as well as ours if you have not contacted us before hand when working on some feature / issue. You can contact us on the slack group: https://girlscriptgssoc.slack.com/messages/CB4V6N62H/details/ or on relevant issues itself. We welcome any contribution that could enhance app's functionality. Kindly follow the simple steps below to submit a Pull Request.

# Development

1) Fork this repo and clone the forked repo locally.
2) Install with

    ```sh
    git clone https://github.com/kaustubhhiware/facebook-archive.git
    cd facebook-archive
    git remote set-url upstream https://github.com/kaustubhhiware/facebook-archive.git
    git remote set-url origin https://github.com/[your_username]/facebook-archive.git
    sudo chmod a+x run.sh # only for the first time
    ```

3) Make a seperate branch with a descriptive name (that could explain the purpose of the PR) such as `awesome_feature` and switch to it by running `git checkout -b your_branch(here, awesome_feature)` in the terminal.

4) Add/Modify the code and do `git add files_involved` to add your changes.

5) Commit your changes using `git commit -am "your_message"`. Please refer to [commit message guidelines](https://chris.beams.io/posts/git-commit/) to write better commit messages. It will help in an easier review process.

6) Do `git pull upstream master` to sync with this repo.

7) Do `git push origin your_branch(here, awesome_feature)` to push code into your branch.

8) Finally, create a PR by clicking on the `New pull request` button [here](https://github.com/kaustubhhiware/facebook-archive/pulls). Make sure your PR is compliant with the following checklist.

# PR Checklist

- [ ] When making a PR, add images / plots in the repository.
- [ ] Make sure to add appropriate documentation wherever required; including a brief explanation of the script in comments, adding docstrings in functions, and using intuitive variable names. Refer [#16](https://github.com/kaustubhhiware/facebook-archive/issues/16) for details.
- [ ] Link these images in the README in the Features section.
- [ ] Post all the images of your script `abc.py` in `images/abc`.
- [ ] If you have some things to work upon in the PR, please add `in-progress` label. Remove this label when you're ready for a review.
- [ ] Don't try to push many commits, make a new commit only when there is some good amount of change from the last commit. To add your changes to the previous commit you can use git commit --amend or you can squash several commits into one. Also try to write descriptive commit messages, so that if someone looks in the logs he can understand what work was done in that commit. All this makes the repository logs clean and understandable, which is helpful when the project grows. You can refer to this: https://chris.beams.io/posts/git-commit/ (copied from @techytushar (M)'s reply to one PR)
- [ ] Add an anonymous version of the file you're using, so that a user can try out the script without actually downloading the data. Place this json file in the `examples` folder, as it would appear in your extracted archive. This file can be a subset of your own file, anonymised.
- [ ]  Update requirements.txt, if needed.
- [ ] _optional_ Try to make insights from your plots. If approved, add these in the observations section of the README.


# ToDos

These are the things to note, irrespective of what issue you are working on.

- [ ] Pick larger intervals to plot for clearer graphs, less shaky.
- [ ] Make sure the scripts are compatible with the latest version of JSON data provided by facebook's archive - [#2](https://github.com/kaustubhhiware/facebook-archive/issues/2).