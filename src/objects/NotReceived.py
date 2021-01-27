"""
NotReceived

When an expected input is not received, it will be given an instance
of the NotReceived class
SO that things do not mix up
None != NotReceived
"""
class NotReceived(object):
	def __init__(self):
		pass
		