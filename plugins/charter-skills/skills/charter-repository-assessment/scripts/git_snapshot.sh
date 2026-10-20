#!/usr/bin/env bash

set -u
set -o pipefail
export GIT_OPTIONAL_LOCKS=0

usage() {
  cat <<'EOF'
Usage: git_snapshot.sh [--repo PATH] [--compare REF]...

Print a read-only snapshot of local Git metadata. The command never fetches and
does not prove that locally recorded remote-tracking refs match the server.

For each pair of --compare refs it reports what each side changed since their
merge base and whether one side's changes are already present in the other,
so a branch integrated by squash, rebase or cherry-pick reads as integrated
rather than diverged. Evidence, strongest first: every commit has an equal
patch on the other side; one commit there carries the branch's whole change;
the change still reverse-applies to the other side's tree. A squash with
hand-resolved conflicts can read as diverged, and one the target later
reverted still reads as integrated.
EOF
}

tmp_root=""
cleanup() {
  if [[ -n "$tmp_root" ]]; then
    rm -rf "$tmp_root"
  fi
}
trap cleanup EXIT

# Count "+" lines (commits without a patch-equivalent) in `git cherry` output.
cherry_summary() {
  local lines="$1" total=0 plus=0
  if [[ -n "$lines" ]]; then
    total="$(printf '%s\n' "$lines" | wc -l | tr -d ' ')"
    plus="$(printf '%s\n' "$lines" | grep -c '^+' || true)"
  fi
  printf '%s of %s' "$plus" "$total"
}

# Diff options that keep patch text independent of user configuration.
diff_opts=(--no-color --no-ext-diff --no-textconv --no-renames --no-relative
  --src-prefix=a/ --dst-prefix=b/)

# Print whether SOURCE's changes since BASE are already contained in TARGET:
#   no_net_change             SOURCE changed nothing since BASE
#   patch_equivalent_commits  every SOURCE commit has an equal patch in TARGET
#                             (rebase or cherry-pick)
#   squash_commit <oid>       one TARGET commit carries SOURCE's whole change
#   changes_present           SOURCE's change reverse-applies to TARGET's tree
#   not_present | unknown
# CHERRY is `git cherry TARGET SOURCE` output. Only objects are read; the
# scratch index for the reverse-apply check lives under $tmp_root.
changes_present_in() {
  local target="$1" source="$2" base="$3" cherry="$4" work source_id squash
  if git -C "$root" diff --quiet --no-ext-diff "$base" "$source" --; then
    printf '%s' 'no_net_change'
    return
  fi
  if [[ -n "$cherry" && $'\n'"$cherry" != *$'\n+'* ]]; then
    printf '%s' 'patch_equivalent_commits'
    return
  fi
  source_id="$(git -C "$root" diff "${diff_opts[@]}" "$base" "$source" -- 2>/dev/null |
    git -C "$root" patch-id --stable 2>/dev/null | cut -d ' ' -f 1)"
  if [[ -n "$source_id" ]]; then
    squash="$(git -C "$root" log -p "${diff_opts[@]}" --format='commit %H' "$base..$target" -- 2>/dev/null |
      git -C "$root" patch-id --stable 2>/dev/null |
      awk -v id="$source_id" '$1 == id && !found { print $2; found = 1 }')"
    if [[ -n "$squash" ]]; then
      printf 'squash_commit %s' "$squash"
      return
    fi
  fi
  if [[ -z "$tmp_root" ]] || ! work="$(mktemp -d "$tmp_root/pair.XXXXXX")"; then
    printf '%s' 'unknown'
    return
  fi
  if ! git -C "$root" diff --binary "${diff_opts[@]}" "$base" "$source" -- >"$work/patch" 2>/dev/null ||
    ! GIT_INDEX_FILE="$work/index" git -C "$root" read-tree "$target" 2>/dev/null; then
    printf '%s' 'unknown'
    return
  fi
  if GIT_INDEX_FILE="$work/index" git -C "$root" apply --cached --check --reverse -C1 \
    --whitespace=nowarn "$work/patch" >/dev/null 2>&1; then
    printf '%s' 'changes_present'
  else
    printf '%s' 'not_present'
  fi
}

repo="."
compare_refs=()

