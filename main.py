#!/usr/bin/env python

import report

rep = report.Report()
# Authenticate
rep.create_api_connection()
# Generate report
rep.run()
