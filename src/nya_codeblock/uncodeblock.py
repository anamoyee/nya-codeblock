from .codeblock import BACKTICKS, NEWLINE


def uncodeblock(text: str) -> str:
	"""*Try to* remove any markdown/discord codeblocks along with their langcodes if any are found.

	Args:
		text: The text to remove markdown/discord codeblocks from.

	Returns:
		str: The text with any markdown/discord codeblocks removed.
	"""
	if text[-3:] == BACKTICKS and text[:3] == BACKTICKS:
		code_start = 3
		code_end = -3
		if NEWLINE in text[3:]:  # Check if there is a language code specified
			code_start = text.index(NEWLINE) + 1
		return text[code_start:code_end].strip()
	return text
