import smtplib
import email.message as email
import traceback
from src.core.utils import clear
from src.core.lang import langs, c
from src.core.emails import emails_modals as emails, email_logger


class SendEmail:
    def __init__(self, env, to: str, subject: str=None, content: str | dict=None, server: str | None=None, system: bool=False):
        email_logger().info('The sending email process starts')
        self._env = env
        self._to = to
        self._subject = subject
        self._content = content
        self._error = None
        self._server = 'smtp.gmail.com:587' if not server else server
        self._special_emails = ['email_test', 'critical_error']
        self._status = False
        self._system = system

        self._organizer()
        if not self._error: self._send_email()

    # método responsável por enviar emails
    def _send_email(self):
        if not self._system: clear('Sending email...' if self._env.LANG == 'en' else 'Enviando e-mail...')
        message = email.Message()
        message['Subject'] = self._subject
        message['From'] = f'{self._env.BOT_NAME} <{self._env.EMAIL_ADDRESS}>'
        message['To'] = self._to
        message.add_header('Content-Type', 'text/html')
        message.set_payload(self._content)

        try:
            email_logger().info('Configuring SMTP server')
            with smtplib.SMTP(self._server) as server:
                # faz login apenas em produção
                if self._server == 'smtp.gmail.com:587':
                    server.starttls()
                    email_logger().info('Logging into the server')
                    server.login(self._env.EMAIL_ADDRESS, self._env.EMAIL_PASSWORD)
                    email_logger().info(f'Server configured with email: {self._env.EMAIL_ADDRESS}')
                
                email_logger().info(f'Sending email to: {self._to}')
                server.sendmail(message['From'], message['To'], message.as_string().encode('utf-8'))

                if not self._system: clear(langs(self._env)[self._env.LANG]['SUCCESSFULLY_EMAIL_SEND'])
                email_logger().info(f'Email sent successfully.\n\tFrom: {self._env.EMAIL_ADDRESS}\n\tTo: {self._to}\n\tSubject: {self._subject}')
                self._status = True
        
        except smtplib.SMTPAuthenticationError:
            email_logger().error(f'The credentials used are invalid')
            if not self._system: clear(langs(self._env)[self._env.LANG]['INVALID_CREDENTIALS'])
            self._error = 'invalid_credentials'

        except Exception as e:
            email_logger().error(f'An unknown error has occurred:\n\t{traceback.format_exc()}')
            msg = 'Ocorreu um erro desconhecido:' if self._env.LANG == 'pt' else 'An unknown error has occurred:'
            clear(c(f'{msg}\n\t{traceback.format_exc()}', 'r'))
    
    # retorna o status
    @property
    def status(self) -> bool:
        return self._status
    

    # retorna error
    @property
    def error(self) -> None | str:
        return self._error


    # método que organiza o envio do email
    def _organizer(self):
        if not all([self._env.EMAIL_ADDRESS, self._env.EMAIL_PASSWORD]):
            if not self._system: clear(langs(self._env)[self._env.LANG]['EMAIL_NOT_CONFIGURED'])
            self._error = 'email_not_configured'

        if not self._subject:
            email_logger().info('This email will be sent by the user')
            self._subject = input(langs(self._env)[self._env.LANG]['SET_SUBJECT'])
        else:
            email_logger().info('This email will be sent by the system')

        if not self._content and self._subject not in self._special_emails:
            self._content = input(langs(self._env)[self._env.LANG]['SET_CONTENT'])
            email_logger().info(f'The content of the email:\n\t{self._content}')

        modal = self._get_modals_email
        
        if not modal: return

        self._subject = modal['subject']
        self._content = modal['content']


    # retorna os modelos de email
    @property
    def _get_modals_email(self) -> dict:
        modals = {
            'email_test': {'subject': f'{self._env.BOT_NAME} - Test Email', 'content': emails.test_email(self._env)},
            'critical_error': {'subject': f'{self._env.BOT_NAME} - Error', 'content': emails.critical_error(self._env, self._content)}
        }

        modal = modals.get(self._subject)

        return modal

        