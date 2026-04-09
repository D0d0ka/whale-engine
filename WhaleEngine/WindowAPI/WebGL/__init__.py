class windowAPI:
	def __init__(self, *args, **kwargs):
		raise NotImplementedError("WebGL backend is not implemented yet.")

	# Engine lifecycle
	def poll(self):
		raise NotImplementedError()

	def clear(self):
		raise NotImplementedError()

	def swap(self):
		raise NotImplementedError()

	def should_close(self):
		raise NotImplementedError()

	def terminate(self):
		raise NotImplementedError()

	# Input API
	def normalize_key(self, key):
		raise NotImplementedError()

	def set_key_callback(self, callback):
		raise NotImplementedError()

	def get_cursor_pos(self):
		raise NotImplementedError()

	def is_mouse_button_down(self, button):
		raise NotImplementedError()

	# Render API
	def create_texture_from_image(self, image):
		raise NotImplementedError()

	def render_2d_entities(self, entities):
		raise NotImplementedError()