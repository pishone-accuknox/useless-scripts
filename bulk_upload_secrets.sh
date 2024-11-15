while IFS= read -r line; do
    IFS="=" read -r key value <<< "$line"
    gh secret set "$key" --body "$value" --env ENVIRONMENT_NAME
done < .env
