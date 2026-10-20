#!/bin/sh
# Build only this local sample, outside the skill package. Does not launch it.
set -eu
package_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output_dir=${1:?Usage: build-app.sh OUTPUT_DIRECTORY}
mkdir -p "$output_dir"
output_dir=$(CDPATH= cd -- "$output_dir" && pwd)
swift build --package-path "$package_dir" --scratch-path "$output_dir/build"
binary_dir=$(swift build --package-path "$package_dir" --scratch-path "$output_dir/build" --show-bin-path)
app="$output_dir/OrderCounter.app"
mkdir -p "$app/Contents/MacOS" "$app/Contents/Resources"
cp "$binary_dir/OrderCounter" "$app/Contents/MacOS/OrderCounter"
cp "$package_dir/Info.plist" "$app/Contents/Info.plist"
cp "$package_dir/LICENSE.txt" "$app/Contents/Resources/LICENSE.txt"
printf '%s\n' "$app"
