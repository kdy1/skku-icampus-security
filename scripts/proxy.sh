#!/bin/bash

mitmdump -p 9999 --ignore-hosts ':443$' -s proxy.py