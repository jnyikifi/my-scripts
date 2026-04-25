#!/opt/homebrew/bin/python3

import struct
import sys

from PIL import ExifTags, Image

# Nikon MakerNote tag names (partial list of known tags)
NIKON_TAGS = {
    0x0001: "MakerNoteVersion",
    0x0002: "ISO",
    0x0003: "ColorMode",
    0x0004: "Quality",
    0x0005: "WhiteBalance",
    0x0006: "Sharpening",
    0x0007: "FocusMode",
    0x0008: "FlashSetting",
    0x0009: "FlashType",
    0x000B: "WhiteBalanceFineTune",
    0x000C: "WB_RBLevels",
    0x000D: "ProgramShift",
    0x000E: "ExposureDifference",
    0x000F: "ISOSelection",
    0x0010: "DataDump",
    0x0011: "PreviewIFD",
    0x0012: "FlashExposureComp",
    0x0013: "ISOSetting",
    0x0014: "ColorBalanceA",
    0x0016: "ImageBoundary",
    0x0017: "ExternalFlashExposureComp",
    0x0018: "FlashExposureBracketValue",
    0x0019: "ExposureBracketValue",
    0x001A: "ImageProcessing",
    0x001B: "CropHiSpeed",
    0x001C: "ExposureTuning",
    0x001D: "SerialNumber",
    0x001E: "ColorSpace",
    0x001F: "VRInfo",
    0x0020: "ImageAuthentication",
    0x0021: "FaceDetect",
    0x0022: "ActiveD-Lighting",
    0x0023: "PictureControlData",
    0x0024: "WorldTime",
    0x0025: "ISOInfo",
    0x002A: "VignetteControl",
    0x002B: "DistortInfo",
    0x002C: "UnknownInfo",
    0x0032: "UnknownInfo2",
    0x0035: "HDRInfo",
    0x0037: "MechanicalShutterCount",
    0x0039: "LocationInfo",
    0x003D: "BlackLevel",
    0x0045: "CropArea",
    0x004F: "ColorTemperatureAuto",
    0x0080: "ImageAdjustment",
    0x0081: "ToneComp",
    0x0082: "AuxiliaryLens",
    0x0083: "LensType",
    0x0084: "Lens",
    0x0085: "ManualFocusDistance",
    0x0086: "DigitalZoom",
    0x0087: "FlashMode",
    0x0088: "AFInfo",
    0x0089: "ShootingMode",
    0x008A: "AutoBracketRelease",
    0x008B: "LensFStops",
    0x008C: "ContrastCurve",
    0x008D: "ColorHue",
    0x008F: "SceneMode",
    0x0090: "LightSource",
    0x0091: "ShotInfo",
    0x0092: "HueAdjustment",
    0x0093: "NEFCompression",
    0x0094: "Saturation",
    0x0095: "NoiseReduction",
    0x0096: "NEFLinearizationTable",
    0x0097: "ColorBalance",
    0x0098: "LensData",
    0x0099: "RawImageCenter",
    0x009A: "SensorPixelSize",
    0x009C: "SceneAssist",
    0x009E: "RetouchHistory",
    0x00A0: "SerialNumber",
    0x00A2: "ImageDataSize",
    0x00A5: "ImageCount",
    0x00A6: "DeletedImageCount",
    0x00A7: "ShutterCount",
    0x00A8: "FlashInfo",
    0x00A9: "ImageOptimization",
    0x00AA: "Saturation",
    0x00AB: "VariProgram",
    0x00AC: "ImageStabilization",
    0x00AD: "AFResponse",
    0x00B0: "MultiExposure",
    0x00B1: "HighISONoiseReduction",
    0x00B3: "ToningEffect",
    0x00B6: "PowerUpTime",
    0x00B7: "AFInfo2",
    0x00B8: "FileInfo",
    0x00B9: "AFTune",
    0x00BD: "PictureControlData",
    0x00C3: "BarometerInfo",
}


