import unittest

try:
    from tools.analyze_performance_capture_bundle import analyze_bundle
except ImportError:
    from analyze_performance_capture_bundle import analyze_bundle


BUNDLE = """Theft4 performance capture export
Generated: 2026-01-01 00:00:00 +0000
Device: iPhone / iPhone15,4

===== Theft4/startup/frame-captures/publication-trace-2026-01-01-00-00-00-ABCD.csv (10 bytes) =====
kind,frame,monotonic_ns,lost_count,note
status,,,,collecting
frame,1,1000000000,,
frame,2,1050000000,,
marker,3,1060000000,,user-lag-spike
status,,,,saved

===== Theft4/startup/frame-captures/renderer-timing-2026-01-01-00-00-00-ABCD.csv (10 bytes) =====
# host_tick_frequency=24000000
frame,begin_tick,recording_ticks,driver_submit_ticks,cpu_publish_ns,cpu_interval_ns,sample_valid,release_count,resolve_count,clear_count,native_record_bytes,draw_indexed_count
1,0,240000,120000,0,0,0,0,1,1,0,10
2,1000,240000,120000,1000000,50000000,3,0,2,1,4096,20

===== Theft4/startup/frame-captures/runtime-callers-2026-01-01-00-00-00-ABCD.csv (10 bytes) =====
# host_tick_frequency=24000000
monotonic_ns,frame,thread_id,kind,site,calls,samples,wall_ticks,max_wall_ticks
1000,1,7,6,0x1,10,1,24000,24000
2000,2,7,6,0x1,20,2,48000,24000

===== Theft4/startup/frame-captures/frame-scheduling-2026-01-01-00-00-00-ABCD.csv (10 bytes) =====
event,monotonic_ns,thread_id,work_kind
4,1000,7,6
"""


class AnalyzePerformanceCaptureBundleTest(unittest.TestCase):
    def test_bundle_summary(self):
        result = analyze_bundle(BUNDLE)
        self.assertEqual(result["run_token"], "2026-01-01-00-00-00")
        publication = result["publication"]
        self.assertEqual(publication["frames"], 2)
        self.assertAlmostEqual(publication["intervals_ms"]["p50"], 50.0)
        self.assertEqual(publication["statuses"], ["collecting", "saved"])
        self.assertEqual(publication["user_lag_spikes"][0]["frame"], 3)
        self.assertEqual(
            publication["user_lag_spikes"][0]["nearby_intervals"]["count"], 1)
        renderer = result["renderer"]
        self.assertAlmostEqual(renderer["recording_ticks_ms"]["p50"], 10.0)
        self.assertEqual(renderer["cpu_publish_ms_valid"]["count"], 1)
        self.assertEqual(renderer["release_count"]["max"], 0)
        self.assertEqual(renderer["draw_indexed_count"]["p50"], 10.0)
        callers = result["runtime_callers"]
        self.assertEqual(callers["top_sites"][0]["calls"], 20)
        self.assertAlmostEqual(callers["top_sites"][0]["wall_ms"], 2.0)


if __name__ == "__main__":
    unittest.main()
