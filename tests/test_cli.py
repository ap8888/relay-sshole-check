"""Offline synthetic tests; never run a daemon, authentication attempt or package manager."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

CLI = Path(__file__).resolve().parents[1] / 'bin' / 'relay-sshole-check'
SHELL = os.environ.get('TEST_SHELL', '/bin/sh')

class AssessmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='relay-sshole-test-')
        self.root = Path(self.tmp.name) / 'root with spaces'
        self.root.mkdir()
    def tearDown(self):
        self.tmp.cleanup()
    def put(self, name, value):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(value)
        return p
    def runcli(self, *args):
        return subprocess.run([SHELL, str(CLI), '--root', str(self.root), *args], text=True, capture_output=True)
    def assertReview(self, p):
        self.assertEqual(p.returncode, 1, p.stderr)
        self.assertIn('assessment=REVIEW_REQUIRED', p.stdout)
    def pattern(self):
        self.put('lib/ld-musl-test.so.1', '')
        self.put('etc/shadow', 'candidate:*:1:0:99999:7:::\nother:$6$SYNTHETIC_SECRET:1:0:99999:7:::\n')
    def test_empty_is_unknown(self):
        self.assertReview(self.runcli())
    def test_opt_in_shadow(self):
        self.pattern()
        p=self.runcli()
        self.assertReview(p)
        self.assertNotIn('local_exact_star_fields=',p.stdout)
    def test_priority_pattern(self):
        self.pattern()
        p=self.runcli('--shadow')
        self.assertEqual(p.returncode,2)
        self.assertIn('assessment=PRIORITY_REVIEW',p.stdout)
        for secret in ['candidate','other','SYNTHETIC_SECRET','$6$']:
            self.assertNotIn(secret,p.stdout+p.stderr)
    def test_missing_shadow(self):
        p=self.runcli('--shadow'); self.assertReview(p)
        self.assertIn('local_shadow=UNAVAILABLE',p.stdout)
    def test_locked_not_star(self):
        self.pattern()
        self.put('etc/shadow','a:!*:1:0:99999:7:::\nb:!!:1:0:99999:7:::\nc:!:1:0:99999:7:::\n')
        p=self.runcli('--shadow');self.assertReview(p)
        self.assertIn('local_exact_star_fields=0',p.stdout)
    def test_no_hash_partner(self):
        self.pattern();self.put('etc/shadow','a:*:1:0:99999:7:::\n')
        self.assertReview(self.runcli('--shadow'))
    def test_other_hash_does_not_trigger(self):
        self.pattern();self.put('etc/shadow','a:*:1:0:99999:7:::\nb:$y$SYNTHETIC:1:0:99999:7:::\n')
        self.assertReview(self.runcli('--shadow'))
    def test_sha256_partner(self):
        self.pattern();self.put('etc/shadow','a:*:1:0:99999:7:::\nb:$5$SYNTHETIC:1:0:99999:7:::\n')
        self.assertEqual(self.runcli('--shadow').returncode,2)
    def test_no_loader_no_priority(self):
        self.pattern();(self.root/'lib/ld-musl-test.so.1').unlink()
        self.assertReview(self.runcli('--shadow'))
    def test_malformed_shadow(self):
        self.pattern();self.put('etc/shadow','bad:*\n')
        p=self.runcli('--shadow');self.assertReview(p)
        self.assertIn('MALFORMED_OR_EMPTY',p.stdout)
    def test_empty_shadow(self):
        self.put('etc/shadow','');self.assertReview(self.runcli('--shadow'))
    def test_files_unchanged(self):
        self.pattern()
        def snapshot():
            return {str(p.relative_to(self.root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in self.root.rglob('*') if p.is_file()}
        before=snapshot();self.runcli('--shadow');self.assertEqual(before,snapshot())
    def test_os_release_never_sourced(self):
        marker=self.root/'executed'
        self.put('etc/os-release',f'ID="$(touch {marker})"\nVERSION_ID="3.24"\n')
        self.runcli();self.assertFalse(marker.exists())
    def test_config_is_counts_only(self):
        self.put('etc/ssh/sshd_config','  PasswordAuthentication=no\nMatch User private-name\n PasswordAuthentication yes\nInclude secret-path\nUsePAM no\n')
        p=self.runcli();self.assertReview(p)
        self.assertIn('main_config_password_directives=2',p.stdout)
        self.assertNotIn('private-name',p.stdout)
        self.assertNotIn('secret-path',p.stdout)
    def test_effective_is_not_safety_verdict(self):
        p=self.put('effective.txt','passwordauthentication no\nusepam yes\n')
        self.assertReview(self.runcli('--effective',str(p)))
    def test_effective_no_secret_echo(self):
        p=self.put('effective.txt','hostkey /secret\npasswordauthentication yes\nusepam no\n')
        r=self.runcli('--effective',str(p))
        self.assertNotIn('/secret',r.stdout)
        self.assertIn('supplied_effective_usepam=no',r.stdout)
    def test_fixed_package_still_review(self):
        self.put('lib/apk/db/installed','P:openssh-server\nV:10.3_p1-r2\n\nP:other\nV:1\n')
        p=self.runcli();self.assertReview(p)
        self.assertIn('apk_package=openssh-server@10.3_p1-r2',p.stdout)
    def test_new_upstream_still_review(self):
        self.put('lib/apk/db/installed','P:openssh-server\nV:10.6_p2-r0\n')
        self.assertReview(self.runcli())
    def test_missing_option_value(self):
        self.assertEqual(self.runcli('--effective').returncode,64)
    def test_relative_root_rejected(self):
        self.assertEqual(self.runcli('--root','relative').returncode,64)
    def test_unknown_option(self):
        self.assertEqual(self.runcli('--exploit').returncode,64)
    def test_missing_effective(self):
        self.assertEqual(self.runcli('--effective',str(self.root/'absent')).returncode,64)
    def test_no_target_binary_execution(self):
        marker=self.root/'executed'
        p=self.put('usr/sbin/sshd',f'#!/bin/sh\ntouch "{marker}"\n')
        p.chmod(0o755);self.runcli();self.assertFalse(marker.exists())
    def test_help_and_version(self):
        for option in ['--help','--version']:
            self.assertEqual(self.runcli(option).returncode,0)
    def test_syntax(self):
        self.assertEqual(subprocess.run([SHELL,'-n',str(CLI)]).returncode,0)

if __name__ == '__main__':
    unittest.main(verbosity=2)
