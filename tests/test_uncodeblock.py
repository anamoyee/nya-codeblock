from nya_codeblock import codeblock, uncodeblock


def test_uncodeblock():
	code = "print('Hello, World!')"
	langcode = "python"
	code_block = f"```{langcode}\n{code}\n```"

	extracted_code = uncodeblock(code_block)

	assert extracted_code == code


def test_uncodeblock_no_langcode():
	code = "print('Hello, World!')"
	code_block = f"```\n{code}\n```"

	extracted_code = uncodeblock(code_block)

	assert extracted_code == code


def test_uncodeblock_from_codeblock():
	code = "print('Hello, World!')"

	code_block = codeblock(code, langcode="python")
	extracted_code = uncodeblock(code_block)

	assert extracted_code == code
