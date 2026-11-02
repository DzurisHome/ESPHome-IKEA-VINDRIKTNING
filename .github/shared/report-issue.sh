#!/usr/bin/env bash
# ==============================================================================
# Report Issue
# Jedno Issue na jednu vec (podľa labelu) v TOMTO repe.
#
#   report-issue.sh <label> <title> <ok|problem> [body-file]
#
# - problem + žiadne otvorené Issue  → vytvorí ho, priradí a označí REVIEWER
# - problem + Issue už je otvorené   → ak sa obsah zmenil: upraví ho a označí
#                                      REVIEWER v komentári; inak nič (žiadny spam)
# - ok      + Issue je otvorené      → zavrie ho s odkazom na úspešný beh
# - každé Issue sa zamkne → komentovať môžu iba správcovia repa, nie verejnosť
# Potrebuje: GH_TOKEN, GITHUB_REPOSITORY, GITHUB_SERVER_URL, GITHUB_RUN_ID, REVIEWER
# ==============================================================================
set -o errexit
set -o nounset
set -o pipefail

label="${1}"
title="${2}"
state="${3}"
body_file="${4:-}"
run_url="${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}"

gh label create "${label}" --repo "${GITHUB_REPOSITORY}" --color "B60205" --force > /dev/null

number="$(gh issue list \
  --repo "${GITHUB_REPOSITORY}" \
  --label "${label}" \
  --state open \
  --limit 1 \
  --json number \
  --jq '.[0].number // empty')"

if [[ "${state}" == "ok" ]]; then
  if [[ -n "${number}" ]]; then
    gh issue close "${number}" \
      --repo "${GITHUB_REPOSITORY}" \
      --comment "Resolved. Run: ${run_url}"
    echo "Issue #${number} closed."
  fi
  exit 0
fi

body="$(printf '@%s\n\n%s\n' "${REVIEWER}" "$(cat "${body_file}")")"

if [[ -z "${number}" ]]; then
  url="$(gh issue create \
    --repo "${GITHUB_REPOSITORY}" \
    --title "${title}" \
    --label "${label}" \
    --assignee "${REVIEWER}" \
    --body "${body}")"
  number="${url##*/}"
  gh api --method PUT "repos/${GITHUB_REPOSITORY}/issues/${number}/lock" -f lock_reason=resolved > /dev/null
  echo "Issue #${number} created and locked."
  exit 0
fi

current="$(gh issue view "${number}" --repo "${GITHUB_REPOSITORY}" --json body --jq '.body')"
if [[ "$(printf '%s' "${current}" | tr -d '\r')" != "$(printf '%s' "${body}" | tr -d '\r')" ]]; then
  gh issue edit "${number}" --repo "${GITHUB_REPOSITORY}" --body "${body}"
  gh issue comment "${number}" \
    --repo "${GITHUB_REPOSITORY}" \
    --body "@${REVIEWER} Updated. Run: ${run_url}"
  echo "Issue #${number} updated."
else
  echo "Issue #${number} unchanged."
fi
