import uuid

from unique_identifier_msgs.msg import UUID
from unique_identifier_python import *

# random UUID generation tests
def test_random_uuids():
    N = 1000
    uu = []
    for i in xrange(N):
        uu.append(fromRandom())
        assert isinstance(uu[i], uuid.UUID)
        for j in xrange(i-1, -1, -1):
            assert uu[i] != uu[j]

# UUID generation from URL tests
def test_empty_url():
    x = fromURL('')
    assert isinstance(x, uuid.UUID)
    y = fromURL('')
    assert isinstance(y, uuid.UUID)
    assert x == y
    # MUST yield same result as C++ fromURL() function:
    assert str(x) == "1b4db7eb-4057-5ddf-91e0-36dec72071f5"

def test_same_url():
    x = fromURL('http://openstreetmap.org/node/1')
    assert isinstance(x, uuid.UUID)
    y = fromURL('http://openstreetmap.org/node/1')
    assert isinstance(y, uuid.UUID)
    assert x == y
    # MUST yield same result as C++ fromURL() function:
    assert str(x) == 'ef362ac8-9659-5481-b954-88e9b741c8f9'

def test_same_id_different_osm_namespace():
    x = fromURL('http://openstreetmap.org/node/1')
    y = fromURL('http://openstreetmap.org/way/1')
    assert x != y
    # MUST yield same result as C++ fromURL() function:
    assert str(y) == 'b3180681-b125-5e41-bd04-3c8b046175b4'

def test_actual_osm_node_id():
    x = fromURL('http://openstreetmap.org/node/1')
    y = fromURL('http://openstreetmap.org/node/152370223')
    assert x != y
    # MUST yield same result as C++ fromURL() function:
    assert str(y) == '8e0b7d8a-c433-5c42-be2e-fbd97ddff9ac'

def test_route_segment():
    start = 'da7c242f-2efe-5175-9961-49cc621b80b9'
    end = '812f1c08-a34b-5a21-92b9-18b2b0cf4950'
    x = fromURL('http://ros.org/wiki/road_network/' + start + '/' + end)
    y = fromURL('http://ros.org/wiki/road_network/' + end + '/' + start)
    assert x != y
    # MUST yield same result as C++ fromURL() function:
    assert str(x) == 'acaa906e-8411-5b45-a446-ccdc2fc39f29'

# UUID message generation tests
def test_msg_creation():
    msg = toMsg(fromURL('http://openstreetmap.org/node/152370223'))
    assert toHexString(msg) == '8e0b7d8a-c433-5c42-be2e-fbd97ddff9ac'

def test_msg_same_id_different_namespace():
    x = toMsg(fromURL('http://openstreetmap.org/node/1'))
    y = toMsg(fromURL('http://openstreetmap.org/way/1'))
    assert x != y
    assert toHexString(y) == 'b3180681-b125-5e41-bd04-3c8b046175b4'

def test_msg_route_segment():
    start = 'da7c242f-2efe-5175-9961-49cc621b80b9'
    end = '812f1c08-a34b-5a21-92b9-18b2b0cf4950'
    x = toMsg(fromURL('http://ros.org/wiki/road_network/'
                      + start + '/' + end))
    y = toMsg(fromURL('http://ros.org/wiki/road_network/'
                      + end + '/' + start))
    assert x != y
    assert toHexString(x) == 'acaa906e-8411-5b45-a446-ccdc2fc39f29'

def test_nil_msg():
    x = UUID()
    y = toMsg(uuid.UUID(hex='00000000-0000-0000-0000-000000000000'))
    assert x == y

def test_random_msg():
    x = UUID()
    y = toMsg(fromRandom())
    assert x != y

def test_equivalent_msgs():
    s = 'da7c242f-2efe-5175-9961-49cc621b80b9'
    x = toMsg(uuid.UUID(s))
    y = toMsg(uuid.UUID(s))
    assert x == y
    assert s == toHexString(y)

def test_to_and_from_msg():
    x = uuid.UUID('da7c242f-2efe-5175-9961-49cc621b80b9')
    y = (fromMsg(toMsg(x)))
    assert x == y
    assert isinstance(y, uuid.UUID)

def test_msg_to_string():
    s = 'da7c242f-2efe-5175-9961-49cc621b80b9'
    x = toMsg(uuid.UUID(s))
    y = toHexString(x)
    assert x == y
    assert isinstance(y, str)

