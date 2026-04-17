#!/usr/bin/env python3
"""
BU1 Blog Image Strategy Validator
=================================

Checks that source blog drafts follow the BU1 image planning workflow:

- exactly one hero image per article
- enough images for the article length
- meaningful inline image placement tied to real H2 headings
- alt text and metadata required for future upload automation

Usage:
    python3 scripts/validate_blog_images.py
    python3 scripts/validate_blog_images.py drafts/blog/2026-04-17-example.md
"""

import argparse
import glob
import os
import re
import sys


BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DRAFT_GLOB = os.path.join(BASE_DIR, "drafts", "blog", "*.md")

INLINE_KINDS_REQUIRING_CAPTION = {"infographic", "diagram", "chart", "timeline"}
GENERIC_ALT_PREFIXES = (
    "obrazek",
    "obrázek",
    "fotografie",
    "foto",
    "image of",
    "photo of",
)


def strip_yaml_scalar(value):
    value = value.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def normalize_space(text):
    return re.sub(r"\s+", " ", text).strip()


def strip_tags(text):
    return normalize_space(re.sub(r"<[^>]+>", " ", text))


def extract_frontmatter(text, path):
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing opening frontmatter delimiter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError(f"{path}: missing closing frontmatter delimiter")
    return text[4:end], text[end + 5 :]


