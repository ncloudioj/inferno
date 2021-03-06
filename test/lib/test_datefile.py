from nose.tools import ok_
import os
from inferno.lib.datefile import Datefile
from datetime import datetime
from datetime import timedelta
import time

TEST_FILE = 'xxxx___test_datefile___'

class TestDatefile(object):
    def delete(self):
        print 'setup'
        if os.path.exists(os.path.join('/tmp', TEST_FILE)):
            os.remove(os.path.join('/tmp', TEST_FILE))

    def test_creation(self):
        # ensure newly created Datefiles are 'old'
        self.delete()
        after = datetime.utcnow()
        datefile = Datefile('/tmp', TEST_FILE)
        actual = datefile.timestamp
        ok_(after > actual)
        ok_(os.path.exists(os.path.join('/tmp', TEST_FILE)))

    def test_reopening(self):
        # test overriding the timestamp
        before = datetime.utcnow()
        datefile = Datefile('/tmp', TEST_FILE, timestamp=datetime.utcnow())
        actual = datefile.timestamp
        ok_(before < actual)

    def test_is_older_than(self):
        self.delete()
        before = datetime.utcnow()
        datefile = Datefile('/tmp', TEST_FILE)
        ok_(datefile.is_older_than({'seconds': 2}))
        ok_(datefile.is_older_than({'days': 2}))
        # test will stop working on Jan 1, 2170
        ok_(not datefile.is_older_than({'days': 73000}))
        datefile.touch(before)
        time.sleep(3)
        ok_(datefile.is_older_than({'seconds': 2}))
        ok_(not datefile.is_older_than({'minutes': 5}))

    def test_oclock_ran_yesterday(self):
        self.delete()
        now = datetime.utcnow()
        if now.hour == 23:
            now -= timedelta(hours=1)
        before = now - timedelta(hours=26)
        datefile = Datefile('/tmp', TEST_FILE, timestamp=before)
        ok_(datefile.is_older_than({'oclock': now.hour}))
        ok_(not datefile.is_older_than({'oclock': now.hour + 1}))


    def test_oclock_ran_today(self):
        self.delete()
        now = datetime.utcnow()
        if now.hour == 23:
            now -= timedelta(hours=1)
        if now.hour < 2:
            now += timedelta(hours=1)
        before = now - timedelta(hours=1)
        datefile = Datefile('/tmp', TEST_FILE, timestamp=before)
        ok_(not datefile.is_older_than({'oclock': now.hour}))


    def test_touch(self):
        datefile = Datefile('/tmp', TEST_FILE)
        actual = datefile.timestamp
        after = datetime.utcnow()
        datefile.touch()
        ok_(datefile.timestamp > actual)
        ok_(actual < after)




