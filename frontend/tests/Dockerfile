# SPDX-FileCopyrightText: 2026 German Federal Office for Information Security (BSI) <https://www.bsi.bund.de>
#
# SPDX-License-Identifier: Apache-2.0

FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tests
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["pytest", "-v"]
