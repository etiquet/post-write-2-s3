#!/bin/bash
curl -X POST \
-H "Content-Type: application/xml; charset=UTF-8" \
-H "Accept-Encoding: gzip" \
-H "Content-Encoding: gzip" \
-H "X-Api-Key: ZHpiwUuiffdectKeJG24cVudQi9VXlYI" \
--data-binary "@20240615103132_odf.gzip" \
http://localhost:12000/ODFClient # change url