while (($#)); do
  case "$1" in
    --repo)
      if (($# < 2)); then
        printf '%s\n' 'error: --repo requires a path' >&2
        exit 2
      fi
      repo="$2"
      shift 2
      ;;
    --compare)
      if (($# < 2)); then
        printf '%s\n' 'error: --compare requires a ref' >&2
        exit 2
      fi
      compare_refs+=("$2")
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'error: unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if ! root="$(git -C "$repo" rev-parse --show-toplevel 2>/dev/null)"; then
  printf 'error: not a Git worktree: %s\n' "$repo" >&2
  exit 1
fi

branch="$(git -C "$root" symbolic-ref --quiet --short HEAD 2>/dev/null || printf '%s' '(detached)')"
head_oid="$(git -C "$root" rev-parse HEAD)"
upstream="$(git -C "$root" rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"

printf '%s\n' '--- snapshot_scope ---'
printf 'observed_at_utc=%s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
printf 'scope=%s\n' 'local_git_metadata_only'
printf 'network_refresh=%s\n' 'not_performed'
printf 'server_ref_currentness=%s\n' 'unproven'

printf '%s\n' '--- identity ---'
printf 'root=%s\n' "$root"
printf 'branch=%s\n' "$branch"
printf 'head=%s\n' "$head_oid"
printf 'upstream=%s\n' "${upstream:-(none)}"
if [[ -n "$upstream" ]]; then
  divergence="$(git -C "$root" rev-list --left-right --count "HEAD...$upstream" 2>/dev/null || true)"
  printf 'head_vs_upstream_left_right=%s\n' "${divergence:-(unavailable)}"
fi

printf '%s\n' '--- status_porcelain_v2 ---'
git -C "$root" status --porcelain=v2 --branch --untracked-files=all

printf '%s\n' '--- worktrees ---'
git -C "$root" worktree list --porcelain

printf '%s\n' '--- remotes ---'
git -C "$root" remote --verbose

printf '%s\n' '--- local_branches ---'
git -C "$root" branch --verbose --verbose --no-abbrev

printf '%s\n' '--- local_and_remote_tracking_refs ---'
git -C "$root" for-each-ref \
  --sort=refname \
  --format='%(refname)%09%(objectname)%09%(upstream:short)%09%(upstream:track)%09%(committerdate:iso8601-strict)%09%(subject)' \
  refs/heads refs/remotes

if [[ -f "$root/.gitmodules" ]]; then
  printf '%s\n' '--- submodules ---'
  git -C "$root" submodule status --recursive || true
fi

if ((${#compare_refs[@]})); then
  printf '%s\n' '--- requested_refs ---'
  valid_refs=()
  for ref in "${compare_refs[@]}"; do
    if oid="$(git -C "$root" rev-parse --verify "${ref}^{commit}" 2>/dev/null)"; then
      valid_refs+=("$ref")
      git -C "$root" show -s \
        --format="ref=$ref%noid=%H%ncommitted_at=%cI%nsubject=%s" \
        "$oid"
    else
      printf 'ref=%s\nstatus=unresolved\n' "$ref"
    fi
  done

  if ((${#valid_refs[@]} >= 2)); then
    printf '%s\n' '--- pairwise_topology ---'
    tmp_root="$(mktemp -d "${TMPDIR:-/tmp}/git_snapshot.XXXXXX" 2>/dev/null || true)"
    for ((i = 0; i < ${#valid_refs[@]}; i++)); do
      for ((j = i + 1; j < ${#valid_refs[@]}; j++)); do
        a="${valid_refs[$i]}"
        b="${valid_refs[$j]}"
        counts="$(git -C "$root" rev-list --left-right --count "$a...$b")"
        merge_base="$(git -C "$root" merge-base "$a" "$b" 2>/dev/null || true)"
        printf 'a=%s\nb=%s\nleft_right_unique=%s\nmerge_base=%s\n' \
          "$a" "$b" "$counts" "${merge_base:-(none)}"
        if [[ -z "$merge_base" ]]; then
          printf 'relation=%s\n\n' 'unrelated_histories'
          continue
        fi
        a_delta="$(git -C "$root" diff --shortstat --no-ext-diff "$merge_base" "$a" -- 2>/dev/null || true)"
        b_delta="$(git -C "$root" diff --shortstat --no-ext-diff "$merge_base" "$b" -- 2>/dev/null || true)"
        printf 'a_since_merge_base=%s\nb_since_merge_base=%s\n' \
          "${a_delta:-(no file delta)}" "${b_delta:-(no file delta)}"
        if [[ "$(git -C "$root" rev-parse "$a^{commit}")" == "$(git -C "$root" rev-parse "$b^{commit}")" ]]; then
          relation="same_commit"
        elif git -C "$root" merge-base --is-ancestor "$a" "$b"; then
          relation="a_is_ancestor_of_b"
        elif git -C "$root" merge-base --is-ancestor "$b" "$a"; then
          relation="b_is_ancestor_of_a"
        else
          b_cherry="$(git -C "$root" cherry "$a" "$b" 2>/dev/null || true)"
          a_cherry="$(git -C "$root" cherry "$b" "$a" 2>/dev/null || true)"
          b_in_a="$(changes_present_in "$a" "$b" "$merge_base" "$b_cherry")"
          a_in_b="$(changes_present_in "$b" "$a" "$merge_base" "$a_cherry")"
          printf 'b_commits_without_patch_equivalent_in_a=%s\n' "$(cherry_summary "$b_cherry")"
          printf 'a_commits_without_patch_equivalent_in_b=%s\n' "$(cherry_summary "$a_cherry")"
          printf 'b_changes_in_a=%s\na_changes_in_b=%s\n' "$b_in_a" "$a_in_b"
          case "$b_in_a:$a_in_b" in
            unknown:* | *:unknown) relation="undetermined" ;;
            not_present:not_present) relation="diverged" ;;
            not_present:*) relation="a_integrated_into_b" ;;
            *:not_present) relation="b_integrated_into_a" ;;
            *) relation="equivalent_changes" ;;
          esac
        fi
        printf 'relation=%s\n\n' "$relation"
      done
    done
  fi
fi
