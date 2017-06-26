# clone, easyhtmlparser, ehp.
cd ~/projects
git clone git@github.com:iogf/ehp.git ehp-code
##############################################################################
# push, easyhtmlparser, ehp.
cd ~/projects/ehp-code
git status
git add *
git commit 
git push 
##############################################################################
# create, development, branch, ehp.
cd /home/tau/projects/ehp-code
git branch -a
git checkout -b development
git push --set-upstream origin development
##############################################################################
# checkout, undo, easyhtmlparser, ehp.
cd ~/projects/ehp-code
git checkout *
##############################################################################
# install, easyhtmlparser, ehp.
cd ~/projects/ehp-code
sudo bash -i
python2 setup.py install
rm -fr build
exit
##############################################################################
# ehp, pip.
cd ~/projects/ehp-code

echo '
[metadata]
description-file = README.md
' > setup.cfg

vy setup.cfg
python setup.py sdist register upload
rm -fr sdist
##############################################################################
# merge development into master.
cd /home/tau/projects/ehp-code/
git checkout master
git merge development
git push
git checkout development

