from re import findall, search, sub


class StringUtil():
	def check_string_for_email(string):
		email = search(r'[\w.+-]+@[\w-]+\.\w+', string)

		if email:
			return email.group(0)
		
		return ''

	def check_string_for_insta(string):
		matches = findall(r'@\S+', string)
		handle = ''

		if matches:
			for match in matches:
				no_special_characters = sub('/[^a-zA-Z0-9\.\_@]/g', '', match)

				if '.com' not in no_special_characters:
					handle = no_special_characters

					return handle
		
		return ''
