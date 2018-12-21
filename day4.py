import sys
import re
from collections import defaultdict, Counter
from datetime import datetime

class Event(object):
    def __init__(self, when, guard_id, kind):
        self.when = when
        self.guard_id = guard_id
        self.kind = kind

    def __repr__(self):
        return "{} guard {} {}".format(self.when, self.guard_id, self.kind)

class Nap(object):
    def __init__(self, guard_id, start, end):
        self.guard_id = guard_id
        self.start = start
        self.end = end

    @property
    def duration(self):
        return (self.end - self.start).seconds / 60

    def __repr__(self):
        return "Guard {} slept from {} to {} ({} minutes)".format(self.guard_id, self.start, self.end, self.duration)

def parse_event(in_str):
    date_str = in_str[1:17]
    when = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    guard_id = -1
    id_match = re.search("#([0-9]+)", in_str)
    if id_match:
        guard_id = int(id_match.group(1))
        kind = in_str[id_match.end():].strip()
    else:
        kind = in_str[19:]
    return Event(when, guard_id, kind)

def events_to_naps(events):
    curr_guard = -1
    naps = []
    nap_start = None
    nap_end = None
    for event in events:
        if event.kind == 'begins shift':
            curr_guard = event.guard_id
        elif event.kind == 'falls asleep':
            nap_start = event.when
        elif event.kind == 'wakes up':
            nap_end = event.when
            naps.append(Nap(curr_guard, nap_start, nap_end))
    return naps

def find_sleepiest_guard(naps):
    guard_sleep_times = defaultdict(int)
    for nap in naps:
        guard_sleep_times[nap.guard_id] += nap.duration
    longest_time_asleep = -1
    sleepiest_guard = -1
    for guard, duration in guard_sleep_times.iteritems():
        if duration > longest_time_asleep:
            longest_time_asleep = duration
            sleepiest_guard = guard
    return sleepiest_guard, longest_time_asleep

def find_sleepiest_minute_for_guard(guard_id, naps):
    nap_minutes = defaultdict(int)
    for nap in naps:
        if nap.guard_id == guard_id:
            for x in xrange(nap.start.minute, nap.end.minute):
                nap_minutes[x] += 1
    sleepiest_minute = -1
    max_count = 0
    for k, v in nap_minutes.iteritems():
        if v > max_count:
            max_count = v
            sleepiest_minute = k
    return sleepiest_minute

def find_sleepiest_minute(naps):
    # the counter will be the count of (guard, minute) tuples
    guard_sleep_counter = Counter()
    for nap in naps:
        for x in xrange(nap.start.minute, nap.end.minute):
            guard_sleep_counter[(nap.guard_id, x)] += 1
    # most_common returns a list, so we need one "[0]" to get the actual most common value
    # then that is itself a tuple - in this case, ((guard, minute), count) - so we need another [0]
    guard, minute = guard_sleep_counter.most_common(1)[0][0]
    return guard, minute

def main(filename):
    events = []
    with open(filename) as f:
        for line in f:
            event = parse_event(line.strip())
            events.append(parse_event(line.strip()))
    events.sort(key=lambda x: x.when)
    naps = events_to_naps(events)
    # I kinda feel that solution 1 could be arrived at more cleanly
    sleepiest_guard, total_time_asleep = find_sleepiest_guard(naps)
    sleepiest_minute = find_sleepiest_minute_for_guard(sleepiest_guard, naps)
    # ...like solution 2 was
    guard, minute = find_sleepiest_minute(naps)
    print "Sleepiest guard = {}, with {} minutes asleep".format(sleepiest_guard, total_time_asleep)
    print "Sleepiest minute for guard {} is {}".format(sleepiest_guard, sleepiest_minute)
    print "Solution 1 = {}".format(sleepiest_guard * sleepiest_minute)
    print "The most common (guard, sleeping minute) combo is {}, {}".format(guard, minute)
    print "Solution 2 = {}".format(guard * minute)

if __name__ == '__main__':
    main(sys.argv[1])