# UUID Time-Based Generation
# TODO(jacobperron): enable these for ROS 2
# def test_time(self):
#    hw_addr = 0xAABBCCDDEEFF
#    t = rospy.Time(1515778146, 239216089)
#    uu = fromTime(t, hw_addr)  # generate UUID
#    offset = 122192928000000000  # in 100ns intervals between RFC4122 timestamp and epoch time
#    ns_intervals_rfc = uu.fields[0] + (uu.fields[1] << 32) + ((uu.fields[2] & 0x0FFF) << 48)
#    ns_intervals_epoch = ns_intervals_rfc - offset
#    uu_time = rospy.Time()
#    uu_time.secs = long(ns_intervals_epoch / 1e9 * 100)
#    uu_time.nsecs = long(ns_intervals_epoch - uu_time.secs / (100 * 1e-9)) * 100
#
#    self.assertEqual(t.secs, uu_time.secs)
#    # Expect 89ns to be shaved off due to timestamp being stored in 100ns intervals
#    self.assertEqual(t.nsecs - uu_time.nsecs, 89)
#    # Should be able to retrieve the hardware id
#    self.assertEqual(hw_addr, uu.fields[5])

# def test_time_same_interval(self):
#    hw_addr = 0xAABBCCDDEEFF
#    t1 = rospy.Time(1515778146, 239216020)
#    t2 = rospy.Time(1515778146, 239216080)
#    uu1 = fromTime(t1, hw_addr)  # generate UUID for t1
#    uu2 = fromTime(t2, hw_addr)  # generate UUID for t2
#    offset = 122192928000000000  # in 100ns intervals between RFC4122 timestamp and epoch time
#
#    # Get time associated with uuid uu1
#    ns_intervals_rfc = uu1.fields[0] + (uu1.fields[1] << 32) + ((uu1.fields[2] & 0x0FFF) << 48)
#    ns_intervals_epoch = ns_intervals_rfc - offset
#    uu1_time = rospy.Time()
#    uu1_time.secs = long(ns_intervals_epoch / 1e9 * 100)
#    uu1_time.nsecs = long(ns_intervals_epoch - uu1_time.secs / (100 * 1e-9)) * 100
#
#    # Get time associated with uuid uu2
#    ns_intervals_rfc = uu2.fields[0] + (uu2.fields[1] << 32) + ((uu2.fields[2] & 0x0FFF) << 48)
#    ns_intervals_epoch = ns_intervals_rfc - offset
#    uu2_time = rospy.Time()
#    uu2_time.secs = long(ns_intervals_epoch / 1e9 * 100)
#    uu2_time.nsecs = long(ns_intervals_epoch - uu2_time.secs / (100 * 1e-9)) * 100
#
#    self.assertEqual(uu1_time.secs, uu2_time.secs)
#    # Timestamps should be same as they were generated for timestamps in the same 100ns interval
#    self.assertEqual(uu1_time.nsecs, uu2_time.nsecs)
#    # UUIDs should be different due to different (hopefully) randomly generated 14-bit clock ids 
#    self.assertNotEqual(uu1, uu2)

# def test_time_different_interval(self):
#    hw_addr = 0xAABBCCDDEEFF
#    t1 = rospy.Time(1515778146, 239216020)
#    t2 = rospy.Time(1515778146, 239216120)
#    uu1 = fromTime(t1, hw_addr)  # generate UUID for t1
#    uu2 = fromTime(t2, hw_addr)  # generate UUID for t2
#    offset = 122192928000000000  # in 100ns intervals between RFC4122 timestamp and epoch time
#
#    # Get time associated with uuid uu1
#    ns_intervals_rfc = uu1.fields[0] + (uu1.fields[1] << 32) + ((uu1.fields[2] & 0x0FFF) << 48)
#    ns_intervals_epoch = ns_intervals_rfc - offset
#    uu1_time = rospy.Time()
#    uu1_time.secs = long(ns_intervals_epoch / 1e9 * 100)
#    uu1_time.nsecs = long(ns_intervals_epoch - uu1_time.secs / (100 * 1e-9)) * 100
#
#    # Get time associated with uuid uu2
#    ns_intervals_rfc = uu2.fields[0] + (uu2.fields[1] << 32) + ((uu2.fields[2] & 0x0FFF) << 48)
#    ns_intervals_epoch = ns_intervals_rfc - offset
#    uu2_time = rospy.Time()
#    uu2_time.secs = long(ns_intervals_epoch / 1e9 * 100)
#    uu2_time.nsecs = long(ns_intervals_epoch - uu2_time.secs / (100 * 1e-9)) * 100
#
#    # Timestamps were generated for the same second
#    self.assertEqual(uu1_time.secs, uu2_time.secs)
#    # Timestamps should be different as they were generated for times in different 100ns intervals
#    self.assertNotEqual(uu1_time.nsecs, uu2_time.nsecs)
