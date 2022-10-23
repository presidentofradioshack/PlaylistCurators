from re import search, findall

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
				if '.' not in match:
					handle = match

					return handle
		
		return ''