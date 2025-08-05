#!/bin/bash
repo='jfloff/ariannacore-python'
bold="$(tput bold)"
red="$(tput setaf 1)"
green="$(tput setaf 2)"
reset="$(tput sgr0)"

build_with_status () {
  version="$1"
  tag="$2"

  printf '%sBuilding %s ... ' "$bold" "$tag"
  if ! docker build "$version" -t "$tag"; then
    printf '\n%s%sBUILD FAILED%s' "$bold" "$red" "$reset"
    exit 1
  fi

  if ! echo 'print("something")' | docker run --rm -i "$tag" &> /dev/null; then
    printf '%s%sTEST FAILED%s' "$bold" "$red" "$reset"
    exit 1
  else
    printf '%s%sSUCCESS%s' "$bold" "$green" "$reset"
  fi
  printf "\n"
}

# Move to where the script is
HERE="$( cd "$(dirname "$0")" || exit ; pwd -P )"
cd "$HERE" || exit

# Find all the top-level dirs
for version in $(find . -maxdepth 1 -not -name '.*' -type d -printf '%P\n' | sort); do
  build_with_status "$version" "$repo:$version"
done
