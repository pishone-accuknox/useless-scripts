## Useless scripts in general. Time saver for some.

- ecr-to-docker.sh
This script will pull images from public ecr repo, retag it, push it to your private/public docker registry and delete the image.
Images should be listed in the images.txt file. Can be run in Github Actions. Please check sample workflow.

- rename-risk-factor.py
A script to rename `rick_factor` in the file that needs to be sent to the artifact API. Wrote with nessus findings in mind but should work for other findings as well.
