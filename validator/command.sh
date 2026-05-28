#!/bin/sh

# SPDX-FileCopyrightText: 2026 German Federal Office for Information Security (BSI) <https://www.bsi.bund.de>
#
# SPDX-License-Identifier: Apache-2.0

set -e

cd /app/node_modules/@secvisogram/csaf-validator-service || exit 1

# Run dev server
npm run dev
