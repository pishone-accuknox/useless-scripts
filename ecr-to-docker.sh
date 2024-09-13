#!/bin/bash

PRIVATE_REGISTRY_USERNAME=$PRIVATE_REGISTRY_USERNAME
PRIVATE_REGISTRY_PASSWORD=$PRIVATE_REGISTRY_PASSWORD

tmp_file=$(mktemp)

cp images.txt $tmp_file

sed -i "s#<airgapped_reg>#$1#g" $tmp_file

total_images=$(wc -l < "$tmp_file")
echo "Total number of images to process: $total_images"

pushed_count=0

while IFS= read -r line; do
  pub_img=$(echo "$line" | awk '{print $1}')
  priv_img=$(echo "$line" | awk '{print $2}')

  echo "Pulling public image: $pub_img"
  docker pull $pub_img

  echo "Tagging image: $pub_img as $priv_img"
  docker tag $pub_img $priv_img

  echo "Pushing private image: $priv_img"
  docker push $priv_img

  pushed_count=$((pushed_count + 1))
  pending_count=$((total_images - pushed_count))

  echo "Pushed $pushed_count out of $total_images images. Pending: $pending_count"

done < "$tmp_file"

rm $tmp_file

REGISTRY_SCAN_TAG="v0.1.1"

echo "Pulling Helm chart..."
helm pull oci://public.ecr.aws/ssgseewfweg/registry-scan --version $REGISTRY_SCAN_TAG

echo "Pushing Helm chart to private registry..."
helm push registry-scan-$REGISTRY_SCAN_TAG.tgz oci://$1

echo "Script completed successfully."