def parse_nikon_makernote(data):
    """Parse Nikon MakerNote data and return a dict of tags."""
    tags = {}

    # Check for Nikon header
    if not data.startswith(b"Nikon\x00"):
        return tags

    # Skip "Nikon\x00" (6 bytes) + version info (4 bytes)
    offset = 10

    # Determine byte order from TIFF header
    byte_order = data[offset : offset + 2]
    if byte_order == b"MM":
        endian = ">"  # Big-endian
    elif byte_order == b"II":
        endian = "<"  # Little-endian
    else:
        return tags

    # Skip to IFD offset (after byte order + magic 0x002a)
    ifd_offset = struct.unpack(endian + "I", data[offset + 4 : offset + 8])[0]
    ifd_pos = offset + ifd_offset

    # Read number of entries
    num_entries = struct.unpack(endian + "H", data[ifd_pos : ifd_pos + 2])[0]
    ifd_pos += 2

    # Type sizes
    type_sizes = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 7: 1, 8: 2, 9: 4, 10: 8, 11: 4, 12: 8}

    for _ in range(num_entries):
        if ifd_pos + 12 > len(data):
            break

        tag_id = struct.unpack(endian + "H", data[ifd_pos : ifd_pos + 2])[0]
        tag_type = struct.unpack(endian + "H", data[ifd_pos + 2 : ifd_pos + 4])[0]
        count = struct.unpack(endian + "I", data[ifd_pos + 4 : ifd_pos + 8])[0]
        value_offset = data[ifd_pos + 8 : ifd_pos + 12]

        ifd_pos += 12

        # Calculate data size
        type_size = type_sizes.get(tag_type, 1)
        data_size = count * type_size

        # Get the actual data
        if data_size <= 4:
            raw_value = value_offset[:data_size]
        else:
            val_offset = struct.unpack(endian + "I", value_offset)[0]
            raw_value = data[offset + val_offset : offset + val_offset + data_size]

        # Parse value based on type
        try:
            if tag_type == 1:  # BYTE
                value = list(raw_value)
            elif tag_type == 2:  # ASCII
                value = raw_value.rstrip(b"\x00").decode("ascii", errors="replace")
            elif tag_type == 3:  # SHORT
                value = list(
                    struct.unpack(endian + "H" * count, raw_value[: count * 2])
                )
                if len(value) == 1:
                    value = value[0]
            elif tag_type == 4:  # LONG
                value = list(
                    struct.unpack(endian + "I" * count, raw_value[: count * 4])
                )
                if len(value) == 1:
                    value = value[0]
            elif tag_type == 5:  # RATIONAL
                value = []
                for i in range(count):
                    num = struct.unpack(endian + "I", raw_value[i * 8 : i * 8 + 4])[0]
                    den = struct.unpack(endian + "I", raw_value[i * 8 + 4 : i * 8 + 8])[
                        0
                    ]
                    value.append(f"{num}/{den}" if den else "0")
                if len(value) == 1:
                    value = value[0]
            elif tag_type == 7:  # UNDEFINED
                value = (
                    raw_value.hex()
                    if len(raw_value) <= 32
                    else f"({len(raw_value)} bytes)"
                )
            elif tag_type == 9:  # SLONG
                value = list(
                    struct.unpack(endian + "i" * count, raw_value[: count * 4])
                )
                if len(value) == 1:
                    value = value[0]
            elif tag_type == 10:  # SRATIONAL
                value = []
                for i in range(count):
                    num = struct.unpack(endian + "i", raw_value[i * 8 : i * 8 + 4])[0]
                    den = struct.unpack(endian + "i", raw_value[i * 8 + 4 : i * 8 + 8])[
                        0
                    ]
                    value.append(f"{num}/{den}" if den else "0")
                if len(value) == 1:
                    value = value[0]
            else:
                value = (
                    raw_value.hex()
                    if len(raw_value) <= 32
                    else f"({len(raw_value)} bytes)"
                )
        except Exception:
            value = f"(parse error, {data_size} bytes)"

        tag_name = NIKON_TAGS.get(tag_id, f"Tag_{tag_id:#06x}")
        tags[tag_name] = value

    return tags


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <image_file>")
    sys.exit(1)

img = Image.open(sys.argv[1])
img_exif = img.getexif()
# print(type(img_exif))
# <class 'PIL.Image.Exif'>

print(img_exif)

if img_exif is None:
    print("Sorry, image has no exif data.")
else:
    for key, val in img_exif.items():
        tag_name = ExifTags.TAGS.get(key, key)
        print(f"{tag_name}:{val}")

    # Print IFD (sub-directory) EXIF data
    for ifd_id in ExifTags.IFD:
        try:
            ifd = img_exif.get_ifd(ifd_id)
            if ifd:
                print(f"\n--- {ifd_id.name} ---")
                for key, val in ifd.items():
                    # Skip MakerNote here, we'll parse it separately
                    if key == 37500:
                        continue
                    tag_name = ExifTags.TAGS.get(key, key)
                    print(f"{tag_name}:{val}")

                # Parse MakerNote if present in Exif IFD
                if ifd_id == ExifTags.IFD.Exif and 37500 in ifd:
                    makernote_data = ifd[37500]
                    if isinstance(makernote_data, bytes):
                        print(f"\n--- MakerNote ---")
                        makernote_tags = parse_nikon_makernote(makernote_data)
                        if makernote_tags:
                            for tag_name, val in makernote_tags.items():
                                print(f"{tag_name}:{val}")
                        else:
                            print("(Unable to parse MakerNote or unknown format)")
        except KeyError:
            pass
