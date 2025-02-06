import smtplib
import email.message as email
import traceback
from src.core.utils import clear, wait
from src.core.lang import langs, c
from src.core.emails import emails_modals as emails


class SendEmail:
    def __init__(self, env, to: str, subject: str=None, content: str | dict=None, server: str | None=None):
        self._env = env
        self._to = to
        self._subject = subject
        self._content = content
        self._error = False
        self._server = 'smtp.gmail.com:587' if not server else server
        self._special_emails = ['email_test', 'error_log']
        self._status = False

        self._organizer()
        if not self._error: self._send_email()

    # método responsável por enviar emails
    def _send_email(self):
        clear(c('.', 'g', 'w'))
        message = email.Message()
        message['Subject'] = self._subject
        message['From'] = f'{self._env.BOT_NAME} <{self._env.EMAIL_ADDRESS}>'
        clear(c('...', 'g', 'w'))
        message['To'] = self._to
        message.add_header('Content-Type', 'text/html')
        message.set_payload(self._content)
        clear(c('.....', 'g', 'w'))

        try:
            with smtplib.SMTP(self._server) as server:
                clear(c('.', 'g', 'w'))
                # faz login apenas em produção
                if self._server == 'smtp.gmail.com:587':
                    server.starttls()
                    server.login(self._env.EMAIL_ADDRESS, self._env.EMAIL_PASSWORD)
                clear(c('...', 'g', 'w'))
                server.sendmail(message['From'], message['To'], message.as_string().encode('utf-8'))

                clear(langs(self._env)[self._env.LANG]['SUCCESSFULLY_EMAIL_SEND'])

                self._status = True
        
        except smtplib.SMTPAuthenticationError:
            clear(langs(self._env)[self._env.LANG]['INVALID_CREDENTIALS'])

    
    # retorna o status
    @property
    def status(self) -> bool:
        return self._status


    # método que organiza o envio do email
    def _organizer(self):
        if not all([self._env.EMAIL_ADDRESS, self._env.EMAIL_PASSWORD]):
            clear(langs(self._env)[self._env.LANG]['EMAIL_NOT_CONFIGURED'])
            self._error = True
            return

        if not self._subject: self._subject = input(langs(self._env)[self._env.LANG]['SET_SUBJECT'])
        if not self._content and self._subject not in self._special_emails: self._content = input(langs(self._env)[self._env.LANG]['SET_CONTENT'])

        modal = self._get_modals_email
        
        if not modal: return

        self._subject = modal['subject']
        self._content = modal['content']


    # retorna os modelos de email
    @property
    def _get_modals_email(self) -> dict:
        modals = {
            'email_test': {'subject': f'{self._env.BOT_NAME} - Test Email', 'content': emails.test_email(self._env)},
            'error_log': {'subject': f'{self._env.BOT_NAME} - Error', 'content': emails.error_log(self._env, self._content)}
        }

        modal = modals.get(self._subject)

        return modal

        