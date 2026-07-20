from nya_codeblock import codeblocks


def test_codeblocks():
	code1 = "print('Hello, World!')"
	code2 = "print('Goodbye, World!')"

	result = codeblocks(
		code1,
		code2,
		langcodes=("python", "python"),
	)

	assert result == f"```python\n{code1}``````python\n{code2}```"


def test_codeblocks_no_langcodes():
	code1 = "print('Hello, World!')"
	code2 = "print('Goodbye, World!')"

	result = codeblocks(
		code1,
		code2,
	)

	assert result == f"```\n{code1}``````\n{code2}```"
