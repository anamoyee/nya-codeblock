from collections.abc import Callable

from nya_extract_error import extract_error, extract_traceback

BACKTICK = "`"
BACKTICKS = 3 * BACKTICK
NEWLINE = "\n"


def _default_cut_at(text: str, max_length: int) -> str:
	"""Cut text at max_length, if text is longer than max_length.

	Args:
		text: The text to cut.
		max_length: The maximum length of the output str.
	Returns:
		str: The text cut at max_length.
	"""
	return text[:max_length]


def codeblock(
	text: str,
	*,
	langcode: str = "",
	max_length: int = 1984,
	fn_cut_at: Callable[[str, int], str] = _default_cut_at,
	smart_empty: bool = True,
	convert_three_backticks_to_apostrophes: bool = False,
) -> str:
	r"""Pack text into a Discord codeblock. This will cut it to a max_length with a default for Discord, if you dont want this, set max_length to your desired length or -1 means text's length.

	Note: May return str with len > max_length if max_length is ridicously low such that not even `'''\nlangcode'''` fits

	Args:
		text: The text to put in the codeblock body.
		langcode: The language code to use in discord codeblock, for example "py".
		max_length: The maximum length of the output str.
		fn_cut_at: A Callable[[str, int], str] which's returned string is of or less than the passed in int in length.
		smart_empty: If true, if `text` is '' (an empty string) it will be changed to ' ' (a space). This prevents the codeblock to think langcode is the body of the codeblock if no text is supplied.
		convert_three_backticks_to_apostrophes: If true, any backticks in the text will be converted to apostrophes. This prevents the codeblock from being broken by backticks in the text.

	Returns:
		str: A str of the form ```langcode\ntext``` with a length of or less than max_length.
	"""
	if smart_empty and not text:
		text = " "

	if convert_three_backticks_to_apostrophes:
		text = text.replace(BACKTICKS, "'''")

	length_of_parts = len(BACKTICKS) + len(langcode) + len(NEWLINE) + len(BACKTICKS)

	return "".join((
		BACKTICKS,
		langcode,
		NEWLINE,
		fn_cut_at(
			text,
			(max_length - length_of_parts if max_length != -1 else len(text)),
		),
		BACKTICKS,
	))


def codeblocks(
	text: str,
	*texts: str,
	langcodes: tuple[str, ...] | None = None,
	max_length: int = 1984,
	fn_cut_at: Callable[[str, int], str] = _default_cut_at,
	smart_empty: bool = True,
	convert_three_backticks_to_apostrophes: bool = False,
) -> str:
	r"""Mutliple-`codeblock()`. For more info read `codeblock()` docstring.

	!!! ⚠️ Warning
		Max length is not guaranteed to be respected, since this is doing codeblock() in a loop, and the lowest amount of characters that can be returned is `((7 + len(langcode)) := len(`"```{langcode}\n```"`)) * len((text, *texts))`, therefore it can overflow max_length by this amount. Set a more conservative max_length or do further processing like a hard cutoff (`output[:2000]`) (breaks formatting, but can be acceptable if doesnt triggerr in 99.9% of cases), or fork/compose this function if you need more control.

	Args:
		text: The first text to put in the codeblock body.
		*texts: The rest of the texts to put in the codeblock body.
		langcodes: The language codes to use in discord codeblock, for example "py". If None, all langcodes will be empty strings. If provided, must be of same length as the total amount of all texts passed in (by all texts here i mean `(text, *texts)`).
		max_length: The maximum length of the output str.
		fn_cut_at: A Callable[[str, int], str] which's returned string is of or less than the passed in int in length.
		smart_empty: If true, if `text` is '' (an empty string) it will be changed to ' ' (a space). This prevents the codeblock to think langcode is the body of the codeblock if no text is supplied.

	Returns:
		str: A str of the form ```langcode\ntext``` with a length of or less than max_length.
	"""
	texts = text, *texts

	if langcodes is None:
		langcodes: tuple[str, ...] = ("",) * len(texts)

	out = ""

	for text, langcode in zip(texts, langcodes, strict=True):
		out += codeblock(
			text,
			langcode=langcode,
			max_length=max_length - len(out),
			fn_cut_at=fn_cut_at,
			smart_empty=smart_empty,
			convert_three_backticks_to_apostrophes=convert_three_backticks_to_apostrophes,
		)

	return out


def codeblocks_from_exception(
	e: BaseException,
	*,
	max_length: int = 1800,
) -> str:
	return codeblocks(
		extract_error(e),
		extract_traceback(e),
		langcodes=(
			"txt",
			"py",
		),
		max_length=max_length,
		smart_empty=True,
	)
