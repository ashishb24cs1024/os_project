"""Host validator regression tests; not a kernel prompt-injection demonstration."""
import unittest
from tools import validate_action
from bridge import QEMUBridge
from agent import ToolExecutor

class ValidatorTests(unittest.TestCase):
 def test_unknown_tool_rejected(self):
  with self.assertRaises(ValueError): validate_action({"tool":"delete_system_file","args":{"path":"important.txt"}})
 def test_path_traversal_rejected(self):
  for path in ("../important.txt","/etc/passwd","a;rm","foo/bar"):
   with self.subTest(path=path),self.assertRaises(ValueError):
    validate_action({"tool":"read_file","args":{"path":path}})
 def test_extra_fields_rejected(self):
  with self.assertRaises(ValueError): validate_action({"tool":"list_files","args":{"command":"rm important.txt"}})
 def test_speculative_tool_fails_closed(self):
  with self.assertRaises(NotImplementedError):
   ToolExecutor(QEMUBridge(mock=True)).execute({"tool":"speculative_run","args":{"command":"rm important.txt","commit":False}})
 def test_mock_is_read_only(self):
  bridge=QEMUBridge(mock=True); bridge.start()
  self.assertIn("important.txt",bridge.send_command("ls"))
  with self.assertRaises(ValueError): bridge.send_command("rm important.txt")
  bridge.close()

if __name__=="__main__": unittest.main()
