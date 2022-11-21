# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: idna\core.py
from . import idnadata
import bisect, unicodedata, re
from typing import Union, Optional
from .intranges import intranges_contain
_virama_combining_class = 9
_alabel_prefix = b'xn--'
_unicode_dots_re = re.compile('[.。．｡]')

class IDNAError(UnicodeError):
    __doc__ = ' Base exception for all IDNA-encoding related problems '


class IDNABidiError(IDNAError):
    __doc__ = ' Exception when bidirectional requirements are not satisfied '


class InvalidCodepoint(IDNAError):
    __doc__ = ' Exception when a disallowed or unallocated codepoint is used '


class InvalidCodepointContext(IDNAError):
    __doc__ = ' Exception when the codepoint is not valid in the context it is used '


def _combining_class(cp: int) -> int:
    v = unicodedata.combining(chr(cp))
    if v == 0:
        if not unicodedata.name(chr(cp)):
            raise ValueError('Unknown character in unicodedata')
    return v


def _is_script(cp: str, script: str) -> bool:
    return intranges_contain(ord(cp), idnadata.scripts[script])


def _punycode(s: str) -> bytes:
    return s.encode('punycode')


def _unot(s: int) -> str:
    return 'U+{:04X}'.format(s)


def valid_label_length(label: Union[(bytes, str)]) -> bool:
    if len(label) > 63:
        return False
    else:
        return True


def valid_string_length(label: Union[(bytes, str)], trailing_dot: bool) -> bool:
    if len(label) > (254 if trailing_dot else 253):
        return False
    else:
        return True


def check_bidi(label: str, check_ltr: bool=False) -> bool:
    bidi_label = False
    for idx, cp in enumerate(label, 1):
        direction = unicodedata.bidirectional(cp)
        if direction == '':
            raise IDNABidiError('Unknown directionality in label {} at position {}'.format(repr(label), idx))
        if direction in ('R', 'AL', 'AN'):
            bidi_label = True

    if not bidi_label:
        if not check_ltr:
            return True
    else:
        direction = unicodedata.bidirectional(label[0])
        if direction in ('R', 'AL'):
            rtl = True
        else:
            if direction == 'L':
                rtl = False
            else:
                raise IDNABidiError('First codepoint in label {} must be directionality L, R or AL'.format(repr(label)))
    valid_ending = False
    number_type = None
    for idx, cp in enumerate(label, 1):
        direction = unicodedata.bidirectional(cp)
        if rtl:
            if direction not in ('R', 'AL', 'AN', 'EN', 'ES', 'CS', 'ET', 'ON', 'BN',
                                 'NSM'):
                raise IDNABidiError('Invalid direction for codepoint at position {} in a right-to-left label'.format(idx))
            if direction in ('R', 'AL', 'EN', 'AN'):
                valid_ending = True
            else:
                if direction != 'NSM':
                    valid_ending = False
                if direction in ('AN', 'EN'):
                    if not number_type:
                        number_type = direction
                    elif number_type != direction:
                        raise IDNABidiError('Can not mix numeral types in a right-to-left label')
                elif direction not in ('L', 'EN', 'ES', 'CS', 'ET', 'ON', 'BN', 'NSM'):
                    raise IDNABidiError('Invalid direction for codepoint at position {} in a left-to-right label'.format(idx))
            if direction in ('L', 'EN'):
                valid_ending = True
            elif direction != 'NSM':
                valid_ending = False

    if not valid_ending:
        raise IDNABidiError('Label ends with illegal codepoint directionality')
    return True


def check_initial_combiner(label: str) -> bool:
    if unicodedata.category(label[0])[0] == 'M':
        raise IDNAError('Label begins with an illegal combining character')
    return True


def check_hyphen_ok(label: str) -> bool:
    if label[2:4] == '--':
        raise IDNAError('Label has disallowed hyphens in 3rd and 4th position')
    if label[0] == '-' or label[(-1)] == '-':
        raise IDNAError('Label must not start or end with a hyphen')
    return True


