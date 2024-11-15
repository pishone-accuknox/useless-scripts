## Useless scripts in general. Time saver for some.

- [ecr-to-docker.sh](https://github.com/pishone-accuknox/useless-scripts/blob/main/ecr-to-docker.sh): 
This script will pull images from public ecr repo, retag it, push it to your private/public docker registry and delete the image.
Images should be listed in the images.txt file. Can be run in Github Actions. Please check [sample workflow](https://github.com/pishone-accuknox/useless-scripts/blob/main/.github/workflows/docker-image-transfer.yml).

- [rename-risk-factor.py](https://github.com/pishone-accuknox/useless-scripts/blob/main/rename-risk-factor.py): 
A script to rename `rick_factor` in the file that needs to be sent to the artifact API. Wrote with nessus findings in mind but should work for other findings as well.

- [bulk_upload_secrets.sh](https://github.com/pishone-accuknox/useless-scripts/blob/main/bulk_upload_secrets.sh):
Upload all secrets to Github secrets. 
Requires:
    - `gh` to be installed and authenticated.
    - `.env` file with secrets.