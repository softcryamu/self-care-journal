#!/usr/bin/env python3
"""Create a fillable digital PDF from the print Self Care Journal PDF.

This script keeps the original PDF pages intact. It does not rasterize,
JPEG-convert, or recompress the page contents. It only adds transparent
AcroForm widgets and link annotations on top of the existing pages.

Default input : SelfCareJournal_print_final.pdf.pdf
Default output: SelfCareJournal_fillable.pdf
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_INPUT = "SelfCareJournal_print_final.pdf.pdf"
DEFAULT_OUTPUT = "SelfCareJournal_fillable.pdf"

# PDF uses points. The source document is A4-sized: 595.2756 x 841.8898 pt.
# Page numbers below are human page numbers, converted to zero-based indexes at runtime.


@dataclass(frozen=True)
class CheckboxSpec:
    page: int
    name: str
    rect: tuple[float, float, float, float]


@dataclass(frozen=True)
class TextSpec:
    page: int
    name: str
    rect: tuple[float, float, float, float]
    multiline: bool = True
    font_size: int = 12


@dataclass(frozen=True)
class LinkSpec:
    page: int
    name: str
    rect: tuple[float, float, float, float]
    uri: str


CHECKBOXES: tuple[CheckboxSpec, ...] = (
    # Page 3 checkboxes
    CheckboxSpec(3, "p3_check_01", (78.651, 592.0596, 91.34706, 604.7556)),
    CheckboxSpec(3, "p3_check_02", (78.651, 561.589, 91.34706, 574.28506)),
    CheckboxSpec(3, "p3_check_03", (78.651, 530.5542, 91.34706, 543.25027)),
    CheckboxSpec(3, "p3_check_04", (78.651, 500.08366, 91.34706, 512.7797)),
    CheckboxSpec(3, "p3_check_05", (78.651, 393.43678, 91.34706, 406.1328)),
    CheckboxSpec(3, "p3_check_06", (78.651, 363.5305, 91.34706, 376.22657)),
    CheckboxSpec(3, "p3_check_07", (78.651, 332.49568, 91.34706, 345.19175)),
    CheckboxSpec(3, "p3_check_08", (78.651, 300.8966, 91.34706, 313.59266)),
    CheckboxSpec(3, "p3_check_09", (78.651, 199.32813, 91.34706, 212.02417)),
    CheckboxSpec(3, "p3_check_10", (78.651, 168.29334, 91.34706, 180.98938)),
    CheckboxSpec(3, "p3_check_11", (78.651, 136.69422, 91.34706, 149.39032)),
    CheckboxSpec(3, "p3_check_12", (78.651, 105.09515, 91.34706, 117.7912)),
    # Page 7 checkboxes
    CheckboxSpec(7, "p7_check_01", (100.11255, 585.8526, 112.80861, 598.54867)),
    CheckboxSpec(7, "p7_check_02", (100.11255, 558.7677, 112.80861, 571.46377)),
    CheckboxSpec(7, "p7_check_03", (100.11255, 531.68276, 112.80861, 544.3788)),
    CheckboxSpec(7, "p7_check_04", (100.11255, 504.5978, 112.80861, 517.2938)),
    CheckboxSpec(7, "p7_check_05", (100.11255, 478.07716, 112.80861, 490.77323)),
    CheckboxSpec(7, "p7_check_06", (100.11255, 450.99223, 112.80861, 463.6883)),
)

TEXT_FIELDS: tuple[TextSpec, ...] = (
    # Page 5 large writing area
    TextSpec(5, "p5_writing_area", (68.90287, 73.35504, 520.725, 338.56159)),
    # Page 7: "other" short field and lower writing area
    TextSpec(7, "p7_other", (188.07094, 445.77275, 326.44148, 467.21498), multiline=False),
    TextSpec(7, "p7_writing_area", (83.58708, 90.28308, 512.81808, 324.45484)),
)

LINKS: tuple[LinkSpec, ...] = (
    LinkSpec(9, "blog", (160.96161, 89.71881, 350.1621, 113.41815), "https://windandsky2.com/"),
    LinkSpec(9, "note", (160.96161, 55.86267, 378.401, 79.56195), "https://note.com/mona_soyokaze"),
    LinkSpec(9, "x", (160.96161, 19.74945, 384.04878, 43.44873), "https://x.com/windandsky22"),
)


def _import_pypdf():
    try:
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import (
            ArrayObject,
            BooleanObject,
            DecodedStreamObject,
            DictionaryObject,
            FloatObject,
            NameObject,
            NumberObject,
            TextStringObject,
        )
    except ModuleNotFoundError as exc:  # pragma: no cover - depends on user environment
        raise SystemExit(
            "pypdf is not installed. Install it first with: python -m pip install pypdf"
        ) from exc

    return {
        "PdfReader": PdfReader,
        "PdfWriter": PdfWriter,
        "ArrayObject": ArrayObject,
        "BooleanObject": BooleanObject,
        "DecodedStreamObject": DecodedStreamObject,
        "DictionaryObject": DictionaryObject,
        "FloatObject": FloatObject,
        "NameObject": NameObject,
        "NumberObject": NumberObject,
        "TextStringObject": TextStringObject,
    }


def _rect(values: Iterable[float], ArrayObject, FloatObject):
    return ArrayObject([FloatObject(value) for value in values])


def _get_writer_add_object(writer):
    # pypdf exposes _add_object as the stable low-level API used by its own writers.
    return writer._add_object  # noqa: SLF001


def _make_checkbox_appearances(writer, width: float, height: float, pdf):
    DictionaryObject = pdf["DictionaryObject"]
    NameObject = pdf["NameObject"]
    ArrayObject = pdf["ArrayObject"]
    FloatObject = pdf["FloatObject"]
    DecodedStreamObject = pdf["DecodedStreamObject"]

    add_object = _get_writer_add_object(writer)
    bbox = _rect((0, 0, width, height), ArrayObject, FloatObject)

    off = DecodedStreamObject()
    off.set_data(b"")
    off.update(
        {
            NameObject("/Type"): NameObject("/XObject"),
            NameObject("/Subtype"): NameObject("/Form"),
            NameObject("/BBox"): bbox,
        }
    )

    yes = DecodedStreamObject()
    mark = (
        "q\n"
        "0 0 0 RG 0 0 0 rg\n"
        "1.4 w 1 J 1 j\n"
        f"{width * 0.18:.3f} {height * 0.52:.3f} m\n"
        f"{width * 0.42:.3f} {height * 0.22:.3f} l\n"
        f"{width * 0.84:.3f} {height * 0.82:.3f} l\n"
        "S\n"
        "Q\n"
    ).encode("ascii")
    yes.set_data(mark)
    yes.update(
        {
            NameObject("/Type"): NameObject("/XObject"),
            NameObject("/Subtype"): NameObject("/Form"),
            NameObject("/BBox"): bbox,
        }
    )

    return add_object(off), add_object(yes)


def _add_annotation_to_page(page, annotation_ref, pdf) -> None:
    NameObject = pdf["NameObject"]
    ArrayObject = pdf["ArrayObject"]

    annotations = page.get(NameObject("/Annots"))
    if annotations is None:
        annotations = ArrayObject()
        page[NameObject("/Annots")] = annotations
    else:
        annotations = annotations.get_object()
    annotations.append(annotation_ref)


def _add_checkbox(writer, page, field_refs, spec: CheckboxSpec, pdf) -> None:
    DictionaryObject = pdf["DictionaryObject"]
    NameObject = pdf["NameObject"]
    NumberObject = pdf["NumberObject"]
    TextStringObject = pdf["TextStringObject"]
    ArrayObject = pdf["ArrayObject"]
    FloatObject = pdf["FloatObject"]

    x1, y1, x2, y2 = spec.rect
    off_ref, yes_ref = _make_checkbox_appearances(writer, x2 - x1, y2 - y1, pdf)
    checkbox = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Widget"),
            NameObject("/FT"): NameObject("/Btn"),
            NameObject("/T"): TextStringObject(spec.name),
            NameObject("/Rect"): _rect(spec.rect, ArrayObject, FloatObject),
            NameObject("/F"): NumberObject(4),
            NameObject("/Ff"): NumberObject(0),
            NameObject("/V"): NameObject("/Off"),
            NameObject("/AS"): NameObject("/Off"),
            NameObject("/DA"): TextStringObject("0 0 0 rg /Helv 0 Tf"),
            NameObject("/BS"): DictionaryObject({NameObject("/W"): NumberObject(0)}),
            NameObject("/AP"): DictionaryObject(
                {
                    NameObject("/N"): DictionaryObject(
                        {NameObject("/Off"): off_ref, NameObject("/Yes"): yes_ref}
                    )
                }
            ),
        }
    )
    annotation_ref = _get_writer_add_object(writer)(checkbox)
    _add_annotation_to_page(page, annotation_ref, pdf)
    field_refs.append(annotation_ref)


def _add_text_field(writer, page, field_refs, spec: TextSpec, pdf) -> None:
    DictionaryObject = pdf["DictionaryObject"]
    NameObject = pdf["NameObject"]
    NumberObject = pdf["NumberObject"]
    TextStringObject = pdf["TextStringObject"]
    ArrayObject = pdf["ArrayObject"]
    FloatObject = pdf["FloatObject"]

    flags = 4096 if spec.multiline else 0
    text_field = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Widget"),
            NameObject("/FT"): NameObject("/Tx"),
            NameObject("/T"): TextStringObject(spec.name),
            NameObject("/Rect"): _rect(spec.rect, ArrayObject, FloatObject),
            NameObject("/F"): NumberObject(4),
            NameObject("/Ff"): NumberObject(flags),
            NameObject("/V"): TextStringObject(""),
            NameObject("/DV"): TextStringObject(""),
            NameObject("/DA"): TextStringObject(f"0.15 0.15 0.15 rg /Helv {spec.font_size} Tf"),
            NameObject("/BS"): DictionaryObject({NameObject("/W"): NumberObject(0)}),
        }
    )
    annotation_ref = _get_writer_add_object(writer)(text_field)
    _add_annotation_to_page(page, annotation_ref, pdf)
    field_refs.append(annotation_ref)


def _add_link(writer, page, spec: LinkSpec, pdf) -> None:
    DictionaryObject = pdf["DictionaryObject"]
    NameObject = pdf["NameObject"]
    NumberObject = pdf["NumberObject"]
    TextStringObject = pdf["TextStringObject"]
    ArrayObject = pdf["ArrayObject"]
    FloatObject = pdf["FloatObject"]

    link = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/Link"),
            NameObject("/Rect"): _rect(spec.rect, ArrayObject, FloatObject),
            NameObject("/Border"): ArrayObject([NumberObject(0), NumberObject(0), NumberObject(0)]),
            NameObject("/A"): DictionaryObject(
                {
                    NameObject("/S"): NameObject("/URI"),
                    NameObject("/URI"): TextStringObject(spec.uri),
                }
            ),
            NameObject("/NM"): TextStringObject(f"link_{spec.name}"),
        }
    )
    annotation_ref = _get_writer_add_object(writer)(link)
    _add_annotation_to_page(page, annotation_ref, pdf)


def create_fillable_pdf(input_pdf: Path, output_pdf: Path) -> None:
    pdf = _import_pypdf()
    PdfReader = pdf["PdfReader"]
    PdfWriter = pdf["PdfWriter"]
    DictionaryObject = pdf["DictionaryObject"]
    NameObject = pdf["NameObject"]
    ArrayObject = pdf["ArrayObject"]
    BooleanObject = pdf["BooleanObject"]
    TextStringObject = pdf["TextStringObject"]

    if not input_pdf.exists():
        raise SystemExit(f"Input PDF not found: {input_pdf}")

    reader = PdfReader(str(input_pdf))
    writer = PdfWriter()
    for source_page in reader.pages:
        writer.add_page(source_page)

    if len(writer.pages) < 9:
        raise SystemExit(f"Expected at least 9 pages, but found {len(writer.pages)} pages in {input_pdf}")

    font = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject("/Helvetica"),
            NameObject("/Encoding"): NameObject("/WinAnsiEncoding"),
        }
    )
    font_ref = _get_writer_add_object(writer)(font)
    field_refs = ArrayObject()

    acroform = DictionaryObject(
        {
            NameObject("/Fields"): field_refs,
            NameObject("/NeedAppearances"): BooleanObject(True),
            NameObject("/DA"): TextStringObject("/Helv 12 Tf 0 g"),
            NameObject("/DR"): DictionaryObject(
                {NameObject("/Font"): DictionaryObject({NameObject("/Helv"): font_ref})}
            ),
        }
    )
    writer._root_object.update({NameObject("/AcroForm"): _get_writer_add_object(writer)(acroform)})  # noqa: SLF001

    for spec in CHECKBOXES:
        _add_checkbox(writer, writer.pages[spec.page - 1], field_refs, spec, pdf)

    for spec in TEXT_FIELDS:
        _add_text_field(writer, writer.pages[spec.page - 1], field_refs, spec, pdf)

    for spec in LINKS:
        _add_link(writer, writer.pages[spec.page - 1], spec, pdf)

    with output_pdf.open("wb") as output_file:
        writer.write(output_file)

    print(f"Created: {output_pdf}")
    print(f"Pages: {len(writer.pages)}")
    print(f"Form fields: {len(CHECKBOXES) + len(TEXT_FIELDS)}")
    print(f"Links: {len(LINKS)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add transparent fillable form fields and links to the Self Care Journal print PDF."
    )
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        type=Path,
        help=f"Input print PDF path. Default: {DEFAULT_INPUT}",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        type=Path,
        help=f"Output fillable PDF path. Default: {DEFAULT_OUTPUT}",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    create_fillable_pdf(args.input, args.output)


if __name__ == "__main__":
    main()