def check_nfc(label: str) -> None:
    if unicodedata.normalize('NFC', label) != label:
        raise IDNAError('Label must be in Normalization Form C')


def valid_contextj(label: str, pos: int) -> bool:
    cp_value = ord(label[pos])
    if cp_value == 8204:
        if pos > 0:
            if _combining_class(ord(label[(pos - 1)])) == _virama_combining_class:
                return True
        ok = False
        for i in range(pos - 1, -1, -1):
            joining_type = idnadata.joining_types.get(ord(label[i]))
            if joining_type == ord('T'):
                pass
            elif joining_type in [ord('L'), ord('D')]:
                ok = True
                break

        if not ok:
            return False
        ok = False
        for i in range(pos + 1, len(label)):
            joining_type = idnadata.joining_types.get(ord(label[i]))
            if joining_type == ord('T'):
                pass
            elif joining_type in [ord('R'), ord('D')]:
                ok = True
                break

        return ok
    else:
        if cp_value == 8205:
            if pos > 0:
                if _combining_class(ord(label[(pos - 1)])) == _virama_combining_class:
                    return True
            return False
        return False


def valid_contexto(label: str, pos: int, exception: bool=False) -> bool:
    cp_value = ord(label[pos])
    if cp_value == 183:
        if 0 < pos < len(label) - 1:
            if ord(label[(pos - 1)]) == 108:
                if ord(label[(pos + 1)]) == 108:
                    return True
        return False
    if cp_value == 885:
        if pos < len(label) - 1:
            if len(label) > 1:
                return _is_script(label[(pos + 1)], 'Greek')
        return False
    if cp_value == 1523 or cp_value == 1524:
        if pos > 0:
            return _is_script(label[(pos - 1)], 'Hebrew')
        else:
            return False
    if cp_value == 12539:
        for cp in label:
            if cp == '・':
                pass
            else:
                if _is_script(cp, 'Hiragana') or _is_script(cp, 'Katakana') or _is_script(cp, 'Han'):
                    return True

        return False
    if 1632 <= cp_value <= 1641:
        for cp in label:
            if 1776 <= ord(cp) <= 1785:
                return False

        return True
    else:
        if 1776 <= cp_value <= 1785:
            for cp in label:
                if 1632 <= ord(cp) <= 1641:
                    return False

            return True
        return False


def check_label(label: Union[(str, bytes, bytearray)]) -> None:
    if isinstance(label, (bytes, bytearray)):
        label = label.decode('utf-8')
    if len(label) == 0:
        raise IDNAError('Empty Label')
    check_nfc(label)
    check_hyphen_ok(label)
    check_initial_combiner(label)
    for pos, cp in enumerate(label):
        cp_value = ord(cp)
        if intranges_contain(cp_value, idnadata.codepoint_classes['PVALID']):
            continue
        else:
            if intranges_contain(cp_value, idnadata.codepoint_classes['CONTEXTJ']):
                try:
                    if not valid_contextj(label, pos):
                        raise InvalidCodepointContext('Joiner {} not allowed at position {} in {}'.format(_unot(cp_value), pos + 1, repr(label)))
                except ValueError:
                    raise IDNAError('Unknown codepoint adjacent to joiner {} at position {} in {}'.format(_unot(cp_value), pos + 1, repr(label)))

            if intranges_contain(cp_value, idnadata.codepoint_classes['CONTEXTO']):
                if not valid_contexto(label, pos):
                    raise InvalidCodepointContext('Codepoint {} not allowed at position {} in {}'.format(_unot(cp_value), pos + 1, repr(label)))
            else:
                raise InvalidCodepoint('Codepoint {} at position {} of {} not allowed'.format(_unot(cp_value), pos + 1, repr(label)))

    check_bidi(label)


def alabel(label: str) -> bytes:
    try:
        label_bytes = label.encode('ascii')
        ulabel(label_bytes)
        if not valid_label_length(label_bytes):
            raise IDNAError('Label too long')
        return label_bytes
    except UnicodeEncodeError:
        pass

    if not label:
        raise IDNAError('No Input')
    label = str(label)
    check_label(label)
    label_bytes = _punycode(label)
    label_bytes = _alabel_prefix + label_bytes
    if not valid_label_length(label_bytes):
        raise IDNAError('Label too long')
    return label_bytes


