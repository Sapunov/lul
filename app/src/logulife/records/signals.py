from django.dispatch import Signal


ready_to_process = Signal(providing_args=['instance'])
