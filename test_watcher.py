import os, tempfile, time, unittest
from pathlib import Path
from eve_escalation_watcher import TEXT, Universe, data_dir, default_sound_file, newest_chat_file, parse, parse_bridges, parse_chat_line

class WatcherTests(unittest.TestCase):
    def test_all_interface_translation_keys_exist_in_both_languages(self):
        keys = {"settings", "language", "theme", "light", "dark", "home", "radius", "sound", "bridges", "update", "folder", "start", "stop", "sound_file", "choose_sound", "test", "volume", "chat_wait", "clear_chat", "matching", "clear_list", "time", "seller", "system", "jumps", "message", "catalog_load", "catalog_ready", "downloading", "download_error", "choose_folder", "choose_alert", "update_first", "folder_required", "watching", "stopped", "no_file", "switched", "found", "read_error", "bridges_title", "bridges_help", "unknown", "bridges_saved", "save_replace", "cancel", "unknown_system"}
        for language in ("uk", "en"):
            self.assertTrue(keys.issubset(TEXT[language]), language)
    def test_bundled_alert_is_used_when_no_sound_is_saved(self):
        self.assertEqual(Path(default_sound_file()), data_dir() / "alert1.mp3")
        self.assertEqual(default_sound_file("C:/custom/alert.wav"), "C:/custom/alert.wav")
    def test_any_message_with_nearby_system_alerts(self):
        near = {"LK1K-5": 3, "M9-FIB": 5}
        line = "[20:27:27] Alcatraz202 > LK1K-5 angel 10 150m 22h"
        self.assertEqual(parse(line, near), [("20:27:27", "Alcatraz202", "LK1K-5", 3, "LK1K-5 angel 10 150m 22h")])
    def test_exact_for_example_message_is_ignored(self):
        self.assertEqual(parse("[20:27:27] Seller > For example", {"FOR-EXAMPLE": 3}), [])
    def test_all_nearby_systems_in_one_message_alert(self):
        near = {"LK1K-5": 3, "M9-FIB": 5}
        offers = parse("[20:27:27] Seller > LK1K-5 and M9-FIB escalations", near)
        self.assertEqual([offer[2] for offer in offers], ["LK1K-5", "M9-FIB"])
    def test_purchase_marker_after_system_is_excluded(self):
        near = {"LK1K-5": 3, "M9-FIB": 5}
        for text in ("LK1K-5 x 150m", "M9-FIB х 150m", "LK1K-5 x", "LK1K-5 X.", "M9-FIB Х,"):
            self.assertEqual(parse(f"[20:27:27] Buyer > {text}", near), [])
    def test_only_exact_purchase_marker_is_excluded(self):
        near = {"LK1K-5": 3}
        for text in ("LK1K-5 x150m", "LK1K-5  x 150m", "LK1K-5 sale x 150m", "LK1K-5 x. 150m"):
            self.assertEqual(len(parse(f"[20:27:27] Seller > {text}", near)), 1)
    def test_chat_line_is_available_even_without_system(self):
        self.assertEqual(parse_chat_line("[ 2026.10.20 19:14:33 ] A > hello"), ("2026.10.20 19:14:33", "A", "hello"))
    def test_newest_file_ignores_other_chat_names(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder); old=p/"Imperium Expeditions_20261020_181158_2120170704.txt"; new=p/"Imperium Expeditions_20261020_181200_2120322300.txt"; other=p/"Локальний_20261020_181200_2120322300.txt"; invalid=p/"Imperium Expeditions_1.txt"
            header="Channel Name:    Imperium Expeditions\n"
            old.write_text(header,encoding="utf-16");new.write_text(header,encoding="utf-16")
            other.write_text("Channel Name:    Локальний\n",encoding="utf-16");invalid.write_text(header,encoding="utf-16")
            os.utime(old,(99,99));os.utime(new,(1,1));os.utime(other,(999,999))
            self.assertEqual(newest_chat_file(p),new)
    def test_bfs_radius(self):
        u=Universe();u.names={x:x for x in "A B C D".split()};u.graph={"A":{"B"},"B":{"A","C"},"C":{"B","D"},"D":{"C"}}
        self.assertEqual(u.nearby("A",2), {"A":0,"B":1,"C":2})
    def test_jump_bridges_are_bidirectional_and_count_as_one_jump(self):
        u=Universe();u.names={x:x for x in "HOME GATE REMOTE".split()};u.graph={"HOME":{"GATE"},"GATE":{"HOME"},"REMOTE":set()}
        bridges=parse_bridges("REMOTE -> HOME\nHOME -> REMOTE\ninvalid")
        self.assertEqual(bridges, [("HOME","REMOTE")])
        self.assertEqual(u.nearby("HOME",1,bridges), {"HOME":0,"GATE":1,"REMOTE":1})
if __name__ == "__main__": unittest.main()
