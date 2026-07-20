from nya_codeblock import codeblock


def test_codeblock_simple():
	result = codeblock("Hello, World!")
	assert result == "```\nHello, World!```"


def test_codeblock_with_langcode():
	result = codeblock("print('Hello, World!')", langcode="python")
	assert result == "```python\nprint('Hello, World!')```"


def test_codeblock_max_length():
	result = codeblock("This is a long text that should be cut.", max_length=24)
	assert result == "```\nThis is a long te```"
	assert len(result) <= 24


def test_codeblock_smart_empty():
	with_smart_empty = codeblock("", smart_empty=True)
	assert with_smart_empty == "```\n ```"

	without_smart_empty = codeblock("", smart_empty=False)
	assert without_smart_empty == "```\n```"
