from __future__ import unicode_literals, division, absolute_import
from builtins import *  # pylint: disable=unused-import, redefined-builtin


class TestSeriesList(object):
    config = """
        templates:
          global:
            disable: [seen]

        tasks:
          list_get:
            series_list: test_list

          test_list_add:
            mock:
              - {title: 'series 1', url: "http://mock.url/file1.torrent"}
            accept_all: yes
            list_add:
              - series_list: test_list

          test_basic_configure_series:
            mock:
              - {title: 'series 1.s01e01.720p.HDTV-flexget', url: "http://mock.url/file1.torrent"}
            configure_series:
              from:
                series_list: test_list

          test_add_with_attributes:
            mock:
              - {title: 'series 1',
                 set: {movedone: "/random/path"},
                 url: "http://mock.url/file1.torrent",
                 tvdb_id: "1234",
                 tvmaze_id: "1234",
                 not_valid_id: "1234",
                 trakt_show_id: "1234",
                 alternate_name: [SER1, SER2],
                 name_regexp: ["^ser", "^series 1$"],
                 quality: 720p,
                 qualities: [720p, 1080p],
                 timeframe: '2 days',
                 upgrade: yes,
                 propers: yes,
                 specials: yes,
                 not_a_real_attribute: yes,
                 tracking: 'backfill',
                 identified_by: "ep"}
            accept_all: yes
            list_add:
              - series_list: test_list

    """

    def test_base_series_list(self, execute_task):
        task = execute_task('test_list_add')
        assert len(task.accepted) == 1

        task = execute_task('list_get')
        assert len(task.entries) == 1
        assert task.find_entry(title='series 1')

    def test_base_configure_series_with_list(self, execute_task):
        task = execute_task('test_list_add')
        assert len(task.accepted) == 1

        task = execute_task('test_basic_configure_series')
        assert len(task.accepted) == 1
        assert task.find_entry(category='accepted', series_name='series 1')

    def test_series_list_with_attributes(self, execute_task):
        task = execute_task('test_add_with_attributes')
        assert len(task.accepted) == 1

        task = execute_task('list_get')
        assert len(task.entries) == 1
        entry = task.find_entry(title='series 1')
        assert entry

        assert entry['set']['movedone'] == '/random/path'
        assert entry['set']['tvdb_id'] == '1234'
        assert entry['set']['tvmaze_id'] == '1234'
        assert entry['set']['trakt_show_id'] == '1234'
        assert entry['quality'] == '720p'
        assert entry['alternate_name'] == ['SER1', 'SER2']
        assert entry['name_regexp'] == ["^ser", "^series 1$"]
        assert entry['qualities'] == ['720p', '1080p']
        assert entry['timeframe'] == '2 days'
        assert entry['upgrade'] == True
        assert entry['propers'] == True
        assert entry['specials'] == True
        assert entry['tracking'] == 'backfill'
        assert entry['identified_by'] == 'ep'
        assert not entry.get('not_a_real_attribute')