def ulabel(label: Union[(str, bytes, bytearray)]) -> str:
    if not isinstance(label, (bytes, bytearray)):
        try:
            label_bytes = label.encode('ascii')
        except UnicodeEncodeError:
            check_label(label)
            return label

    else:
        label_bytes = label
    label_bytes = label_bytes.lower()
    if label_bytes.startswith(_alabel_prefix):
        label_bytes = label_bytes[len(_alabel_prefix):]
        if not label_bytes:
            raise IDNAError('Malformed A-label, no Punycode eligible content found')
        if label_bytes.decode('ascii')[(-1)] == '-':
            raise IDNAError('A-label must not end with a hyphen')
    else:
        check_label(label_bytes)
        return label_bytes.decode('ascii')
    try:
        label = label_bytes.decode('punycode')
    except UnicodeError:
        raise IDNAError('Invalid A-label')

    check_label(label)
    return label


def uts46_remap(domain: str, std3_rules: bool=True, transitional: bool=False) -> str:
    """Re-map the characters in the string according to UTS46 processing."""
    from .uts46data import uts46data
    output = ''
    for pos, char in enumerate(domain):
        code_point = ord(char)
        try:
            uts46row = uts46data[(code_point if code_point < 256 else bisect.bisect_left(uts46data, (code_point, 'Z')) - 1)]
            status = uts46row[1]
            replacement = None
            if len(uts46row) == 3:
                replacement = uts46row[2]
            if status == 'V' or status == 'D' and not transitional or status == '3' and not std3_rules and replacement is None:
                output += char
            else:
                if replacement is not None:
                    if status == 'M' or status == '3' and not std3_rules or status == 'D' and transitional:
                        output += replacement
            if status != 'I':
                raise IndexError()
        except IndexError:
            raise InvalidCodepoint('Codepoint {} not allowed at position {} in {}'.format(_unot(code_point), pos + 1, repr(domain)))

    return unicodedata.normalize('NFC', output)


def encode(s: Union[(str, bytes, bytearray)], strict: bool=False, uts46: bool=False, std3_rules: bool=False, transitional: bool=False) -> bytes:
    if isinstance(s, (bytes, bytearray)):
        s = s.decode('ascii')
    else:
        if uts46:
            s = uts46_remap(s, std3_rules, transitional)
        else:
            trailing_dot = False
            result = []
            if strict:
                labels = s.split('.')
            else:
                labels = _unicode_dots_re.split(s)
            if not labels or labels == ['']:
                raise IDNAError('Empty domain')
            if labels[(-1)] == '':
                del labels[-1]
                trailing_dot = True
            for label in labels:
                s = alabel(label)
                if s:
                    result.append(s)
                else:
                    raise IDNAError('Empty label')

            if trailing_dot:
                result.append(b'')
        s = (b'.').join(result)
        raise valid_string_length(s, trailing_dot) or IDNAError('Domain too long')
    return s


def decode(s: Union[(str, bytes, bytearray)], strict: bool=False, uts46: bool=False, std3_rules: bool=False) -> str:
    try:
        if isinstance(s, (bytes, bytearray)):
            s = s.decode('ascii')
    except UnicodeDecodeError:
        raise IDNAError('Invalid ASCII in A-label')

    if uts46:
        s = uts46_remap(s, std3_rules, False)
    else:
        trailing_dot = False
        result = []
        if not strict:
            labels = _unicode_dots_re.split(s)
        else:
            labels = s.split('.')
    if not labels or labels == ['']:
        raise IDNAError('Empty domain')
    if not labels[(-1)]:
        del labels[-1]
        trailing_dot = True
    for label in labels:
        s = ulabel(label)
        if s:
            result.append(s)
        else:
            raise IDNAError('Empty label')

    if trailing_dot:
        result.append('')
    return '.'.join(result)