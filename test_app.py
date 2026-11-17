import os, pickle, shutil, tempfile, unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
LINE = 'INS:256183 ADMIS Moye=18.39 Algo=19.75 Math=19 STI=19.7 ScPh=18 Angl=16.75 Fran=12.5 Arab=13.87 Phil=11.5 EdPh=99.99 Espa=20'


class InTmp(unittest.TestCase):
    def setUp(self):
        self.old = os.getcwd()
        self.tmp = tempfile.mkdtemp()
        shutil.copy(os.path.join(HERE, 'inst.txt'), self.tmp)
        os.chdir(self.tmp)

    def tearDown(self):
        os.chdir(self.old)
        shutil.rmtree(self.tmp)


class TestSearch(InTmp):
    def test_verif(self):
        from search import verif
        self.assertTrue(verif(LINE))
        self.assertFalse(verif('hello'))
        self.assertFalse(verif(LINE.replace('Algo', 'xxxx')))


class TestInterface(InTmp):
    def test_hex(self):
        from interface import rgb_to_hex
        self.assertEqual(rgb_to_hex(0, 0, 0), '#000000')
        self.assertEqual(rgb_to_hex(255, 16, 1), '#FF1001')

    def test_extract(self):
        import interface
        interface.initialisation()
        interface.extract(LINE, interface.t, interface.nt)
        e = pickle.load(open('data.dat', 'rb'))
        self.assertEqual((e['INS'], e['Res'], e['Moye'], e['Opt']), ('256183', 'ADMIS', '18.39', '20'))
        self.assertEqual(e['EdPh'], '99.99')

    def test_extract_refuse(self):
        import interface
        interface.initialisation()
        interface.extract(LINE.replace('ADMIS', 'REFUSE'), interface.t, interface.nt)
        self.assertEqual(pickle.load(open('data.dat', 'rb'))['Res'], 'REFUSE')

    def test_play_refused_does_not_crash(self):
        import interface
        interface.initialisation()
        interface.extract(LINE.replace('ADMIS', 'REFUSE'), interface.t, interface.nt)
        interface.root = mock.MagicMock()
        interface.guide = mock.MagicMock()
        with mock.patch.object(interface.tk, 'Label'):
            interface.play()
        interface.f.close()  # play() keeps inst.txt open for the guessing phase


class TestMain(InTmp):
    def test_save_zone_accepts_decimal(self):
        import main
        with mock.patch('builtins.input', side_effect=['abc', '25', '14.5']):
            main.saisir_save_zone()
        self.assertEqual(open('moy.txt').read(), '15.5')

    def test_launch_uses_current_python(self):
        import main, sys
        with mock.patch.object(main, 'check_mail', return_value=True), \
             mock.patch.object(main, 'run') as r, mock.patch.object(main.winsound, 'MessageBeep'):
            main.mail_method()
        self.assertEqual(r.call_args[0][0][0], sys.executable)


class TestMail(InTmp):
    def _run(self, subject, body):
        import mailforw
        raw = ('Subject: %s\r\n\r\n%s' % (subject, body)).encode()
        m = mock.MagicMock()
        m.__enter__.return_value = m
        m.search.return_value = ('OK', [b'1'])
        m.fetch.return_value = ('OK', [(b'1', raw)])
        with mock.patch.object(mailforw.imaplib, 'IMAP4_SSL', return_value=m), \
             mock.patch.dict(os.environ, EMAIL='a@b.c', APP_PASSWORD='x'):
            return mailforw.check_mail(), m

    def test_matching_mail_saved(self):
        ok, m = self._run('[SMSFW] x 97754430', 'junk\n************\n' + LINE)
        self.assertTrue(ok)
        self.assertEqual(open('msg.txt').read().strip(), LINE)
        m.__exit__.assert_called()

    def test_multipart_wrapped_forward(self):
        import mailforw
        wrapped = LINE.replace(' Fran', '\nFran')  # sms-fw/Gmail hard-wrap the plain part
        raw = ('Subject: Fwd: [SMSFW] (+21697754430)\r\nMIME-Version: 1.0\r\n'
               'Content-Type: multipart/alternative; boundary="b"\r\n\r\n'
               '--b\r\nContent-Type: text/plain; charset="UTF-8"\r\n\r\n'
               'Forwarded\r\nFrom: 85005\r\n************\r\n' + wrapped + '\r\n\r\n'
               '--b\r\nContent-Type: text/html\r\n\r\n<div>x</div>\r\n--b--\r\n').encode()
        m = mock.MagicMock()
        m.__enter__.return_value = m
        m.search.return_value = ('OK', [b'1'])
        m.fetch.return_value = ('OK', [(b'1', raw)])
        with mock.patch.object(mailforw.imaplib, 'IMAP4_SSL', return_value=m), \
             mock.patch.dict(os.environ, EMAIL='a@b.c', APP_PASSWORD='x'):
            self.assertTrue(mailforw.check_mail())
        self.assertEqual(open('msg.txt').read().strip(), LINE)


    def test_other_mail(self):
        ok, _ = self._run('hello', 'x')
        self.assertFalse(ok)

    def test_no_subject(self):
        ok, _ = self._run('', 'x')
        self.assertFalse(ok)


    def test_load_env(self):
        import mailforw
        open('e', 'w').write('# c\nFOO_T=bar\nBAZ_T="q q"\n')
        with mock.patch.dict(os.environ, clear=False):
            mailforw.load_env('e')
            self.assertEqual((os.environ['FOO_T'], os.environ['BAZ_T']), ('bar', 'q q'))
        os.environ.pop('FOO_T', None); os.environ.pop('BAZ_T', None)


if __name__ == '__main__':
    unittest.main()
