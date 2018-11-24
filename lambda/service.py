# -*- coding: utf-8 -*-

import numpy
import sklearn


def handler(event, context):

	result = {"data": "helloooo!!!!"}
	return result

if __name__ == "__main__":
	print(handler(None, None))