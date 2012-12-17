A script that takes a URL and outputs the sitemap for all the pages on its domain, and the static assets used on each page.

Requirements and setup
----------------------
Tested on Python 2.7 only.

Clone this repo and set up a Python virtualenv for it, then install the requirements (requests, lxml, nose):

    mkvirtualenv site-mapper
    pip install -r requirements.txt


Running the tests
-----------------
One of the tests uses a locally run webserver so first bring up a test server on `localhost:8000` by doing:

    cd example/
    python -m SimpleHTTPServer


Then in another temrinal, simply run the tests (nose should have been installed as part of the requirements):

    nosetests


Actually running the script
---------------------------
From the repo root, run the following and wait for the sitemap result:

    ./site_mapper/mapper_cli.py http://example.com


The output will look something like this:

    ------------------------------------------------------------------------
    Page '/products.html' has links to these pages:
        /
        /company/team.html

    Page '/products.html' has links to these assets:
    	http://cdn.com/lib.js
    	http://example.com/app.js

    ------------------------------------------------------------------------
    Page '/' has links to these pages:
    	/
    	/company/team.html
    	/products.html

    Page '/' has links to these assets:
    	http://cdn.com/lib.js
    	http://example.com/app.css
    	http://example.com/app.js

