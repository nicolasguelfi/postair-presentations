"""AI in the faculty 1/3 — une faculté par slide (gabarit faculty_slide)."""
# @guideline: postair-minimal

from custom.faculty_slide import build_faculty


def build():
    build_faculty(0, ratio=45, image_zoom=100 , zoom=130)
