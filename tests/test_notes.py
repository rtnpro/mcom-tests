#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests
from BeautifulSoup import BeautifulStoneSoup
from unittestzero import Assert
from pages.desktop.notes import Notes


class TestNotes:

    @pytest.mark.nondestructive
    def test_that_notes_page_is_reachable(self, mozwebqa):
        notes_page = Notes(mozwebqa)
        notes_page.go_to_page()
        Assert.contains("Notes", notes_page.firefox_notes_header_text)

    @pytest.mark.skip_selenium
    @pytest.mark.nondestructive
    def test_that_all_links_are_valid(self, mozwebqa):
        notes_page = Notes(mozwebqa)
        url = mozwebqa.base_url + notes_page.notes_page_url
        page_response = requests.get(url)
        html = BeautifulStoneSoup(page_response.content)
        bad_urls = []
        links = html.findAll('a')
        for link in links:
            url = self.make_absolute(link['href'], mozwebqa.base_url)
            if not notes_page.is_valid_link(url):
                bad_urls.append('%s is not a valid url' % url)
        Assert.equal(0, len(bad_urls), '%s bad urls found: ' % len(bad_urls) + ', '.join(bad_urls))

    def make_absolute(self, url, base_url):
        if url.startswith('http'):
            return url
        return base_url + url
