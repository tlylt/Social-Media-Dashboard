This will be our reference of a typical workflow that we will adopt

Collaboration (with forking)

1. Set up remote repository on github
2. Fork repository to own github account
3. Maintain master branch as the most updated/deployable branch
4. Clone repository to local machine
5. Create new branch for feature implementation and testing.
6. Update own repo and create pull request to original remote
7. Administrator check pull request [on github]
8. Admin Merge the pull request
9. Admin delete completed branch

Collaboration (without forking)

1. Clone repo to local machine
2. Create new branch
3. Work on new branch
4. Commit changes
5. Publish branch to reflect in remote repo
6. Create and send pull request [on github]
7. Administrator check pull request [on github]
8. Admin Merge the pull request
9. Admin delete completed branch

Use git for existing folder/project

1. In the folder
   ---git init
2. Track existing files
   ---git add . (adds everything) or git add filename (adds one file)
3. Check differences/changes (if you want)
   ---git diff (for unstaged file) or git diff --staged (for staged file)
4. Updates yoru changes to your branch
   ---git commit -m "the short message about your commit"
   ---git commit -a -m "this shortcut stage all changed files and commit them"
5. Create branch
   ---git branch branchname (does not switch to that branch!)
6. Switch to correct branch
   ---git checkout branchname
7. Easy way to create branch and checkout to it
   ---git checkout -b branchname (create new branch and checkout to it)
8. Show branches
   ---git branch
9. Merging
   ---git checkout master
   ---git merge branchname
   (fastforward for no conflict easy merge)
   (recursive merge for more conflict)
   (failed with conflict notice)
10. Resolving conflicts
    master version will be injected to branch to show difference, delete the unwanted and merge again
11. Find out if branches have been merged
    ---git branch --merged
    ---git branch --no-merge
12. Delete branch
    ---git branch -d branchname (git branch -D branchname for unmerged branch)
13. Connect to remote repo
    ---git remote add origin link
    ---git push -u origin master (from master in local to remote repo [origin])
14. Stay updated with remote
    ---git pull
