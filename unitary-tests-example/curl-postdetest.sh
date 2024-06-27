#!/bin/bash
curl -X POST \
-H "Content-Type: application/xml; charset=UTF-8" \
-H "Accept-Encoding: gzip" \
-H "Content-Encoding: gzip" \
-H "X-APIkey: d1a3d4cf-b379-426b-ab43-ddc29d7ce74a" \
--data-binary "@20240615103132_odf.gzip" \
http://localhost:5001/ODFClient
#attention sur mac le port 5000 est utilisé > passer à 5001 