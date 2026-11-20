#!/bin/sh
# Build only this local sample, outside the skill package. Does not launch it.
set -eu
package_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output_dir=${1:?Usage: build-app.sh OUTPUT_DIRECTORY}
mkdir -p "$output_dir"
output_dir=$(CDPATH= cd -- "$output_dir" && pwd)
swift build --package-path "$package_dir" --scratch-path "$output_dir/build"
binary_dir=$(swift build --package-path "$package_dir" --scratch-path "$output_dir/build" --show-bin-path)
app="$output_dir/CrateLibrary.app"
mkdir -p "$app/Contents/MacOS" "$app/Contents/Resources"
cp "$binary_dir/CrateLibrary" "$app/Contents/MacOS/CrateLibrary"
cp "$package_dir/Info.plist" "$app/Contents/Info.plist"
cp "$package_dir/LICENSE.txt" "$app/Contents/Resources/LICENSE.txt"
# Compile the asset catalog as Xcode does. Info.plist names AccentColor through
# NSAccentColorName, and AppKit reads it from Contents/Resources/Assets.car.
xcrun actool "$package_dir/Assets.xcassets" --compile "$app/Contents/Resources" \
  --platform macosx --minimum-deployment-target 14.0 --accent-color AccentColor \
  --output-partial-info-plist "$output_dir/asset-catalog-info.plist" \
  --output-format human-readable-text --errors --warnings >/dev/null
printf '%s\n' "$app"
