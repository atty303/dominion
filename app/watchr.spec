# -*- mode: ruby; -*-
watch('.*\.py') { |md| system("python tests.py") }