def parse_top_level(frontmatter):
    data = {}
    for line in frontmatter.splitlines():
        if not line or line.startswith("#") or line.startswith(" ") or line.startswith("\t"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = strip_yaml_scalar(value)
    return data


def parse_images(frontmatter):
    images = []
    current = None
    in_images = False

    for raw_line in frontmatter.splitlines():
        if not in_images:
            if raw_line.strip() == "images:":
                in_images = True
            continue

        if not raw_line.strip():
            continue

        if not raw_line.startswith("  "):
            break

        if raw_line.startswith("  - "):
            if current:
                images.append(current)
            current = {}
            remainder = raw_line[4:]
            if ":" in remainder:
                key, value = remainder.split(":", 1)
                current[key.strip()] = strip_yaml_scalar(value)
            continue

        if current and raw_line.startswith("    ") and ":" in raw_line:
            key, value = raw_line.strip().split(":", 1)
            current[key.strip()] = strip_yaml_scalar(value)

    if current:
        images.append(current)

    return images


def extract_h2s(body):
    matches = re.findall(r"<h2>(.*?)</h2>", body, flags=re.IGNORECASE | re.DOTALL)
    return [strip_tags(match) for match in matches]


def count_words(body):
    text = strip_tags(re.sub(r"<!--.*?-->", " ", body, flags=re.DOTALL))
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def parse_size(size_value):
    match = re.fullmatch(r"(\d+)x(\d+)", size_value or "")
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def minimum_image_count(word_count):
    if word_count < 900:
        return 1
    if word_count <= 1500:
        return 2
    return 3


def validate_draft(path):
    text = open(path, encoding="utf-8").read()
    frontmatter, body = extract_frontmatter(text, path)
    top_level = parse_top_level(frontmatter)
    images = parse_images(frontmatter)
    h2s = extract_h2s(body)
    word_count = count_words(body)

    errors = []
    warnings = []

    def error(message):
        errors.append(message)

    def warning(message):
        warnings.append(message)

    title = top_level.get("title") or os.path.basename(path)
    min_images = minimum_image_count(word_count)

    if not images:
        error("missing images block in frontmatter")
        return title, word_count, h2s, errors, warnings

    roles = []
    hero_images = []
    inline_headings = []

    for index, image in enumerate(images, start=1):
        role = image.get("role", "").strip()
        kind = image.get("kind", "").strip()
        size = image.get("size", "").strip()
        placement = image.get("placement", "").strip()
        alt = image.get("alt", "").strip()
        prompt = image.get("prompt", "").strip()
        after_heading = image.get("after_heading", "").strip()
        caption = image.get("caption", "").strip()

        label = f"image #{index}" if not role else f"image `{role}`"

        for required in ("role", "kind", "size", "placement", "alt", "prompt"):
            if not image.get(required, "").strip():
                error(f"{label}: missing `{required}`")

        if role:
            roles.append(role)

        parsed_size = parse_size(size)
        if not parsed_size:
            error(f"{label}: invalid `size` value `{size}`; expected WIDTHxHEIGHT")
        else:
            width, height = parsed_size
            if width <= height:
                error(f"{label}: image must be landscape; got {size}")
            if placement == "top" and width < 1600:
                error(f"{label}: hero image must be at least 1600px wide")
            if placement == "after_h2" and width < 1200:
                error(f"{label}: inline image should be at least 1200px wide")

        alt_length = len(alt)
        if alt_length > 150:
            error(f"{label}: alt text is {alt_length} characters; cap it at 150")

        alt_prefix = alt.lower().strip()
        if alt_prefix.startswith(GENERIC_ALT_PREFIXES):
            error(f"{label}: alt text starts generically; describe meaning, not `obrázek/foto`")

        if kind in INLINE_KINDS_REQUIRING_CAPTION and not caption:
            error(f"{label}: `{kind}` requires a `caption` with the takeaway")

        if placement == "top":
            hero_images.append(image)
            if after_heading:
                error(f"{label}: hero image cannot define `after_heading`")
        elif placement == "after_h2":
            if not after_heading:
                error(f"{label}: inline image must define `after_heading`")
            elif after_heading not in h2s:
                error(f"{label}: `after_heading` does not match any H2 in body")
            else:
                inline_headings.append(after_heading)
        else:
            error(f"{label}: invalid `placement` `{placement}`; use `top` or `after_h2`")

    if len(set(roles)) != len(roles):
        error("image `role` values must be unique machine-readable slugs")

    if len(hero_images) != 1:
        error(f"expected exactly one hero image; found {len(hero_images)}")

    if len(images) < min_images:
        error(
            f"article has {word_count} words and needs at least {min_images} image(s); found {len(images)}"
        )

    if len(images) > 5:
        error("default ceiling is 5 images per article; reduce unless there is strong editorial need")

    if len(set(inline_headings)) != len(inline_headings):
        error("multiple inline images point to the same H2; spread visuals across the article")

    if inline_headings:
        anchor_positions = sorted(h2s.index(heading) + 1 for heading in inline_headings)
        first_allowed_late_index = min(2, len(h2s))
        if word_count >= 900 and anchor_positions[0] > first_allowed_late_index:
            error("first inline image is too late; place one after the first or second H2")

        if min_images >= 3:
            midpoint = (len(h2s) + 1) // 2
            if anchor_positions[-1] <= midpoint:
                error("long article needs an inline image in the second half of the article")

    if len(images) == min_images and word_count > 1450 and min_images == 2:
        warning("article is near the 1500-word threshold; consider a third image if a section is visually complex")

    return title, word_count, h2s, errors, warnings


def resolve_paths(args):
    if args:
        return [os.path.abspath(path) for path in args]
    return sorted(glob.glob(DRAFT_GLOB))


def main():
    parser = argparse.ArgumentParser(description="Validate BU1 blog image strategy")
    parser.add_argument("paths", nargs="*", help="Optional draft paths")
    options = parser.parse_args()

    paths = resolve_paths(options.paths)
    if not paths:
        print("No draft files found.")
        return 0

    failures = 0

    for path in paths:
        try:
            title, word_count, h2s, errors, warnings = validate_draft(path)
        except Exception as exc:  # pylint: disable=broad-except
            failures += 1
            print(f"FAIL {path}")
            print(f"  - {exc}")
            continue

        status = "PASS" if not errors else "FAIL"
        print(f"{status} {path}")
        print(f"  - title: {title}")
        print(f"  - words: {word_count}")
        print(f"  - h2_count: {len(h2s)}")

        for item in warnings:
            print(f"  - WARNING: {item}")

        for item in errors:
            print(f"  - ERROR: {item}")

        if errors:
            failures += 1

    if failures:
        print(f"\nImage validation failed for {failures} draft(s).")
        return 1

    print(f"\nImage validation passed for {len(paths)} draft(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
