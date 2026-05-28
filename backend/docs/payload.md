<!--
SPDX-FileCopyrightText: 2026 German Federal Office for Information Security (BSI) <https://www.bsi.bund.de>

SPDX-License-Identifier: Apache-2.0
-->

## Payload

Send from frontend to backend


    {
        // Required
        domain: string      // URL domain to check
        session_id: string  // Unique client session id (like UUID to identify client)

        // Optional
        ignore_cache: bool  // Client wants to check a domain, regardless of database cache. Default: False
        interrupt: bool     // Client interrupts their request, effectively stopping backend. Default: False
        enable_validator: bool // Runs CSAF Validator for every document downloaded by CSAF Checker. Default: True
    }
