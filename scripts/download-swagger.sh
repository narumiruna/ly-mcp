#!/usr/bin/env bash
set -euo pipefail

readonly swagger_url="https://ly.govapi.tw/v2/swagger.yaml"
readonly repository_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
readonly output_path="${1:-${repository_root}/swagger.yaml}"
readonly temporary_file="$(mktemp "${output_path}.tmp.XXXXXX")"

trap 'rm -f -- "${temporary_file}"' EXIT

curl --fail --location --silent --show-error \
    --output "${temporary_file}" \
    "${swagger_url}"

if [[ ! -s "${temporary_file}" ]]; then
    printf 'Downloaded file is empty: %s\n' "${swagger_url}" >&2
    exit 1
fi

mv -- "${temporary_file}" "${output_path}"
trap - EXIT

printf 'Downloaded %s to %s\n' "${swagger_url}" "${output_path}"
